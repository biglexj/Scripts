import json
import os
import logging

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

BASE_DIR = r"d:\Música\IA Sounds"
FILES = [
    os.path.join(BASE_DIR, "metadata_instrumental.json"),
    os.path.join(BASE_DIR, "metadata_instrumental_2.json"),
    os.path.join(BASE_DIR, "metadata_instrumental_3.json")
]
OUTPUT_FILE = os.path.join(BASE_DIR, "instrumental.json")

def merge_metadata():
    unified_data = []
    current_id = 1

    for file_path in FILES:
        if not os.path.exists(file_path):
            logging.warning(f"Archivo no encontrado: {file_path}")
            continue
        
        logging.info(f"Procesando {os.path.basename(file_path)}...")
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
            for item in data:
                # Re-indexar ID
                item['id'] = current_id
                unified_data.append(item)
                current_id += 1

    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(unified_data, f, indent=4, ensure_ascii=False)
    
    logging.info(f"✨ Éxito. Creado {OUTPUT_FILE} con {len(unified_data)} entradas secuenciales.")

if __name__ == "__main__":
    merge_metadata()
