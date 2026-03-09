import os
import shutil
import sys
import stat

def clonar_estructura(origen, destino, recursivo=True):
    """
    Clona la estructura de carpetas de 'origen' a 'destino'.
    recursivo: Si es True, clona toda la subestructura. Si es False, solo la raíz.
    """

    # Verificar que la carpeta origen existe
    if not os.path.exists(origen):
        print(f"[ERROR] La carpeta origen no existe: {origen}")
        sys.exit(1)

    # Si el destino ya existe, preguntar qué hacer
    if os.path.exists(destino):
        print(f"\n[AVISO] La carpeta destino ya existe: '{destino}'")
        print("¿Qué deseas hacer?")
        print("  [r] Reemplazar (BORRA TODO en el destino antes de empezar)")
        print("  [f] Fusionar   (Crea carpetas nuevas, CONSERVA archivos existentes)")
        print("  [c] Cancelar")
        respuesta = input("Selecciona una opción (r/f/c): ").strip().lower()

        if respuesta == "r":
            def remove_readonly(func, path, excinfo):
                """Limpia el atributo de solo lectura y reintenta la eliminación."""
                os.chmod(path, stat.S_IWRITE)
                func(path)

            shutil.rmtree(destino, onerror=remove_readonly)
            print(f"[INFO] Carpeta destino eliminada para reemplazo total.")
        elif respuesta == "f":
            print(f"[INFO] Modo fusión: Se conservarán los archivos existentes.")
        else:
            print("[INFO] Operación cancelada.")
            sys.exit(0)

    carpetas_creadas = 0

    if recursivo:
        # Recorrer toda la estructura de origen
        for ruta_actual, subcarpetas, archivos in os.walk(origen):
            # Calcular la ruta relativa desde el origen
            ruta_relativa = os.path.relpath(ruta_actual, origen)

            # Construir la ruta equivalente en el destino
            ruta_destino = os.path.join(destino, ruta_relativa)

            # Crear la carpeta en el destino
            os.makedirs(ruta_destino, exist_ok=True)
            carpetas_creadas += 1
            print(f"[OK] {ruta_relativa}")
    else:
        # Crear la carpeta base destino
        os.makedirs(destino, exist_ok=True)
        # Solo listar carpetas de primer nivel
        for item in os.listdir(origen):
            ruta_item = os.path.join(origen, item)
            if os.path.isdir(ruta_item):
                ruta_destino = os.path.join(destino, item)
                os.makedirs(ruta_destino, exist_ok=True)
                carpetas_creadas += 1
                print(f"[OK] {item}")

    print(f"\n✅ Listo. Se clonaron {carpetas_creadas} carpetas.")
    print(f"   Origen:  {origen}")
    print(f"   Destino: {destino}")
    print(f"   Modo:    {'Recursivo' if recursivo else 'Solo carpetas en raíz'}")


if __name__ == "__main__":
    # Uso directo desde terminal: python clonar_estructura.py <origen> <destino> [r/n]
    if len(sys.argv) >= 3:
        origen  = sys.argv[1]
        destino = sys.argv[2]
        recursivo = True
        if len(sys.argv) == 4:
            recursivo = sys.argv[3].lower() != 'n'
    else:
        # Si no se pasan argumentos, pedir interactivamente
        print("=== CLONADOR DE ESTRUCTURA DE CARPETAS ===\n")
        origen  = input("Ruta de la carpeta ORIGEN:  ").strip().strip('"')
        destino = input("Ruta de la carpeta DESTINO: ").strip().strip('"')
        ans = input("¿Deseas clonar subcarpetas recursivamente? (s/n): ").strip().lower()
        recursivo = ans == 's'

    clonar_estructura(origen, destino, recursivo)
