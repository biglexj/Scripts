# 🛠️ Scripts Utility - Automatización y Organización

Este repositorio contiene una colección de herramientas diseñadas para simplificar tareas repetitivas de gestión de archivos y estructuras de carpetas.

## 📂 Organización de Proyectos

### 🏗️ Creador de Subcarpetas Dinámico (`organizacion/crear_subcarpetas_estandar.py`)
Automatiza la preparación de proyectos con una estructura flexible y a medida.
*   **Acción**: Permite elegir mediante un menú qué carpetas crear (Assets, Proyecto, Render, Guion, Miniaturas, etc.).
*   **Características**: Selección múltiple (ej. `1 5 7`), lista extendida de categorías, manejo de existencias.
*   **Uso**:
    ```bash
    python organizacion/crear_subcarpetas_estandar.py "C:/Ruta/De/Proyectos"
    ```

### 📂 Clonador de Estructura (`organizacion/clonar_estructura.py`)
Duplica la jerarquía de carpetas de un origen a un destino **sin copiar archivos**.
*   **Características**: Modo recursivo, modo raíz, opciones de fusión o reemplazo.
*   **Uso**:
    ```bash
    python organizacion/clonar_estructura.py "C:/Ruta/Origen" "D:/Ruta/Destino"
    ```

### 🔄 Deshacer Organización (`organizacion/undo_organization.py`)
Script de utilidad para revertir cambios de organización.

---

## 🏷️ Gestión de Archivos

### 🖊️ Renombrador Inteligente (`gestion/renombrar_archivos_carpetas.py`)
Normaliza nombres de archivos y carpetas masivamente.
*   **Formatos**: `Title Case`, `UPPER CASE`, `snake_case`, `kebab-case`, `PascalCase`, `camelCase`, etc.
*   **Características**: Modo simulación (Dry Run), control de profundidad, selectivo para archivos o carpetas.
*   **Uso**: `python gestion/renombrar_archivos_carpetas.py`

---

## 🔊 Recursos Multimedia

### 🎵 Procesamiento de Audio
*   **Audio SFX (`multimedia/estructura_sfx.ps1`)**: Genera librerías categorizadas de sonido.
*   **Conversión WAV a FLAC (`multimedia/wav_a_flac.py`)**: Conversión automatizada de archivos de audio.
*   **Gestión de Metadatos**:
    *   `multimedia/extract_metadata_to_json.py`: Extrae metadatos de audio a JSON.
    *   `multimedia/merge_json_metadata.py`: Combina múltiples archivos de metadatos.
    *   `multimedia/sync_json_to_flac.py`: Sincroniza metadatos JSON de vuelta a archivos FLAC.

## ⚡ Atajos (PowerShell)

Si has configurado tu `$PROFILE`, puedes usar estos comandos desde cualquier terminal:

| Comando | Script | Descripción |
| :--- | :--- | :--- |
| `clonar-est` | `clonar_estructura.py` | Clonar carpetas (solo estructura). |
| `crear-sub` | `crear_subcarpetas_estandar.py` | Crear Assets/Proyecto en subcarpetas. |
| `renombrar-it` | `renombrar_archivos_carpetas.py` | Renombrado masivo inteligente. |
| `sfx-gen` | `estructura_sfx.ps1` | Generar estructura para SFX. |
| `wav2flac` | `wav_a_flac.py` | Convertir WAV a FLAC. |
| `init-docs` | `init_project_docs.py` | Crear documentación y `.agents/rules/base.md` desde las plantillas. |

### Inicializar documentación y reglas

Desde la raíz de cualquier proyecto:

```powershell
init-docs
```

El comando procesa los placeholders de `templates/`, conserva archivos existentes y crea la regla siempre activa `.agents/rules/base.md`. Usa `init-docs --force` únicamente cuando quieras regenerar y sobrescribir los documentos administrados; `--no-rules` omite la regla.

---

## 🛠️ Requisitos e Instalación

*   **Python 3.x** y **PowerShell**.
*   Clona el repo y ejecuta directamente, no requiere dependencias externas.
