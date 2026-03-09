# Notas de Lanzamiento - Scripts Utility

## [1.4.0] - 2026-03-08

### ✨ Novedades
- **Evolución "Power-Up"**: El script `crear_subcarpetas_estandar.py` ahora es dinámico.
- **Menú Interactivo**: Selección de carpetas (Assets, Proyecto, Render, Guion, Miniatura, etc.).
- **Selección Múltiple**: Permite crear varias carpetas a la vez indicando sus números.

## [1.3.0] - 2026-03-08

### ✨ Novedades
- **Integración con PowerShell**: Se han añadido alias globales al perfil de PowerShell (`$PROFILE`) para ejecutar los scripts desde cualquier ubicación.
- **Nuevos Alias**: `clonar-est`, `crear-sub`, `renombrar-it`, `sfx-gen`, `wav2flac`.
- **Documentación**: Sección de atajos añadida al `README.md`.

## [1.2.0] - 2026-03-08

### ✨ Novedades
- **Reorganización Estructural**: Se han movido los scripts a subdirectorios (`organizacion/`, `gestion/`, `multimedia/`) para mejorar la escalabilidad del proyecto.
- **Documentación**: Actualizado el `README.md` con las nuevas rutas de acceso.

## [1.1.0] - 2026-03-08

### ✨ Novedades
- **Nuevo Script**: `crear_subcarpetas_estandar.py` para automatizar la estructura interna de proyectos (`Assets`/`Proyecto`).
- **Reorganización**: El `README.md` ahora agrupa los scripts por categorías (Organización, Gestión, Multimedia).

## [1.0.0] - 2026-03-08

### ✨ Novedades
- **Clonador de Estructura**: Implementación de `clonar_estructura.py` para duplicar carpetas sin archivos.
- **Renombrador Inteligente**: Implementación de `renombrar_archivos_carpetas.py` con múltiples formatos (Snake, Camel, Pascal, etc.).
- **Estructura SFX**: Script `estructura_sfx.ps1` para organizar librerías de sonido.

### 📝 Documentación
- Creación de `README.md` detallado en español.
- Configuración de `.gitignore` para limpieza del repositorio.

---
*Primera versión estable de las herramientas de automatización.*
