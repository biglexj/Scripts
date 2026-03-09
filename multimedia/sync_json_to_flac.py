import os
import json
import shutil
from mutagen.flac import FLAC
import logging
from collections import defaultdict
import re

# Configuración de logs
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

# Configuración de origen (Debe coincidir con la extracción)
FOLDER_SUFFIX = "3" # O "3"
TARGET_DIR = fr"d:\Música\IA Sounds\Instrumental {FOLDER_SUFFIX}"
JSON_FILE = fr"d:\Música\IA Sounds\metadata_instrumental_{FOLDER_SUFFIX}.json"

def sanitize_filename(name):
    """Elimina caracteres no válidos para nombres de archivos/carpetas."""
    return "".join(c for c in name if c.isalnum() or c in (' ', '.', '_', '-')).strip()

def clean_title(filename):
    """Limpia el nombre de archivo para encontrar el título base (mismo que en extraccion)."""
    base = os.path.splitext(filename)[0]
    base = base.replace("_undo", "").strip()
    # Coincidir con el regex de extracción: [\s-]*\d+$
    base = re.sub(r'[\s-]*\d+$', '', base).strip()
    base = re.sub(r'\s*\(Extend\)', '', base, flags=re.IGNORECASE).strip()
    return base

def sync_and_organize():
    if not os.path.exists(JSON_FILE):
        logging.error(f"No se encontró el archivo JSON: {JSON_FILE}")
        return

    with open(JSON_FILE, 'r', encoding='utf-8') as f:
        metadata_list = json.load(f)

    # 1. Agrupar y ordenar archivos físicos EXACTAMENTE igual que el script de extracción
    all_files = [f for f in os.listdir(TARGET_DIR) if f.lower().endswith('.flac') and os.path.isfile(os.path.join(TARGET_DIR, f))]
    
    file_data = []
    for filename in all_files:
        path = os.path.join(TARGET_DIR, filename)
        try:
            audio = FLAC(path)
            album = audio.get("album", [""])[0]
            title = audio.get("title", [""])[0]
            file_data.append({
                "filename": filename,
                "path": path,
                "album_tag": album if album else clean_title(filename),
                "title_tag": title
            })
        except:
            pass

    groups = defaultdict(list)
    for item in file_data:
        groups[item["album_tag"]].append(item)

    # Reconstruir la lista ordenada de archivos físicos
    sorted_physical_files = []
    for album_name in sorted(groups.keys()):
        group_items = groups[album_name]
        def group_sort_key(item):
            is_base = 0 if item["title_tag"].lower() == album_name.lower() or os.path.splitext(item["filename"])[0].lower() == album_name.lower() else 1
            return (is_base, item["filename"].lower())
        group_items.sort(key=group_sort_key)
        sorted_physical_files.extend(group_items)

    if len(sorted_physical_files) != len(metadata_list):
        logging.warning(f"Discrepancia: {len(sorted_physical_files)} archivos vs {len(metadata_list)} entradas JSON.")

    logging.info("Iniciando sincronización y organización...")

    for i, entry in enumerate(metadata_list):
        if i >= len(sorted_physical_files):
            break

        file_item = sorted_physical_files[i]
        src_path = file_item["path"]

        new_title = entry['title']
        album_name = entry['album']
        bpm = entry['bpm']
        track_num = entry.get('track_count', 1)

        try:
            # 1. Actualizar Metadatos
            audio = FLAC(src_path)
            audio["title"] = new_title
            audio["album"] = album_name
            audio["bpm"] = str(bpm)
            audio["tracknumber"] = str(track_num)
            audio.save()

            # 2. Organizar
            album_folder_name = sanitize_filename(album_name)
            album_path = os.path.join(TARGET_DIR, album_folder_name)
            if not os.path.exists(album_path):
                os.makedirs(album_path)

            new_filename = f"{sanitize_filename(new_title)}.flac"
            dst_path = os.path.join(album_path, new_filename)

            counter = 1
            final_dst = dst_path
            while os.path.exists(final_dst):
                final_dst = os.path.join(album_path, f"{sanitize_filename(new_title)} ({counter}).flac")
                counter += 1

            shutil.move(src_path, final_dst)
            logging.info(f"✅ [{i+1}] {file_item['filename']} -> {album_folder_name}/{os.path.basename(final_dst)}")

        except Exception as e:
            logging.error(f"❌ Error en {file_item['filename']}: {e}")

    logging.info("✨ Sincronización completa.")

if __name__ == "__main__":
    sync_and_organize()
