#!/bin/bash
# Enhanced Zsh installation script with automatic distribution detection
# Usage: curl -sSf https://your-domain.com/install-zsh.sh | bash

set -e

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}🐚 Instalando Zsh + Plugins - Setup Biglex${NC}"
echo "=========================================="

# Funciones
log_info() { echo -e "${GREEN}[INFO]${NC} $1"; }
log_warn() { echo -e "${YELLOW}[WARN]${NC} $1"; }
log_error() { echo -e "${RED}[ERROR]${NC} $1"; }

# Detectar distribución y gestor de paquetes
detect_distro() {
    if command -v pacman &> /dev/null; then
        echo "arch"
        PKG_UPDATE="sudo pacman -Sy"
        PKG_INSTALL="sudo pacman -S --needed --noconfirm"
    elif command -v apt &> /dev/null; then
        echo "debian"
        PKG_UPDATE="sudo apt update"
        PKG_INSTALL="sudo apt install -y"
    elif command -v zypper &> /dev/null; then
        echo "opensuse"
        PKG_UPDATE="sudo zypper refresh"
        PKG_INSTALL="sudo zypper install -y"
    elif command -v dnf &> /dev/null; then
        echo "fedora"
        PKG_UPDATE="sudo dnf check-update"
        PKG_INSTALL="sudo dnf install -y"
    else
        log_error "Distribución Linux no soportada"
        log_info "Soportado: Arch, Debian/Ubuntu, openSUSE, Fedora"
        exit 1
    fi
}

DISTRO=$(detect_distro)
log_info "Distribución detectada: $DISTRO (usando el gestor de paquetes correspondiente)"

# Instalar dependencias base
log_info "Instalando dependencias base: curl, git, zsh"
eval "$PKG_UPDATE"
eval "$PKG_INSTALL curl git zsh"

# Instalar Oh My Zsh
log_info "Instalando Oh My Zsh..."
sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)" "" --unattended || {
    log_warn "Oh My Zsh ya podría estar instalado o hubo un problema menor"
}

# Definir ubicación personalizada de Oh My Zsh
export ZSH="${ZSH:-$HOME/.oh-my-zsh}"
export ZSH_CUSTOM="${ZSH_CUSTOM:-$ZSH/custom}"

# Instalar plugins
log_info "Instalando plugins esenciales..."

# Función para instalar un plugin si no existe
install_plugin() {
    local repo_url=$1
    local plugin_name=$(basename "$repo_url" | sed 's/\.git$//')
    local target_dir="$ZSH_CUSTOM/plugins/$plugin_name"
    
    if [ -d "$target_dir" ]; then
        log_info "Plugin $plugin_name ya instalado, actualizando..."
        (cd "$target_dir" && git pull) || log_warn "No se pudo actualizar $plugin_name"
    else
        log_info "Instalando plugin: $plugin_name"
        git clone "$repo_url" "$target_dir"
    fi
}

# Lista de plugins a instalar
PLUGINS=(
    "https://github.com/zsh-users/zsh-autosuggestions"
    "https://github.com/zsh-users/zsh-syntax-highlighting"
    "https://github.com/zsh-users/zsh-completions"
    "https://github.com/zsh-users/zsh-history-substring-search"
)

for plugin in "${PLUGINS[@]}"; do
    install_plugin "$plugin"
done

# Configurar .zshrc
log_info "Configurando ~/.zshrc..."
# Backup
cp "$HOME/.zshrc" "$HOME/.zshrc.backup.$(date +%Y%m%d_%H%M%S)" 2>/dev/null || true

# Asegurar que existe .zshrc
if [ ! -f "$HOME/.zshrc" ]; then
    cp "$ZSH/templates/zshrc.zsh-template" "$HOME/.zshrc"
fi

# Activar plugins (más completos)
sed -i 's/^plugins=(.*/plugins=(git zsh-autosuggestions zsh-syntax-highlighting zsh-completions zsh-history-substring-search sudo extract web-search)/' "$HOME/.zshrc"

# Configurar tema
sed -i 's/^ZSH_THEME=".*"/ZSH_THEME="agnoster"/' "$HOME/.zshrc"

# Añadir aliases y configuraciones si no existen
if ! grep -q "### BIGLEX CONFIG" "$HOME/.zshrc"; then
    cat >> "$HOME/.zshrc" << 'EOF'

### BIGLEX CONFIG
# Aliases personalizados
alias ll='ls -la'
alias la='ls -la'
alias l='ls -la'
alias cls='clear'
alias ..='cd ..'
alias ...='cd ../..'
alias home='cd ~'
alias root='cd /'

# Git shortcuts
alias gs='git status'
alias ga='git add'
alias gc='git commit'
alias gp='git push'
alias gpl='git pull'
alias gst='git status'
alias gaa='git add --all'
alias gcm='git commit -m'
alias gps='git push'

# Sistema (según distribución)
if command -v pacman &> /dev/null; then
    alias update='sudo pacman -Syu'
elif command -v apt &> /dev/null; then
    alias update='sudo apt update && sudo apt upgrade -y'
elif command -v zypper &> /dev/null; then
    alias update='sudo zypper refresh && sudo zypper update -y'
elif command -v dnf &> /dev/null; then
    alias update='sudo dnf upgrade -y'
fi

# Otros aliases útiles
alias cls='clear'
alias df='df -h'
alias du='du -h'
alias free='free -h'
alias cat='bat' 2>/dev/null || echo "bat no instalado, usando cat normal"
alias ls='ls --color=auto' 2>/dev/null || echo "ls color no disponible"

# Funciones
take() { mkdir -p "$1" && cd "$1"; }
ex() {
    if [ -f "$1" ]; then
        case "$1" in
            *.tar.bz2)   tar xjf "$1"     ;;
            *.tar.gz)    tar xzf "$1"     ;;
            *.bz2)       bunzip2 "$1"     ;;
            *.rar)       unrar x "$1"     ;;
            *.gz)        gunzip "$1"      ;;
            *.tar)       tar xf "$1"      ;;
            *.tbz2)      tar xjf "$1"     ;;
            *.tgz)       tar xzf "$1"     ;;
            *.zip)       unzip "$1"       ;;
            *.Z)         uncompress "$1"  ;;
            *.7z)        7z x "$1"        ;;
            *)           echo "'$1' no se puede extraer con ex()" ;;
        esac
    else
        echo "'$1' no es un archivo válido"
    fi
}
### END BIGLEX CONFIG
EOF
fi

log_info "✅ Instalación completada!"
echo ""
echo -e "${YELLOW}📋 Pasos finales:${NC}"
echo "1. Ejecuta: chsh -s \$(which zsh)"
echo "2. Cierra y vuelve a abrir tu terminal"
echo "3. ¡Disfruta tu nuevo Zsh! 🚀"
echo ""
echo -e "${YELLOW}💡 Tips:${NC}"
echo "- Para cambiar el tema, edita ZSH_THEME en ~/.zshrc"
echo "- Temas populares: agnoster, powerlevel10k/powerlevel10k, robbyrussell"
echo "- Para instalar powerlevel10k: git clone --depth=1 https://github.com/romkatv/powerlevel10k.git \${ZSH_CUSTOM:-~\/.oh-my-zsh\/custom}/themes/powerlevel10k"