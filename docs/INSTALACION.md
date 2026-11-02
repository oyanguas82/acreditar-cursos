# Instalación

## ChatGPT mediante GitHub

Para un espacio de trabajo que permita importar plugins, un administrador puede registrar este repositorio desde la administración de plugins. Use `oyanguas82/acreditar-cursos`, rama `main` y el catálogo `.agents/plugins/marketplace.json`. La fuente del complemento es `plugins/acreditacion-cursos-unad`.

La importación y la sincronización requieren los permisos correspondientes del espacio y de GitHub. Publicar los archivos aquí no activa por sí solo el plugin en una cuenta. [Procedimiento oficial de OpenAI](https://learn.chatgpt.com/docs/enterprise/plugin-management).

El ZIP `dist/acreditacion-cursos-unad-chatgpt-1.1.0.zip` permite guardar o actualizar el paquete mediante Plugin Creator en una cuenta compatible. Contiene un único plugin portable y sus recursos. El complemento privado creado anteriormente conserva su identidad y audiencia, y no se cambia automáticamente al publicar el repositorio.

## ChatGPT de escritorio y Codex

El catálogo del repositorio permite registrar el origen con:

```text
codex plugin marketplace add oyanguas82/acreditar-cursos --ref main
```

Después, abra el directorio de plugins de la aplicación compatible, seleccione el origen **Acreditación de cursos UNAD** e instale el complemento. Inicie una sesión nueva para usar sus componentes. La disponibilidad depende del cliente y sus políticas.

Como habilidad local independiente, copie la carpeta completa `plugins/acreditacion-cursos-unad/skills/acreditacion-unad` a la ubicación de habilidades que admita su cliente. Conserve sus referencias y recursos. [Empaquetado y catálogos OpenAI](https://developers.openai.com/plugins/build/plugins).

## Claude Code

Desde una sesión:

```text
/plugin marketplace add oyanguas82/acreditar-cursos
/plugin install acreditacion-cursos-unad@acreditar-cursos
```

Para comprobar localmente el manifiesto sin ejecutar una conversación:

```text
claude plugin validate ./plugins/acreditacion-cursos-unad --strict
```

La habilidad del plugin se identifica como `/acreditacion-cursos-unad:acreditacion-unad`. Alternativamente, extraiga el ZIP para Claude y cargue la carpeta con `claude --plugin-dir ./acreditacion-cursos-unad`. [Catálogos Claude Code](https://code.claude.com/docs/en/plugin-marketplaces) · [Referencia de plugins](https://code.claude.com/docs/en/plugins-reference).

## Claude web, escritorio o Cowork

1. Descargue `dist/acreditacion-unad-1.1.0.zip`.
2. Abra **Customize → Skills → + → Create skill → Upload a skill**.
3. Cargue el ZIP y active la habilidad.
4. Pruebe un encargo con documentos del curso.

El ZIP contiene una carpeta `acreditacion-unad/` con `SKILL.md` y sus recursos. La disponibilidad depende de las capacidades y políticas de su cuenta. [Carga de skills en Claude](https://support.claude.com/en/articles/12512180-use-skills-in-claude).

## Comprobación en cada anfitrión

Pida primero una revisión acotada y compruebe que se cargó la habilidad. Revise las fuentes usadas y el archivo entregado. Para Office, recursos interactivos, importaciones Moodle y acceso OAI, compruebe además el producto real y el permiso disponible. La validación de manifiestos no sustituye estas pruebas.
