# Diccionario con carpetas madre y sus subcategorías
$estructura = @{
    "Sonidos de Transición - Movimiento" = @("Whoosh", "Swish", "Movimiento-rapido", "Deslizamientos", "Transiciones")
    "Efectos Digitales - Glitch"         = @("Glitch", "Errores-digitales", "Bits-Beeps", "Tecnologico")
    "Emociones - Ambientes"              = @("Triste", "Feliz", "Tenso", "Suspenso", "Epico", "Relajado")
    "Acción - Impacto"                   = @("Golpes", "Explosiones", "Choques", "Caidas", "Punetazos")
    "Fantasía - Sci-Fi"                  = @("Magia", "Laser", "Espacial", "Portal", "Hechizo")
    "Humanos - Reacciones"              = @("Voces-Reacciones", "Risa", "Gritos", "Suspiros", "Aplausos")
    "Naturaleza - Ambiente"             = @("Viento", "Lluvia", "Truenos", "Animales", "Ambiente-city", "Ambiente-bosque")
    "Objetos - Cosas"                   = @("Puertas", "Pasos", "Cadenas", "Cristales", "Metal-Madera")
    "Videojuegos - Retro"               = @("8-Bit", "Power-Up", "Daño", "UI-Menu", "Coins-Arcade")
    "Comedia - Cartoon"                = @("Comic", "Exagerado", "Trompeta-graciosa", "Saltos", "Burbujas")
    "Otros - Utiles"                   = @("Loopables", "Stingers", "Ambientes-largos", "One-Shots", "Silencios-Fades")
}

# Carpeta raíz donde se crearán
$base = "E:\Vídeos\Assets\Audio Efects"  # ← Cambia esta ruta

# Crear estructura de carpetas
foreach ($categoria in $estructura.Keys) {
    $rutaCategoria = Join-Path $base $categoria
    if (-not (Test-Path $rutaCategoria)) {
        New-Item -ItemType Directory -Path $rutaCategoria | Out-Null
        Write-Host "📁 Carpeta madre creada: $rutaCategoria"
    }

    foreach ($sub in $estructura[$categoria]) {
        $rutaSub = Join-Path $rutaCategoria $sub
        if (-not (Test-Path $rutaSub)) {
            New-Item -ItemType Directory -Path $rutaSub | Out-Null
            Write-Host "    📂 Subcarpeta creada: $rutaSub"
        }
    }
}
