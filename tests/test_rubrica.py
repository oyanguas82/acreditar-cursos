"""Pruebas de comportamiento sobre intervalos y entradas inválidas."""
import importlib.util, uuid, unittest
from pathlib import Path
path = Path(__file__).resolve().parents[1] / "plugins/acreditacion-cursos-unad/skills/acreditacion-unad/scripts/validar_rubrica.py"
spec = importlib.util.spec_from_file_location("rubricas", path)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
BASE = "criterio,maximo,nivel,desde,hasta\nC1,12,Ausente,0,0\nC1,12,Bajo,1,7\nC1,12,Medio,8,9\nC1,12,Alto,10,12\n"

class Rangos(unittest.TestCase):
    def check_text(self, text, total=12):
        fixture_dir = Path(__file__).resolve().parents[1] / "build-local/fixtures-rangos"
        fixture_dir.mkdir(parents=True, exist_ok=True)
        file = fixture_dir / (uuid.uuid4().hex + ".csv")
        file.write_text(text, encoding="utf-8")
        return module.validar(file, total)
    def test_valida(self):
        self.assertTrue(self.check_text(BASE)["valido"])
    def test_suma_criterios(self):
        text = BASE + "\n".join(line.replace("C1,", "C2,") for line in BASE.splitlines()[1:]) + "\n"
        result = self.check_text(text, 24)
        self.assertTrue(result["valido"])
        self.assertEqual(result["total_calculado"], 24)
    def test_solapamiento(self):
        self.assertFalse(self.check_text(BASE.replace("Medio,8,9", "Medio,7,9"))["valido"])
    def test_hueco(self):
        self.assertFalse(self.check_text(BASE.replace("Medio,8,9", "Medio,9,9"))["valido"])
    def test_falta_final(self):
        self.assertFalse(self.check_text(BASE.replace("Alto,10,12", "Alto,10,11"))["valido"])
    def test_entrada_invalida(self):
        for value in ("true", "", "-1", "1.5", "NaN"):
            with self.subTest(value=value):
                self.assertFalse(self.check_text(BASE.replace("C1,12,Bajo", f"C1,{value},Bajo"))["valido"])
    def test_maximos_inconsistentes(self):
        self.assertFalse(self.check_text(BASE.replace("C1,12,Alto", "C1,13,Alto"))["valido"])
    def test_nombre_duplicado(self):
        self.assertFalse(self.check_text(BASE.replace("Medio,", "Bajo,"))["valido"])
    def test_limite_fuera(self):
        self.assertFalse(self.check_text(BASE.replace("Alto,10,12", "Alto,10,13"))["valido"])
    def test_total_distinto(self):
        self.assertFalse(self.check_text(BASE, 25)["valido"])
    def test_vacio(self):
        self.assertFalse(self.check_text(BASE.splitlines()[0] + "\n")["valido"])
    def test_cabecera(self):
        with self.assertRaises(ValueError):
            self.check_text(BASE.replace("maximo", "puntos"))
    def test_columna_faltante(self):
        self.assertFalse(self.check_text(BASE.replace("C1,12,Alto,10,12", "C1,12,Alto,10"))["valido"])

if __name__ == "__main__":
    unittest.main(verbosity=2)
