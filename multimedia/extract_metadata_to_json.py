import os
import json
import random
import string
import datetime
from mutagen.flac import FLAC
import logging
from collections import defaultdict
import re

# Configuración de logs
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

try:
    import librosa
    HAS_LIBROSA = True
except ImportError:
    HAS_LIBROSA = False
    logging.warning("Librosa no está instalado. El cálculo automático de BPM estará desactivado.")

# Directorio de origen y salida (Configurable)
TARGET_DIR = r"d:\Música\IA Sounds\Instrumental 3"
# Cambiar el nombre del archivo de salida según el folder
FOLDER_SUFFIX = "3" # O "3"
OUTPUT_FILE = fr"d:\Música\IA Sounds\metadata_instrumental_{FOLDER_SUFFIX}.json"

# Diccionario de variaciones semánticas para duplicados - Consolidadas (ES + EN)
TITLE_VARIATIONS = {
    # --- ESPAÑOL (Folder 1) ---
    "Amanecer Digital": [
        "Amanecer Digital", "Iluminación Digital", "Despertar Cibernético", "Aurora Virtual", "Alba Binaria", 
        "Resplandor Tecnológico", "Amanecer Digital (Extend)", "Iluminación Digital (Extend)", "Futuro Radiante", "Nacer del Bit"
    ],
    "Amor Inesperado": ["Amor Inesperado", "Romance Sorpresa", "Afecto Súbito", "Encuentro Furtivo"],
    "Bajo las Estrellas": ["Bajo las Estrellas", "Noche Estelar", "Manto Cósmico", "Velada Nocturna", "Cielo Infinito"],
    "Brilla y Comienza": ["Brilla y Comienza", "Resplandor Inicial", "Destello de Origen", "Luz Primera"],
    "Caminos de Amor": ["Caminos de Amor", "Rutas del Corazón", "Senderos de Pasión", "Travesía Romántica"],
    "Cielo de Neón": ["Cielo de Neón", "Firmamento Brillante", "Bóveda Luminosa", "Horizonte Eléctrico"],
    "Efectos de Tecnología": ["Efectos de Tecnología", "Impacto Cibernético", "Consecuencia Digital", "Ondas Binarias"],
    "La Ciudad Se Enciende": ["La Ciudad Se Enciende", "Metrópolis Iluminada", "Luces Urbanas", "Despertar de asfalto"],
    "Más Química": ["Más Química", "Conexión Profunda", "Fórmula Perfecta", "Reacción Vital"],
    "Otra Vez": ["Otra Vez", "Un Nuevo Intento", "Una Oportunidad Más", "Reinicio Constante"],
    "Reacciones en Cadena": ["Reacciones en Cadena", "Secuencia Imparable", "Efecto Dominó", "Cascada de Eventos"],
    "Recuerdos Eléctricos": ["Recuerdos Eléctricos", "Memorias de Neón", "Nostalgia Digital", "Ecos de Volts"],
    "San Valentín": ["San Valentín", "Flecha de Cupido", "Promesa Romántica", "Febrero Eterno", "Día Especial"],
    "Sinfonía de odio helada": ["Sinfonía de Odio Helada", "Melodía del Invierno", "Canto Gélido", "Acordes de Escarcha"],
    "Sueño en Tokio": [
        "Sueño en Tokio", "Noche en Shibuya", "Luces de Shinjuku", "Fantasía Nipona", "Sueño en Tokio (Extend)", 
        "Noche en Shibuya (Extend)", "Harajuku Neon", "Ginza Nocturna"
    ],
    "Te Besé al Amanecer": ["Te Besé al Amanecer", "Caricia Matutina", "Beso de Madrugada"],

    # --- INGLÉS (Folder 2 & 3) ---
    "Adrenaline Pulse": ["Adrenaline Pulse", "Heartbeat Rush", "Pulse of Energy", "Adrenaline Surge", "Fast Lane Rhythm"],
    "Blazing Horizon": ["Blazing Horizon", "Fiery Sunset", "Radiant Skyline", "Flaming Horizon", "Dawn of Fire"],
    "Blazing Resolve": ["Blazing Resolve", "Burning Determination", "Fiery Will", "Resolve Unbound", "Steadfast Spirit"],
    "Boardroom Elegance": ["Boardroom Elegance", "Corporate Grace", "Executive Style", "Polished Ambition", "The Suit Flow"],
    "Breaking the Silence": ["Breaking the Silence", "Shattered Quiet", "Voice of the Still", "Silence Breaker", "Echoing Call"],
    "Bright Ideas": ["Bright Ideas", "Spark of Genius", "Creative Flash", "Illuminated Minds", "The Idea Engine", "Neon Thoughts"],
    "By the Firelight": ["By the Firelight", "Hearthside Glow", "Whispers of Embers", "Fireside Memories", "Cozy Flame"],
    "Candy Carousel": ["Candy Carousel", "Sweet Rollercoaster", "Sugar Spin", "Chromatic Treat", "Pastel Ride"],
    "Candy Pixel Universe": ["Candy Pixel Universe", "Sugar Bit World", "Virtual Sweetness", "Pixel Candy Sky", "Retro Treat"],
    "City Lights Glow": ["City Lights Glow", "Urban Neon", "Metropoli Shine", "Nocturnal Cityscape", "Midnight Glow"],
    "Coastal Breeze Serenade": ["Coastal Breeze Serenade", "Ocean Whisper", "Seaside Breath", "Marine Melody", "Shoreline Softness"],
    "Coffee and Quiet": ["Coffee and Quiet", "Muted Morning", "Steam and Silence", "Slow Sip", "Café Solitude"],
    "Coffee and a Smile": ["Coffee and a Smile", "Cheerful Brew", "Morning Joy", "Caffeine Grin", "Roast & Relish"],
    "Concrete Jungle Anthem": ["Concrete Jungle Anthem", "Urban Echo", "Streetwise Vibration", "Asphalt Rhythm", "City Heartbeat"],
    "Crushing the Void": ["Crushing the Void", "Eclipsing Empty", "Void Breaker", "Darkness Shattered", "Final Frontier"],
    "Digital Dreams": ["Digital Dreams", "Cybernetic Vision", "Binary Sleep", "Virtual Reverie", "Bitwise Fantasy"],
    "Digital Lament": ["Digital Lament", "Electronic Sorrow", "Circuit Cry", "Cyber Mourning", "Technological Ethereal"],
    "Digital Revolution": ["Digital Revolution", "Silicon Rebellion", "Network Uprising", "Binary Upheaval", "Code Shift"],
    "Echoes of Thought": ["Echoes of Thought", "Mindful Resonance", "Silent Reflection", "Mental Echo", "Wisdom Waves"],
    "Echoes of the Horizon": ["Echoes of the Horizon", "Distant Calling", "Skyward Resonance", "Vast Whisper", "Infinite Echo"],
    "Echoes of the Quiet": ["Echoes of the Quiet", "Soft Stillness", "Peaceful Vibe", "Gentle Echo", "Silence Speaks"],
    "Electrify the Night": ["Electrify the Night", "Neon Current", "Shock of Dark", "High Voltage Night", "Electric Pulse"],
    "End of the Storm": ["End of the Storm", "After the Rain", "Calm Horizon", "Storm's Departure", "Sunshine Reborn"],
    "Eternal Descent": ["Eternal Descent", "Endless Downward", "Abyssal Fall", "Ageless Plunge", "Voidward Journey"],
    "Fading Lights": ["Fading Lights", "Dimming Glow", "Twilight Vanish", "Subtle Dark", "Waning Brightness"],
    "Falling Lights": ["Falling Lights", "Descending Stars", "Luminous Drop", "Gravity Glow", "Cascade of Light"],
    "Fresh Ideas Only": ["Fresh Ideas Only", "Pure Innovation", "New Wave Thinking", "Clean Concept", "The Origin Point", "Novel Spark"],
    "Funky Time Machine": ["Funky Time Machine", "Retro Groove Box", "Temporal Funk", "Disco Portal", "Groovy Warp"],
    "Heroes Arise": ["Heroes Arise", "Legend's Call", "Valiant Ascent", "Champions Awake", "Epic Onset"],
    "Meltdown Glow": ["Meltdown Glow", "Fused Radiance", "Nuclear Shine", "Molten Light", "Thermal Bloom"],
    "Midnight Cravings": ["Midnight Cravings", "Late Night Desire", "Shadow Hunger", "Lunar Urge", "Moonlit Want"],
    "Midnight Reverie": ["Midnight Reverie", "Lunar Dream", "Midnight Lullaby", "Nighttime Wonder", "Starlit Reflection"],
    "Midnight Windowpane": ["Midnight Windowpane", "Glass and Moon", "Night Glass", "Window to Stars", "Reflective Dark"],
    "Moonlight Whispers": ["Moonlight Whispers", "Lunar Secrets", "Shadow Breathe", "Crescent Murmur", "Silver Silence"],
    "Moonlit Scribbles": ["Moonlit Scribbles", "Lunar Notes", "Sketch of Stars", "Nocturnal Lines", "Silver Ink"],
    "Neon Dreams": ["Neon Dreams", "Vivid Cyber", "Luminous Sleep", "Glow Vision", "Fluorescent Fantasy"],
    "Neon Ghosts": ["Neon Ghosts", "Electronic Spirits", "Glowing Phantoms", "Spectral Circuits", "Ether Neons"],
    "Neon Nights": ["Neon Nights", "Electric Dark", "Cyan Skyline", "Magenta Night", "Neon Jungle"],
    "Neon Reverie": ["Neon Reverie", "Glowing Thought", "Fluorescent Dream", "High Contrast Mind", "Static Peace"],
    "Neon Runner": ["Neon Runner", "Cyber Dash", "Circuit Sprint", "Bitwise Racer", "Lightpath Scout"],
    "Neon to Nostalgia": ["Neon to Nostalgia", "Glow to Memory", "Retrograde Neon", "Pastel Recall", "Classic Luster"],
    "Pasture Light": ["Pasture Light", "Meadow Glow", "Fields of Dawn", "Rustic Shine", "Verdant Aura"],
    "Petals in the Rain": ["Petals in the Rain", "Wet Blooms", "Storm Blossom", "Floral Shower", "Droplet Petal"],
    "Pit of Fury": ["Pit of Fury", "Cavern of Rage", "Depths of Wrath", "Hellfire Core", "Unchained Abyss"],
    "Pixel Heart Arcade": ["Pixel Heart Arcade", "8-Bit Pulse", "Arcade Blood", "Retro Heartbeat", "Joystick Soul"],
    "Pixelated Dreams": ["Pixelated Dreams", "Low-Res Vision", "Square Fantasy", "Bitwise Sleep", "Gridwork Dream"],
    "Pixelated Quest": ["Pixelated Quest", "Tilemap Adventure", "Square Journey", "Sprite Mission", "8-Bit Odyssee"],
    "Pixelated Showdown": ["Pixelated Showdown", "Boss Fight Bit", "Grid Combat", "Low-Res Duel", "Arcade Clash"],
    "Rain On Old Textbooks": ["Rain On Old Textbooks", "Library Pluvi", "Dust and Droplets", "Ink Blur", "Stormy Study"],
    "Raindrops and Reverie": ["Raindrops and Reverie", "Patter of Dreams", "Pluvial Wonder", "Mist and Mind", "Soft Storm"],
    "Reach the Summit": ["Reach the Summit", "Peak Attainment", "Mountain Breath", "High Point", "Climber's Zenith"],
    "Rise and Conquer": ["Rise and Conquer", "Dominion Rising", "Victory Ascent", "The Takeover", "Mastery Dawn"],
    "Rise and Shine": ["Rise and Shine", "Morning Awake", "Golden Hours", "Daybreak Energy", "Luminous Start"],
    "Rise of the Brave": ["Rise of the Brave", "Courageous Ascent", "Valor Rising", "Heart of Steel", "Braveheart Day"],
    "Rising Shadows": ["Rising Shadows", "Shadowy Growth", "Umbra Ascent", "Darkness Expanding", "Twilight Creep"],
    "Ritual of the Void": ["Ritual of the Void", "Abyssal Rite", "Void Ceremony", "Dark Transmutation", "Infinite Ritual"],
    "Rooftop Reverie": ["Rooftop Reverie", "Skyline Dream", "High-Rise Calm", "Urban Solitude", "Top Floor View"],
    "Shatter the Sky": ["Shatter the Sky", "Skybreaker", "Heaven's Split", "Cloud Cracker", "Final Impact"],
    "Shattered Sky": ["Shattered Sky", "Broken Firmament", "Fragmented Blue", "Sky shards", "Celestial Fracture"],
    "Shattered Spires": ["Shattered Spires", "Broken Towers", "Ruined Peaks", "Fallen Zenith", "Castle Debris"],
    "Shining Skies": ["Shining Skies", "Radiant Heavens", "Luminous Cloud", "Pure Azure", "Solar Firmament"],
    "Spring Blossom": ["Spring Blossom", "Vernal Bloom", "Floral Rebirth", "Petal Awakening", "Gardens of May"],
    "Stadium to Bedroom Confession": ["Stadium to Bedroom Confession", "Crowd to Quiet", "Grand to Intimate", "Echoed Secret", "The Soft Reveal"],
    "Starry Goodbye": ["Starry Goodbye", "Celestial Farewell", "Interstellar Parting", "Astro Adieu", "Comet's End"],
    "Storm of Titans": ["Storm of Titans", "Colossal Tempest", "Giants in Rain", "Titan's Thunder", "Epic Gale"],
    "The Eternal Flame": ["The Eternal Flame", "Ageless Torch", "Everlasting Burn", "Immortal Fire", "Infinity Blaze"],
    "Through the Static": ["Through the Static", "Noise Piercer", "Beyond Interference", "Signal Found", "Clarity Peak"],
    "Ultimate Showdown": ["Ultimate Showdown", "Final Battle", "Supreme Clash", "Zenith Duel", "The Last Stand"],
    "Unity in Motion": ["Unity in Motion", "Synchronized Flow", "Collective Speed", "Haromnic Movement", "The Grand Union"],
    "Velvet Steam": ["Velvet Steam", "Soft Vapor", "Silk Mist", "Sleek Haze", "Cloud of Comfort"],
    "Whispers in the Wind": ["Whispers in the Wind", "Aeolian Secrets", "Airy Murmurs", "Gale Breath", "Breezy Call"],
    "Whispers of the Horizon": ["Whispers of the Horizon", "Skyline Secrets", "Distant Murmurs", "Vast Calling", "Edge of Earth"]
}

