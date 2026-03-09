"""
Script: wav_a_flac.py
Función:
  - Busca todos los WAV en la carpeta raíz (y subcarpetas)
  - Convierte a FLAC con máxima calidad (sin pérdida)
  - Limpia el nombre del FLAC: "(1)" → "- 1"
  - FLAC queda en la misma carpeta del WAV
  - WAV original se mueve a _WAV_Backup manteniendo la estructura

Requisito: FFmpeg instalado y en el PATH

Uso:
  python wav_a_flac.py
"""

import os
import re
import shutil
import subprocess

# ============================================================
# CONFIGURACIÓN
# ============================================================
CARPETA_RAIZ   = r"D:\Música\IA Sounds"
CARPETA_BACKUP = r"D:\Música\IA Sounds\_WAV_Backup"
# ============================================================

def limpiar_nombre(nombre_sin_ext):
    """
    Convierte patrón (N) al final por - N
    Ejemplo: 'Rise and Conquer (1)' → 'Rise and Conquer - 1'
    """
    limpio = re.sub(r'\s*\((\d+)\)\s*$', r' - \1', nombre_sin_ext).strip()
    return limpio

def main():
    convertidos = 0
    errores     = []

    for raiz, _, archivos in os.walk(CARPETA_RAIZ):
        # Saltar la carpeta de backup
        if CARPETA_BACKUP in raiz:
            continue

        for archivo in archivos:
            if not archivo.lower().endswith('.wav'):
                continue

            ruta_wav      = os.path.join(raiz, archivo)
            nombre_sin_ext = os.path.splitext(archivo)[0]

            # Nombre limpio para el FLAC
            nombre_flac   = limpiar_nombre(nombre_sin_ext) + '.flac'
            ruta_flac     = os.path.join(raiz, nombre_flac)

            print(f"🔄 Convirtiendo: {archivo}")
            print(f"   → {nombre_flac}")

            # Convertir WAV → FLAC con FFmpeg (máxima calidad)
            resultado = subprocess.run(
                [
                    'ffmpeg',
                    '-i', ruta_wav,
                    '-compression_level', '12',
                    '-y',          # Sobrescribir si existe
                    ruta_flac
                ],
                capture_output=True,
                text=True
            )

            if resultado.returncode != 0:
                print(f"   ❌ Error al convertir: {archivo}")
                errores.append(archivo)
                continue

            # Mover WAV original al backup manteniendo estructura
            ruta_relativa  = os.path.relpath(ruta_wav, CARPETA_RAIZ)
            ruta_destino   = os.path.join(CARPETA_BACKUP, ruta_relativa)
            carpeta_destino = os.path.dirname(ruta_destino)

            os.makedirs(carpeta_destino, exist_ok=True)
            shutil.move(ruta_wav, ruta_destino)

            print(f"   ✅ WAV movido a backup")
            convertidos += 1

    print(f"\n✅ Convertidos: {convertidos}")
    if errores:
        print(f"❌ Errores ({len(errores)}):")
        for e in errores:
            print(f"   - {e}")

if __name__ == '__main__':
    main()
