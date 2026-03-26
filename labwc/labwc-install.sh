#!/bin/bash
# LabWC installation script using GNU Stow

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=== LabWC Installation ==="
echo ""

# Update system and install base dependencies
echo "Updating system..."
sudo pacman -Suy

echo ""
echo "Installing base development tools..."
sudo pacman -S --needed --noconfirm git base-devel

echo ""
echo "Installing yay AUR helper..."
if [ ! -d "yay" ]; then
    git clone https://aur.archlinux.org/yay.git
fi
cd yay && makepkg -si
cd ..

echo ""
echo "Installing terminal apps..."
cat terminal-apps.lst | tr '\n' ' ' | xargs yay -S --needed --noconfirm --asdeps

echo ""
echo "Installing additional apps..."
cat apps.lst | tr '\n' ' ' | xargs yay -S --needed --noconfirm --asdeps

echo ""
echo "Creating symlinks with stow..."

# Use stow to create symlinks
cd "$SCRIPT_DIR/.."
stow labwc -v

echo ""
echo "Enabling auto-theme timer..."
systemctl --user daemon-reload
systemctl --user enable --now auto-theme.timer

echo ""
echo "=== Installation Complete ==="
echo ""
echo "Reload LabWC config with W-r or restart LabWC"
echo "Check timer status: systemctl --user list-timers | grep auto-theme"
echo ""
