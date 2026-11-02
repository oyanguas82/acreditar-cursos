# Asistente de acreditación de cursos UNAD

Complemento y skill en español para **ChatGPT, Codex y Claude**, con revisión documental, diseño académico y constitución del expediente de un curso.

## Qué permite hacer

- Revisar coherencia entre RAC/RAP, syllabus, guías, rúbricas, agenda y evidencias.
- Diseñar y producir materiales académicos, componente práctico, OVA/OVI y bancos GIFT.
- Organizar fuentes, entregables, hallazgos, responsables y condiciones de cierre.
- Verificar matemáticamente los rangos enteros de una rúbrica.
- Trabajar con **18 formatos, instructivos y ejemplos institucionales incluidos**.

El agente distingue ERROR, MEJORA y VERIFICAR. Registra por separado las comprobaciones en archivos, las pruebas de aula y el aval institucional.

## Descargas de la versión 1.1.0

| Uso | Archivo |
|---|---|
| Complemento ChatGPT / Codex | [ZIP ChatGPT](dist/acreditacion-cursos-unad-chatgpt-1.1.0.zip) |
| Complemento Claude Code | [ZIP Claude](dist/acreditacion-cursos-unad-claude-1.1.0.zip) |
| Skill para cargar en Claude | [ZIP de la skill](dist/acreditacion-unad-1.1.0.zip) |
| Skill empaquetada | [Archivo .skill](dist/acreditacion-unad-1.1.0.skill) |
| Integridad de descargas | [SHA256SUMS.txt](dist/SHA256SUMS.txt) |

[Instrucciones de instalación para cada plataforma](docs/INSTALACION.md).

### Claude Code desde este repositorio

En una sesión de Claude Code:

```text
/plugin marketplace add oyanguas82/acreditar-cursos
/plugin install acreditacion-cursos-unad@acreditar-cursos
```

Después de instalar, la habilidad se invoca como `/acreditacion-cursos-unad:acreditacion-unad`. El catálogo propio sigue el mecanismo de [marketplaces de Claude Code](https://code.claude.com/docs/en/plugin-marketplaces).

### ChatGPT y Codex

El catálogo está en `.agents/plugins/marketplace.json`. El paquete portable conserva `plugin.json` y la compatibilidad `.codex-plugin/plugin.json`. Consulte [instalación](docs/INSTALACION.md) para importación desde GitHub y para uso local. El repositorio publicado y el catálogo público oficial de plugins tienen procesos distintos.

### Claude en la web o escritorio

Descargue el ZIP de la skill y cárguelo desde **Customize → Skills → + → Create skill → Upload a skill**. Active la habilidad. Esta ruta está documentada por [Claude](https://support.claude.com/en/articles/12512180-use-skills-in-claude).

## Primer encargo

> Usa la habilidad acreditacion-unad para revisar los documentos de este curso. Identifica las fuentes aplicables, construye la matriz de trazabilidad y entrega un preconcepto con evidencias y decisiones pendientes.

Aporte los documentos del curso, oferta de referencia y de destino, matriz curricular, syllabus, agenda y evidencia de aula según el alcance. Para Sistemas Operativos 202016895 se conserva el antecedente de usar 1604-2026 como base de 2601 y señalar lo pendiente de ratificar.

## Formatos y procedencia

Los 18 archivos originales están en [assets/formatos](plugins/acreditacion-cursos-unad/skills/acreditacion-unad/assets/formatos). El [catálogo](plugins/acreditacion-cursos-unad/skills/acreditacion-unad/assets/catalogo-formatos.json) contiene sus huellas.

El apéndice Excel original contiene 16 referencias rotas. La habilidad exige corregir una copia de trabajo y verificarla antes de usarla. Consulte el [catálogo explicativo](plugins/acreditacion-cursos-unad/skills/acreditacion-unad/references/formatos.md).

La persona responsable autorizó expresamente incluir los 18 formatos en este repositorio público. Se conserva la licencia MIT existente para el código original del proyecto y las condiciones de los materiales de terceros en [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md).

## Desarrollo y verificación

La fuente común está en `plugins/acreditacion-cursos-unad/skills/acreditacion-unad`. Los paquetes de ambas plataformas salen de esa misma fuente.

```text
python -m pip install -r requirements-dev.txt
python -m unittest discover -s tests -v
python tools/validar.py
python tools/empaquetar.py
python tools/validar.py --archives
```

[Alcance y resultados de verificación](docs/VALIDACION.md) · [Cambios](CHANGELOG.md).

El complemento prepara y revisa el expediente. El aval corresponde al actor institucional competente. El paquete no incluye una conexión propia a Moodle, OAI ni al repositorio de RED.
