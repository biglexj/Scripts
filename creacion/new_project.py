import os
import re
import sys

# Colores ANSI para el estilo Biglex J
CYAN = "\033[96m"
YELLOW = "\033[93m"
GREEN = "\033[92m"
RED = "\033[91m"
MAGENTA = "\033[95m"
BLUE = "\033[94m"
GRAY = "\033[90m"
WHITE = "\033[97m"
RESET = "\033[0m"

def get_input(prompt, options=None):
    while True:
        print(f"{YELLOW}{prompt}{RESET}")
        if options:
            for key, val in options.items():
                print(f"  {GRAY}{key}) {val}{RESET}")
        
        val = input(f"\n{WHITE}Opción: {RESET}").strip()
        
        if options and val not in options:
            print(f"{RED}❌ Opción inválida{RESET}")
            continue
        return val

def main():
    # Detectar el disco base (por defecto D: o pasado por argumento)
    drive = "D:"
    if len(sys.argv) > 2 and sys.argv[1] == "--base":
        drive = sys.argv[2]

    # Banner de bienvenida
    print(f"\n{CYAN}╔" + "═" * 64 + "╗")
    print(f"║           🎬 CREAR NUEVO PROYECTO DE VIDEO                     ║")
    print(f"╚" + "═" * 64 + f"╝{RESET}\n")

    # Selección de Canal
    canales = {
        "1": "@biglexj",
        "2": "@ely-vtuber",
        "3": "@biglexjtema",
        "4": "@biglexlive",
        "5": "@biglexpe"
    }
    canal_opt = get_input("📺 Selecciona el canal:", canales)
    canal = canales[canal_opt]

    # Selección de Tipo
    tipos = {
        "1": "Video normal",
        "2": "Short"
    }
    tipo_opt = get_input("\n🎥 Tipo de video:", tipos)

    # Construcción de la ruta base
    base_path = os.path.join(drive, "Vídeos", "DaVinci Resolve", canal)
    if tipo_opt == "2":
        base_path = os.path.join(base_path, "Shorts")

    # Verificar existencia de la carpeta del canal
    if not os.path.exists(base_path):
        print(f"{RED}❌ La carpeta del canal no existe: {base_path}{RESET}")
        return

    # Escaneo para detectar el siguiente número de proyecto
    try:
        folders = [f for f in os.listdir(base_path) if os.path.isdir(os.path.join(base_path, f))]
    except Exception as e:
        print(f"{RED}❌ Error al leer la carpeta: {e}{RESET}")
        return

    last_number = 0
    for f in folders:
        match = re.match(r'^(\d+)\.', f)
        if match:
            try:
                num = int(match.group(1))
                if num > last_number:
                    last_number = num
            except ValueError:
                continue

    new_number = last_number + 1
    print(f"\n{GREEN}📝 Número asignado: {new_number}{RESET}")

    # Título del Proyecto
    titulo = input(f"\n{YELLOW}📌 Título del video: {RESET}").strip()
    if not titulo:
        print(f"{RED}❌ El título no puede estar vacío{RESET}")
        return

    # Creación del Proyecto
    project_name = f"{new_number}. {titulo}"
    project_path = os.path.join(base_path, project_name)

    try:
        # Crear carpetas estándar
        subfolders = ["Imágenes", "Videos", "Audio"]
        for sub in subfolders:
            os.makedirs(os.path.join(project_path, sub), exist_ok=True)
        
        print(f"\n{GREEN}✅ ¡Proyecto creado exitosamente!{RESET}")
        print(f"{CYAN}📁 Ruta: {project_path}{RESET}")
        print(f"\n{YELLOW}📂 Estructura creada:{RESET}")
        for sub in subfolders:
            print(f"  {GRAY}├── {sub}\\{RESET}")
            
    except Exception as e:
        print(f"\n{RED}❌ Error al crear el proyecto: {e}{RESET}")

if __name__ == "__main__":
    # Asegurar que el encoding sea UTF-8 para evitar problemas con emojis
    if sys.platform == 'win32':
        sys.stdin.reconfigure(encoding='utf-8')
        sys.stdout.reconfigure(encoding='utf-8')
    main()
