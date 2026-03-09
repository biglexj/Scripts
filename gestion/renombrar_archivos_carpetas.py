import os
import sys

# ============================================================
#  FORMATOS DISPONIBLES
#  1. Title Case      → Primera Letra De Cada Palabra En Mayúscula
#  2. UPPER CASE      → TODAS EN MAYÚSCULA
#  3. lower case      → todas en minúscula
#  4. Sentence case   → Solo la primera letra mayúscula
#  5. PascalCase      → PrimerLetraDeCadaPalabraSinEspacios
#  6. camelCase       → primerLetraMinusculaRestantesMayúscula
#  7. snake_case      → palabras_unidas_con_guion_bajo
#  8. kebab-case      → palabras-unidas-con-guion
# ============================================================

def aplicar_formato(nombre, formato):
    if formato == "1":   # Title Case
        return nombre.title()

    elif formato == "2": # UPPER CASE
        return nombre.upper()

    elif formato == "3": # lower case
        return nombre.lower()

    elif formato == "4": # Sentence case
        return nombre.capitalize()

    elif formato == "5": # PascalCase
        palabras = nombre.replace("-", " ").replace("_", " ").split()
        return "".join(p.capitalize() for p in palabras)

    elif formato == "6": # camelCase
        palabras = nombre.replace("-", " ").replace("_", " ").split()
        if not palabras:
            return nombre
        return palabras[0].lower() + "".join(p.capitalize() for p in palabras[1:])

    elif formato == "7": # snake_case
        return nombre.replace("-", " ").replace("_", " ").lower().replace(" ", "_")

    elif formato == "8": # kebab-case
        return nombre.replace("_", " ").lower().replace(" ", "-")

    else:
        return nombre


def renombrar_elementos(raiz, formato, profundidad_max=None, simular=False, modo="carpetas"):
    """
    Renombra elementos dentro de 'raiz' con el formato elegido.
    - modo: 'carpetas' | 'archivos' | 'ambos'
    - profundidad_max: None = sin límite | 1 = solo nivel raíz | 2 = dos niveles, etc.
    - simular: True = solo muestra cambios sin aplicarlos (dry run)
    """

    cambios    = 0
    sin_cambio = 0
    errores    = 0

    procesar_carpetas = modo in ("carpetas", "ambos")
    procesar_archivos = modo in ("archivos", "ambos")

    # os.walk de abajo hacia arriba para no romper rutas al renombrar
    for ruta_actual, subcarpetas, archivos in os.walk(raiz, topdown=False):

        # Calcular profundidad relativa
        relativa    = os.path.relpath(ruta_actual, raiz)
        profundidad = 0 if relativa == "." else len(relativa.split(os.sep))

        # ── ARCHIVOS ──────────────────────────────────────────
        if procesar_archivos:
            for archivo in archivos:
                nombre_sin_ext, ext = os.path.splitext(archivo)
                nombre_nuevo_sin_ext = aplicar_formato(nombre_sin_ext, formato)
                nombre_nuevo         = nombre_nuevo_sin_ext + ext  # conservar extensión

                if archivo == nombre_nuevo:
                    sin_cambio += 1
                    continue

                ruta_vieja = os.path.join(ruta_actual, archivo)
                ruta_nueva = os.path.join(ruta_actual, nombre_nuevo)

                if simular:
                    print(f"[SIM archivo]  '{archivo}'  →  '{nombre_nuevo}'")
                    cambios += 1
                else:
                    try:
                        os.rename(ruta_vieja, ruta_nueva)
                        print(f"[OK archivo]   '{archivo}'  →  '{nombre_nuevo}'")
                        cambios += 1
                    except Exception as e:
                        print(f"[ERR archivo]  '{archivo}' — {e}")
                        errores += 1

        # ── CARPETAS ──────────────────────────────────────────
        if procesar_carpetas:

            # Saltar la carpeta raíz principal
            if relativa == ".":
                continue

            # Respetar límite de profundidad
            if profundidad_max is not None and profundidad > profundidad_max:
                continue

            nombre_actual = os.path.basename(ruta_actual)
            nombre_nuevo  = aplicar_formato(nombre_actual, formato)

            if nombre_actual == nombre_nuevo:
                sin_cambio += 1
                continue

            ruta_padre = os.path.dirname(ruta_actual)
            ruta_nueva = os.path.join(ruta_padre, nombre_nuevo)

            if simular:
                print(f"[SIM carpeta]  '{nombre_actual}'  →  '{nombre_nuevo}'")
                cambios += 1
            else:
                try:
                    os.rename(ruta_actual, ruta_nueva)
                    print(f"[OK carpeta]   '{nombre_actual}'  →  '{nombre_nuevo}'")
                    cambios += 1
                except Exception as e:
                    print(f"[ERR carpeta]  '{nombre_actual}' — {e}")
                    errores += 1

    print(f"\n{'[SIMULACIÓN]' if simular else '[RESULTADO]'}")
    print(f"  Renombrados : {cambios}")
    print(f"  Sin cambio  : {sin_cambio}")
    if errores:
        print(f"  Errores     : {errores}")


