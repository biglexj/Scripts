import os
import shutil
import logging

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

TARGET_DIR = r"d:\Música\IA Sounds\Instrumental"

def undo_organization():
    if not os.path.exists(TARGET_DIR):
        logging.error("Directorio no encontrado.")
        return

    count = 0
    # Caminar por subdirectorios
    for root, dirs, files in os.walk(TARGET_DIR):
        # Ignorar la raíz misma
        if root == TARGET_DIR:
            continue
        
        for file in files:
            if file.lower().endswith('.flac'):
                src = os.path.join(root, file)
                dst = os.path.join(TARGET_DIR, file)
                
                # Manejar colisiones si existen (aunque no deberían ser muchas en este punto)
                if os.path.exists(dst):
                    base, ext = os.path.splitext(file)
                    dst = os.path.join(TARGET_DIR, f"{base}_undo{ext}")
                
                shutil.move(src, dst)
                count += 1
    
    # Limpiar carpetas vacías
    for root, dirs, files in os.walk(TARGET_DIR, topdown=False):
        if root == TARGET_DIR:
            continue
        if not os.listdir(root):
            os.rmdir(root)

    logging.info(f"✨ Se han movido {count} archivos de vuelta a la raíz y se han limpiado las carpetas.")

if __name__ == "__main__":
    undo_organization()
