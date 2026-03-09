import os
import sys

# Diccionario de opciones de carpetas
OPCIONES_CARPETAS = {
    "1":  "Assets",
    "2":  "Proyecto",
    "3":  "Render",
    "4":  "Backup",
    "5":  "IMG",
    "6":  "Videos",
    "7":  "Guion",
    "8":  "Miniatura",
    "9":  "Cover",
    "10": "Documentación",
    "11": "Referencias"
}

def mostrar_menu():
    print("\n" + "="*45)
    print("      SCREATING POWER-UP: SUBCARPETAS v1.4")
    print("="*45)
    print("Selecciona las carpetas que deseas crear:")
    for key, valor in sorted(OPCIONES_CARPETAS.items(), key=lambda x: int(x[0])):
        print(f"  {key.rjust(2)} -> {valor}")
    print("="*45)
    print("Ingresa los números separados por espacio (ej: 1 2 5)")
    print("Presiona Enter para usar las básicas (1 y 2)")
    
    seleccion = input("\nOpción(es): ").strip()
    
    if not seleccion:
        return ["Assets", "Proyecto"]
    
    indices = seleccion.split()
    carpetas_elegidas = []
    
    for idx in indices:
        if idx in OPCIONES_CARPETAS:
            carpetas_elegidas.append(OPCIONES_CARPETAS[idx])
        else:
            print(f"⚠️  Opción '{idx}' ignorada (inválida)")
            
    return list(set(carpetas_elegidas)) if carpetas_elegidas else ["Assets", "Proyecto"]

def crear_subcarpetas_dinamicas(ruta_raiz, carpetas_a_crear):
    """
    Recorre las carpetas en ruta_raiz y crea las seleccionadas dentro.
    """
    if not os.path.exists(ruta_raiz):
        print(f"[ERROR] La ruta no existe: {ruta_raiz}")
        sys.exit(1)

    print(f"\n🚀 Iniciando en: {ruta_raiz}")
    print(f"📂 Carpetas a crear: {', '.join(carpetas_a_crear)}\n")
    
    contador_carpetas = 0
    subcarpetas_creadas = 0

    try:
        items = os.listdir(ruta_raiz)
    except Exception as e:
        print(f"[ERROR] No se pudo leer la carpeta: {e}")
        sys.exit(1)

    for item in items:
        ruta_item = os.path.join(ruta_raiz, item)
        
        if os.path.isdir(ruta_item):
            if item.startswith('.'):
                continue
                
            contador_carpetas += 1
            print(f"📁 Root: {item}")
            
            for sub in carpetas_a_crear:
                ruta_sub = os.path.join(ruta_item, sub)
                if not os.path.exists(ruta_sub):
                    try:
                        os.makedirs(ruta_sub)
                        print(f"    ✅ + {sub}")
                        subcarpetas_creadas += 1
                    except Exception as e:
                        print(f"    ❌ ! {sub}: {e}")
                else:
                    print(f"    ℹ️   {sub} (ya existe)")

    print(f"\n" + "-"*45)
    print(f"✅ FINALIZADO")
    print(f"Carpetas base procesadas: {contador_carpetas}")
    print(f"Nuevas subcarpetas creadas: {subcarpetas_creadas}")
    print("-"*45)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        ruta = sys.argv[1].strip('"')
    else:
        print("=== CREADOR DE SUBCARPETAS DINÁMICO ===")
        ruta = input("Introduce la ruta de la carpeta raíz: ").strip().strip('"')
    
    if not os.path.isdir(ruta):
        print(f"[ERROR] '{ruta}' no es un directorio válido.")
        sys.exit(1)
        
    carpetas = mostrar_menu()
    crear_subcarpetas_dinamicas(ruta, carpetas)
