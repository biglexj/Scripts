#!/bin/bash
# ~/Scripts/install-zsh.sh
# Enhanced Zsh installation script with automatic distribution detection

echo "🐚 Instalando Zsh + Plugins - Setup Biglex"
echo "=========================================="

# Detectar distribución
if command -v pacman &> /dev/null; then
    echo "🎯 Arch Linux detectado"
    sudo pacman -S --needed curl git zsh
elif command -v apt &> /dev/null; then
    echo "🎯 Debian/Ubuntu detectado"
    sudo apt update && sudo apt install -y curl git zsh
elif command -v zypper &> /dev/null; then
    echo "🎯 openSUSE/SUSE Linux Enterprise detectado"
    sudo zypper refresh && sudo zypper install -y curl git zsh
else
    echo "❌ Distribución no soportada"
    echo "Soportado: Arch, Debian/Ubuntu, openSUSE/SUSE"
    exit 1
fi

echo "📥 Instalando Oh My Zsh..."
sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)" "" --unattended

echo "🔌 Instalando plugins esenciales..."

# zsh-autosuggestions
git clone https://github.com/zsh-users/zsh-autosuggestions ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-autosuggestions

# zsh-syntax-highlighting  
git clone https://github.com/zsh-users/zsh-syntax-highlighting.git ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-syntax-highlighting

# zsh-completions
git clone https://github.com/zsh-users/zsh-completions ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-completions

echo "⚙️ Configurando plugins..."

# Backup
cp ~/.zshrc ~/.zshrc.backup.$(date +%Y%m%d)

# Activar plugins
sed -i 's/plugins=(git)/plugins=(git zsh-autosuggestions zsh-syntax-highlighting zsh-completions)/' ~/.zshrc

echo "🎨 Configurando tema (opcional)..."
# Cambiar tema a uno más moderno
sed -i 's/ZSH_THEME="robbyrussell"/ZSH_THEME="agnoster"/' ~/.zshrc

echo "✅ Instalación completada!"
echo ""
echo "📋 Pasos finales:"
echo "1. Ejecuta: chsh -s \$(which zsh)"
echo "2. Cierra y abre la terminal"
echo "3. ¡Disfruta tu nuevo Zsh! 🚀"