def mostrar_menu():
    print("""
╔══════════════════════════════════════════════╗
║      RENOMBRADOR DE ARCHIVOS / CARPETAS v1.1 ║
╚══════════════════════════════════════════════╝

FORMATOS DISPONIBLES:
  1 → Title Case      (Primera Letra De Cada Palabra)
  2 → UPPER CASE      (TODAS EN MAYÚSCULA)
  3 → lower case      (todas en minúscula)
  4 → Sentence case   (Solo la primera letra)
  5 → PascalCase      (SinEspaciosPrimeraLetraMayúscula)
  6 → camelCase       (sinEspaciosPrimeraPalabraMinúscula)
  7 → snake_case      (palabras_con_guion_bajo)
  8 → kebab-case      (palabras-con-guion)
""")


def main():
    mostrar_menu()

    # Ruta
    ruta = input("Ruta de la carpeta a procesar: ").strip().strip('"')
    if not os.path.exists(ruta):
        print(f"[ERROR] La ruta no existe: {ruta}")
        sys.exit(1)

    # Elementos a procesar: carpetas, archivos o ambos
    print("Elementos a procesar:")
    print("  1 → Solo carpetas")
    print("  2 → Solo archivos")
    print("  3 → Ambos (carpetas y archivos)")
    modo_input = input("Opción (1/2/3): ").strip()
    modos      = {"1": "carpetas", "2": "archivos", "3": "ambos"}
    if modo_input not in modos:
        print("[ERROR] Opción inválida.")
        sys.exit(1)
    modo = modos[modo_input]

    # Formato
    formato = input("\nElige el formato (1-8): ").strip()
    if formato not in [str(i) for i in range(1, 9)]:
        print("[ERROR] Opción inválida.")
        sys.exit(1)

    # Profundidad
    print("\nProfundidad de renombrado:")
    print("  0 → Solo el nivel raíz")
    print("  1 → Raíz + 1 nivel de subcarpetas")
    print("  N → Hasta N niveles")
    print("  [Enter] → Sin límite (todas las subcarpetas)")
    prof_input = input("Profundidad (o Enter para sin límite): ").strip()
    profundidad_max = int(prof_input) if prof_input.isdigit() else None

    # Simulación
    sim_input = input("\n¿Simular primero sin aplicar cambios? (s/n): ").strip().lower()
    simular   = sim_input == "s"

    print(f"\n{'='*50}")
    if simular:
        print("[MODO SIMULACIÓN — No se aplicará ningún cambio]\n")

    renombrar_elementos(ruta, formato, profundidad_max, simular, modo)

    # Si fue simulación, ofrecer aplicar
    if simular:
        aplicar = input("\n¿Aplicar los cambios reales ahora? (s/n): ").strip().lower()
        if aplicar == "s":
            print(f"\n{'='*50}")
            renombrar_elementos(ruta, formato, profundidad_max, simular=False, modo=modo)
        else:
            print("[INFO] No se aplicó ningún cambio.")


if __name__ == "__main__":
    main()
