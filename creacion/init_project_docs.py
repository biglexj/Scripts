import os
import sys
import argparse
from datetime import datetime

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

# Textos estándar de Licencia
MIT_LICENSE = """MIT License

Copyright (c) {year} {author}

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

APACHE_LICENSE = """                                 Apache License
                           Version 2.0, January 2004
                        http://www.apache.org/licenses/

   TERMS AND CONDITIONS FOR USE, REPRODUCTION, AND DISTRIBUTION

   1. Definitions.
      "License" shall mean the terms and conditions for use, reproduction,
      and distribution as defined by Sections 1 through 9 of this document.
      "Licensor" shall mean the copyright owner or entity authorized by
      the copyright owner that is granting the License.
      ... [Contenido simplificado de Apache 2.0] ...
      
   Copyright {year} {author}

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
"""

GPL_LICENSE = """GNU GENERAL PUBLIC LICENSE
Version 3, 29 June 2007

Copyright (C) {year} {author}
Everyone is permitted to copy and distribute verbatim copies
of this license document, but changing it is not allowed.

Preamble
The GNU General Public License is a free, copyleft license for
software and other kinds of works.
... [Contenido simplificado de GPL 3.0] ...
"""

PROPRIETARY_LICENSE = """Copyright (c) {year} {author}. Todos los derechos reservados.

Queda estrictamente prohibida la reproducción, distribución, comunicación pública
o transformación de esta obra bajo cualquier formato o medio sin autorización 
expresa por escrito de {author}.

Este software se proporciona "tal cual", sin garantías de ningún tipo.
"""

LICENSES = {
    "1": ("MIT", MIT_LICENSE),
    "2": ("Apache-2.0", APACHE_LICENSE),
    "3": ("GPL-3.0", GPL_LICENSE),
    "4": ("Propietaria", PROPRIETARY_LICENSE)
}

def get_input(prompt, default=None, options=None):
    while True:
        suffix = f" [{default}]" if default else ""
        print(f"{YELLOW}{prompt}{suffix}{RESET}")
        if options:
            for key, val in options.items():
                print(f"  {GRAY}{key}) {val[0]}{RESET}")
        
        val = input(f"\n{WHITE}Opción/Valor: {RESET}").strip()
        
        if not val and default:
            return default
        
        if options:
            if val not in options:
                print(f"{RED}❌ Opción inválida. Intente de nuevo.{RESET}")
                continue
            return options[val]
            
        if not val:
            print(f"{RED}❌ El valor no puede estar vacío.{RESET}")
            continue
            
        return val

def main():
    parser = argparse.ArgumentParser(description="Inicializa documentos de gestión y reglas de agente en un proyecto.")
    parser.add_argument("--name", help="Nombre del proyecto")
    parser.add_argument("--dir", help="Directorio de destino (por defecto el actual)")
    parser.add_argument("--license", choices=["MIT", "Apache-2.0", "GPL-3.0", "Propietaria"], help="Tipo de licencia")
    args = parser.parse_args()

    # Limpiar argumentos de comillas externas que puedan venir de la consola
    if args.name:
        args.name = args.name.strip("'\"")
    if args.dir:
        args.dir = args.dir.strip("'\"")
    if args.license:
        args.license = args.license.strip("'\"")

    # Configuración de codificación UTF-8 para consola en Windows
    if sys.platform == 'win32':
        sys.stdin.reconfigure(encoding='utf-8')
        sys.stdout.reconfigure(encoding='utf-8')

    # Banner
    print(f"\n{CYAN}╔" + "═" * 64 + "╗")
    print(f"║           🤖 INICIALIZADOR DE DOCUMENTOS DE PROYECTO           ║")
    print(f"╚" + "═" * 64 + f"╝{RESET}\n")

    # 1. Directorio de destino
    dest_dir = args.dir
    if not dest_dir:
        dest_dir = os.getcwd()
    dest_dir = os.path.abspath(dest_dir)
    print(f"{CYAN}📁 Directorio destino: {WHITE}{dest_dir}{RESET}")

    # 2. Nombre del proyecto
    project_name = args.name
    if not project_name:
        default_name = os.path.basename(dest_dir)
        project_name = get_input("📌 Nombre del proyecto", default=default_name)

    # 3. Licencia
    lic_info = None
    if args.license:
        for k, v in LICENSES.items():
            if v[0].lower() == args.license.lower():
                lic_info = v
                break
    
    if not lic_info:
        lic_info = get_input("📜 Selecciona el tipo de licencia:", default=LICENSES["1"], options=LICENSES)

    license_name, license_template = lic_info

    # Parámetros comunes
    author = "biglexj"
    year = str(datetime.now().year)
    today_str = datetime.now().strftime("%Y-%m-%d")

    print(f"\n{BLUE}🛠️  Configurando archivos para {WHITE}{project_name}{BLUE}...{RESET}")

    # Definir rutas de origen y destino
    script_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    templates_dir = os.path.join(script_dir, "templates")

    files_to_copy = ["agent.md", "ROADMAP.md", "RELEASE_NOTES.md", "RELEASE_MESSAGE.md"]
    
    # Asegurar que el directorio de destino exista
    os.makedirs(dest_dir, exist_ok=True)

    # Generar LICENSE
    license_content = license_template.format(year=year, author=author)
    license_path = os.path.join(dest_dir, "LICENSE")
    try:
        with open(license_path, "w", encoding="utf-8") as f:
            f.write(license_content)
        print(f"  {GREEN}✓{RESET} {GRAY}Creado LICENSE ({license_name}){RESET}")
    except Exception as e:
        print(f"  {RED}✗ Error al crear LICENSE: {e}{RESET}")

    # Copiar y procesar plantillas
    for filename in files_to_copy:
        src_path = os.path.join(templates_dir, filename)
        dest_path = os.path.join(dest_dir, filename)

        if not os.path.exists(src_path):
            print(f"  {RED}✗ Plantilla no encontrada: {src_path}{RESET}")
            continue

        try:
            with open(src_path, "r", encoding="utf-8") as f:
                content = f.read()

            # Reemplazar placeholders
            content = content.replace("{{PROJECT_NAME}}", project_name)
            content = content.replace("{{YEAR}}", year)
            content = content.replace("{{AUTHOR}}", author)
            content = content.replace("{{DATE}}", today_str)
            content = content.replace("{{LICENSE}}", license_name)

            with open(dest_path, "w", encoding="utf-8") as f:
                f.write(content)
            
            print(f"  {GREEN}✓{RESET} {GRAY}Creado {filename}{RESET}")
        except Exception as e:
            print(f"  {RED}✗ Error al crear {filename}: {e}{RESET}")

    print(f"\n{GREEN}✨ ¡Documentación de proyecto inicializada con éxito!{RESET}")
    print(f"{CYAN}📂 Ubicación: {WHITE}{dest_dir}{RESET}\n")

if __name__ == "__main__":
    main()