def generate_slug(length=10):
    # ... (misma función)
    """Genera un slug aleatorio de caracteres alfanuméricos."""
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

def get_bpm(file_path):
    """Intenta detectar el BPM del archivo usando librosa."""
    if not HAS_LIBROSA:
        return 0
    
    try:
        logging.info(f"   ⏳ Calculando BPM para: {os.path.basename(file_path)}...")
        y, sr = librosa.load(file_path)
        tempo, _ = librosa.beat.beat_track(y=y, sr=sr)
        if isinstance(tempo, (list, tuple, bytes, bytearray)):
            return int(tempo[0])
        return int(tempo)
    except Exception as e:
        logging.error(f"   ❌ Error calculando BPM: {e}")
        return 0

def clean_title(filename):
    """Limpia el nombre de archivo para encontrar el título base (agrupando variaciones)."""
    base = os.path.splitext(filename)[0]
    # 1. Quitar mención de "_undo" si existe
    base = base.replace("_undo", "").strip()
    # 2. Quitar números finales (ej: "Song 2", "Song - 1")
    base = re.sub(r'[\s-]*\d+$', '', base).strip()
    # 3. Quitar "(Extend)" para agrupar con el original
    base = re.sub(r'\s*\(Extend\)', '', base, flags=re.IGNORECASE).strip()
    return base

