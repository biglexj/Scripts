# Instrucción para el Agente: Alineación de Documentación del Proyecto

El objetivo es alinear este proyecto con las plantillas de documentación estándar de Biglex J de forma segura, sin sobreescribir ni destruir información existente (como historiales de cambios o licencias).

## Tareas a Realizar:

1. **Configurar .gitignore**:
   - Añade `/test/` y `/scratch/` al archivo `.gitignore` del proyecto para evitar subir archivos temporales al repositorio.

2. **Inicializar Documentos Faltantes (sin sobreescribir)**:
   - Inspecciona las plantillas en `D:\Proyectos\biglexj\Scripts\templates`.
   - Crea `agent.md`, `ROADMAP.md` y `RELEASE_MESSAGE.md` en la raíz de este proyecto (solo si no existen).
   - Genera `.agents/rules/base.md` desde `templates/agent.md`, con frontmatter `trigger: always_on`, sin sobrescribir reglas existentes.
   - **Reemplazo de Placeholders**: Sustituye `{{PROJECT_NAME}}`, `{{YEAR}}`, `{{AUTHOR}}`, `{{DATE}}` y `{{LICENSE}}` con la información del proyecto actual.
   - **Adaptación Tecnológica**: Adapta cualquier regla de la plantilla `agent.md` al ecosistema tecnológico de este proyecto (por ejemplo, si el proyecto no es Node.js, reemplaza la mención de `package.json` por los archivos de configuración de versiones reales como `.csproj`, `Cargo.toml`, `pyproject.toml`, `go.mod`, etc.).

3. **Corregir Inconsistencias de Versionado**:
   - Revisa `RELEASE_NOTES.md`.
   - Asegúrate de que las versiones futuras que introduzcan características importantes estén etiquetadas como versiones menores (minor, ej: `v1.1.0`) y no como parches (patch, ej: `v1.0.1`).
   - Asigna un nombre en clave de dulce/postre a la versión mayor actual (ej: `v1.0.0`, `v2.0.0`) y coordínalo en los archivos del proyecto.

4. **Confirmación**:
   - Genera un archivo `walkthrough.md` en la raíz del proyecto o resume los cambios realizados al finalizar.
