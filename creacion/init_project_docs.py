import os
import sys
import argparse
from datetime import datetime
from pathlib import Path

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

# Las licencias disponibles deben existir físicamente en Core-Docs/templates/licenses.
LICENSES = {
    "1": ("MIT", "MIT.txt"),
    "2": ("GPL-3.0", "GPL-3.0-only.txt"),
}

def render_template(content, project_name, year, author, today_str, license_name):
    """Renderiza los valores comunes usados por documentos y reglas."""
    replacements = {
        "{{PROJECT_NAME}}": project_name,
        "{{YEAR}}": year,
        "{{AUTHOR}}": author,
        "{{DATE}}": today_str,
        "{{LICENSE}}": license_name,
    }
    for placeholder, value in replacements.items():
        content = content.replace(placeholder, value)
    return content


def write_text_safely(path, content, force=False):
    """Crea un archivo sin destruir contenido existente por defecto."""
    path = Path(path)
    if path.exists() and not force:
        print(f"  {YELLOW}↷{RESET} {GRAY}Conservado {path} (ya existe){RESET}")
        return "skipped"

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    action = "Actualizado" if force else "Creado"
    print(f"  {GREEN}✓{RESET} {GRAY}{action} {path}{RESET}")
    return "written"


def ensure_gitignore_entries(dest_dir):
    """Añade exclusiones temporales sin reemplazar el .gitignore actual."""
    gitignore_path = Path(dest_dir) / ".gitignore"
    existing = gitignore_path.read_text(encoding="utf-8") if gitignore_path.exists() else ""
    current_lines = {line.strip() for line in existing.splitlines()}
    missing = [entry for entry in ("/test/", "/scratch/") if entry not in current_lines]
    if not missing:
        print(f"  {GREEN}✓{RESET} {GRAY}.gitignore ya contiene /test/ y /scratch/{RESET}")
        return

    separator = "" if not existing or existing.endswith("\n") else "\n"
    updated = existing + separator + "\n# Archivos temporales de agentes\n" + "\n".join(missing) + "\n"
    gitignore_path.write_text(updated, encoding="utf-8")
    print(f"  {GREEN}✓{RESET} {GRAY}Actualizado .gitignore ({', '.join(missing)}){RESET}")

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
    parser.add_argument(
        "--license",
        choices=[license_info[0] for license_info in LICENSES.values()],
        help="Tipo de licencia disponible en Core Docs",
    )
    parser.add_argument("--force", action="store_true", help="Sobrescribe documentos y reglas existentes")
    parser.add_argument("--no-rules", action="store_true", help="No genera .agents/rules/base.md")
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

    license_name, license_template_filename = lic_info

    # Parámetros comunes
    author = "biglexj"
    year = str(datetime.now().year)
    today_str = datetime.now().strftime("%Y-%m-%d")

    print(f"\n{BLUE}🛠️  Configurando archivos para {WHITE}{project_name}{BLUE}...{RESET}")

    # La Documentación Core es la fuente oficial de todas las plantillas.
    # BIGLEX_CORE_DOCS permite usar otra ubicación sin modificar este script.
    workspace_dir = Path(__file__).resolve().parents[2]
    core_docs_dir = Path(
        os.environ.get("BIGLEX_CORE_DOCS", workspace_dir / "Core-Docs")
    ).resolve()
    templates_dir = core_docs_dir / "templates"

    if not templates_dir.is_dir():
        print(f"  {RED}✗ No se encontró la Documentación Core: {templates_dir}{RESET}")
        print(f"  {GRAY}Configura BIGLEX_CORE_DOCS si Core-Docs está en otra ubicación.{RESET}")
        return

    print(f"{CYAN}📚 Documentación Core: {WHITE}{templates_dir}{RESET}")

    files_to_copy = {
        "agent.md": templates_dir / "agents" / "agent.md",
        "ROADMAP.md": templates_dir / "documentation" / "ROADMAP.md",
        "RELEASE_NOTES.md": templates_dir / "documentation" / "RELEASE_NOTES.md",
        "RELEASE_MESSAGE.md": templates_dir / "documentation" / "RELEASE_MESSAGE.md",
    }
    
    # Asegurar que el directorio de destino exista
    os.makedirs(dest_dir, exist_ok=True)

    # Configurar exclusiones temporales sin destruir reglas existentes.
    ensure_gitignore_entries(dest_dir)

    # Preparar el flujo estándar de procesos sin crear un proceso ficticio.
    process_dir = Path(dest_dir) / "process"
    (process_dir / "active").mkdir(parents=True, exist_ok=True)
    (process_dir / "completed").mkdir(parents=True, exist_ok=True)
    (process_dir / "archive").mkdir(parents=True, exist_ok=True)

    process_readme_template = templates_dir / "process" / "PROCESS_README.md"
    if process_readme_template.is_file():
        process_readme_content = render_template(
            process_readme_template.read_text(encoding="utf-8"),
            project_name,
            year,
            author,
            today_str,
            license_name,
        )
        write_text_safely(process_dir / "README.md", process_readme_content, args.force)

    # Copiar los moldes de cada proceso sin reemplazar sus variables futuras.
    local_process_templates_dir = process_dir / "templates"
    for process_template_name in ("PLAN.md", "TASKS.md", "VALIDATION.md", "APPROVAL.md"):
        process_template_path = templates_dir / "process" / process_template_name
        if not process_template_path.is_file():
            print(f"  {RED}✗ Plantilla de proceso no encontrada: {process_template_path}{RESET}")
            continue

        process_template_content = process_template_path.read_text(encoding="utf-8")
        process_template_content = process_template_content.replace(
            "{{PROJECT_NAME}}", project_name
        )
        write_text_safely(
            local_process_templates_dir / process_template_name,
            process_template_content,
            args.force,
        )

    # Generar LICENSE exclusivamente desde Core Docs.
    license_template_path = templates_dir / "licenses" / license_template_filename
    if not license_template_path.is_file():
        print(f"  {RED}✗ Plantilla de licencia no encontrada: {license_template_path}{RESET}")
        return

    license_content = render_template(
        license_template_path.read_text(encoding="utf-8"),
        project_name,
        year,
        author,
        today_str,
        license_name,
    )

    license_path = os.path.join(dest_dir, "LICENSE")
    try:
        result = write_text_safely(license_path, license_content, args.force)
        if result == "written":
            print(f"    {GRAY}Licencia seleccionada: {license_name}{RESET}")
    except Exception as e:
        print(f"  {RED}✗ Error al crear LICENSE: {e}{RESET}")

    # MIT conserva su texto estándar; la atribución visible se solicita aparte.
    if license_name == "MIT":
        notice_template_path = templates_dir / "licenses" / "ATTRIBUTION-NOTICE.md"
        if notice_template_path.is_file():
            notice_content = render_template(
                notice_template_path.read_text(encoding="utf-8"),
                project_name,
                year,
                author,
                today_str,
                license_name,
            )
            write_text_safely(Path(dest_dir) / "NOTICE.md", notice_content, args.force)

    # Copiar y procesar plantillas
    for filename, src_path in files_to_copy.items():
        dest_path = os.path.join(dest_dir, filename)

        if not os.path.exists(src_path):
            print(f"  {RED}✗ Plantilla no encontrada: {src_path}{RESET}")
            continue

        try:
            with open(src_path, "r", encoding="utf-8") as f:
                content = f.read()

            content = render_template(content, project_name, year, author, today_str, license_name)
            write_text_safely(dest_path, content, args.force)
        except Exception as e:
            print(f"  {RED}✗ Error al crear {filename}: {e}{RESET}")

    # Materializar las instrucciones compartidas y la estructura del proyecto.
    if not args.no_rules:
        agent_template_path = templates_dir / "agents" / "agent.md"
        rules_path = os.path.join(dest_dir, ".agents", "rules", "base.md")
        try:
            with open(agent_template_path, "r", encoding="utf-8") as f:
                rule_content = render_template(
                    f.read(), project_name, year, author, today_str, license_name
                )
            rule_content = "---\ntrigger: always_on\n---\n\n" + rule_content.lstrip()
            write_text_safely(rules_path, rule_content, args.force)
        except Exception as e:
            print(f"  {RED}✗ Error al crear reglas del agente: {e}{RESET}")

        folder_structure_template_path = templates_dir / "project" / "folder_structure.md"
        folder_structure_rules_path = Path(dest_dir) / ".agents" / "rules" / "folder_structure.md"
        try:
            folder_structure_content = render_template(
                folder_structure_template_path.read_text(encoding="utf-8"),
                project_name,
                year,
                author,
                today_str,
                license_name,
            ).replace("{{PROJECT_ROOT}}", project_name)
            write_text_safely(
                folder_structure_rules_path,
                folder_structure_content,
                args.force,
            )
        except Exception as e:
            print(f"  {RED}✗ Error al crear la regla de estructura: {e}{RESET}")

        core_profile_template_path = templates_dir / "project" / "core_profile.md"
        core_profile_rules_path = Path(dest_dir) / ".agents" / "rules" / "core_profile.md"
        try:
            core_profile_content = render_template(
                core_profile_template_path.read_text(encoding="utf-8"),
                project_name,
                year,
                author,
                today_str,
                license_name,
            )
            write_text_safely(
                core_profile_rules_path,
                core_profile_content,
                args.force,
            )
        except Exception as e:
            print(f"  {RED}✗ Error al crear el perfil de Documentación Core: {e}{RESET}")

    print(f"\n{GREEN}✨ ¡Documentación de proyecto inicializada con éxito!{RESET}")
    print(f"{CYAN}📂 Ubicación: {WHITE}{dest_dir}{RESET}\n")

if __name__ == "__main__":
    main()