def extract_metadata():
    if not os.path.exists(TARGET_DIR):
        logging.error(f"Directorio no encontrado: {TARGET_DIR}")
        return

    # Listar todos los FLAC en la raíz
    all_files = [f for f in os.listdir(TARGET_DIR) if f.lower().endswith('.flac') and os.path.isfile(os.path.join(TARGET_DIR, f))]
    logging.info(f"Encontrados {len(all_files)} archivos FLAC.")

    # 1. Leer metadatos básicos de todos para agrupar
    file_data = []
    for filename in all_files:
        path = os.path.join(TARGET_DIR, filename)
        try:
            audio = FLAC(path)
            album = audio.get("album", [""])[0]
            title = audio.get("title", [""])[0]
            artist = audio.get("artist", [""])[0]
            genre = audio.get("genre", [""])[0]
            
            bpm_tag = audio.get("bpm", ["0"])[0]
            try:
                bpm = int(float(bpm_tag))
            except ValueError:
                bpm = 0
                
            file_data.append({
                "filename": filename,
                "path": path,
                "album_tag": album if album else clean_title(filename),
                "title_tag": title,
                "artist": artist,
                "genre": genre,
                "bpm": bpm
            })
        except Exception as e:
            logging.error(f"Error leyendo {filename}: {e}")

    # 2. Agrupar por Album
    groups = defaultdict(list)
    for item in file_data:
        groups[item["album_tag"]].append(item)

    results = []
    now_iso = datetime.datetime.now(datetime.timezone.utc).isoformat().replace("+00:00", ".00000+00:00")
    
    global_id = 1
    # Ordenar grupos por nombre para consistencia
    for album_name in sorted(groups.keys()):
        group_items = groups[album_name]
        
        # 3. Ordenar dentro del grupo: El que tiene el nombre del album como titulo va primero
        def group_sort_key(item):
            # Priorizar si el título (actual o previo) coincide con el album
            is_base = 0 if item["title_tag"].lower() == album_name.lower() or os.path.splitext(item["filename"])[0].lower() == album_name.lower() else 1
            return (is_base, item["filename"].lower())
        
        group_items.sort(key=group_sort_key)
        
        # 4. Asignar títulos únicos y track_count
        for idx, item in enumerate(group_items):
            # Asignar título de variación único por grupo
            if album_name in TITLE_VARIATIONS and idx < len(TITLE_VARIATIONS[album_name]):
                final_title = TITLE_VARIATIONS[album_name][idx]
            else:
                final_title = f"{album_name} (Alt {idx})" if idx > 0 else album_name

            # Si el BPM es 0, intentar calcularlo
            bpm = item["bpm"]
            if bpm <= 0:
                bpm = get_bpm(item["path"])

            res_item = {
                "id": global_id,
                "created_at": now_iso,
                "updated_at": now_iso,
                "slug": generate_slug(),
                "title": final_title,
                "artist": item["artist"],
                "album": album_name,
                "genre": item["genre"],
                "bpm": bpm,
                "mood": "",
                "audio_src": "",
                "cover_url": "",
                "audio_origin": "",
                "image_origin": "",
                "youtube_id": None,
                "thumbnail_src": None,
                "prices": {"PEN": 5, "USD": 2},
                "track_count": idx + 1,
                "license": "Standard",
                "source_type": True,
                "tags": [""],
                "release_date": "2024-05-30T00:00:00+00:00",
                "patreon_avi": True,
                "patreon_link": None,
                "featured": False,
                "active": True
            }
            results.append(res_item)
            global_id += 1

    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=4, ensure_ascii=False)
    
    logging.info(f"✨ Proceso completado. Archivo generado con títulos y pistas únicas: {OUTPUT_FILE}")

if __name__ == "__main__":
    extract_metadata()
