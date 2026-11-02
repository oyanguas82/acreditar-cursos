"""Valida rangos enteros en CSV. No decide calidad pedagógica ni aval institucional."""
import argparse
import csv
import json
import re
import sys
from pathlib import Path

HEADERS = ["criterio", "maximo", "nivel", "desde", "hasta"]

def entero(valor, campo, fila):
    if not isinstance(valor, str) or not re.fullmatch(r"0|[1-9][0-9]*", valor.strip()):
        raise ValueError(f"Fila {fila}: {campo} debe ser un entero no negativo.")
    return int(valor.strip())

def validar(path, total=None):
    errors, groups = [], {}
    with Path(path).open(encoding="utf-8-sig", newline="") as stream:
        reader = csv.DictReader(stream)
        if reader.fieldnames != HEADERS:
            raise ValueError("Cabecera esperada: " + ",".join(HEADERS))
        for rowno, row in enumerate(reader, 2):
            try:
                if None in row or any(v is None for v in row.values()):
                    raise ValueError(f"Fila {rowno}: número de columnas incorrecto.")
                name, level = row["criterio"].strip(), row["nivel"].strip()
                if not name or not level:
                    raise ValueError(f"Fila {rowno}: criterio y nivel son obligatorios.")
                maximum, low, high = [entero(row[k], k, rowno) for k in ("maximo", "desde", "hasta")]
                if maximum == 0 or low > high or high > maximum:
                    raise ValueError(f"Fila {rowno}: máximo o límites incoherentes.")
                groups.setdefault(name, []).append((maximum, level, low, high, rowno))
            except ValueError as error:
                errors.append(str(error))
    if not groups:
        errors.append("No hay criterios válidos.")
    computed_total = 0
    for name, rows in groups.items():
        maxima = {r[0] for r in rows}
        if len(maxima) != 1:
            errors.append(f"{name}: máximos inconsistentes.")
            continue
        maximum = maxima.pop()
        computed_total += maximum
        levels = [r[1].casefold() for r in rows]
        if len(levels) != len(set(levels)):
            errors.append(f"{name}: nombre de nivel repetido.")
        if len(rows) < 2:
            errors.append(f"{name}: se necesitan al menos dos niveles.")
        cursor = 0
        for _, level, low, high, rowno in sorted(rows, key=lambda r: (r[2], r[3])):
            if low > cursor:
                errors.append(f"{name}: hueco {cursor}–{low - 1} antes de {level}.")
            if low < cursor:
                errors.append(f"{name}: solapamiento en fila {rowno}, nivel {level}.")
            cursor = max(cursor, high + 1)
        if cursor <= maximum:
            errors.append(f"{name}: hueco final {cursor}–{maximum}.")
    if total is not None and computed_total != total:
        errors.append(f"Total calculado {computed_total}, total esperado {total}.")
    return {"valido": not errors, "total_calculado": computed_total, "criterios": len(groups),
            "errores": errors, "alcance": "Solo estructura y rangos enteros; revisar descriptores y escala aprobada."}

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("csv")
    parser.add_argument("--total", type=int, help="Total aprobado para la actividad, sin valor predeterminado.")
    args = parser.parse_args()
    try:
        if args.total is not None and args.total <= 0:
            raise ValueError("--total debe ser positivo.")
        report = validar(args.csv, args.total)
    except (ValueError, OSError, UnicodeError, csv.Error) as error:
        report = {"valido": False, "errores": [str(error)]}
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if report["valido"] else 1

if __name__ == "__main__":
    sys.exit(main())
