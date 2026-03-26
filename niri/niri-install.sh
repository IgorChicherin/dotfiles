#!/bin/bash
# Niri installation script for Arch Linux

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=== Niri Installation ==="
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
echo "=== Setting up Auto Theme ==="
echo ""

# Create config directories
echo "Creating config directories..."
mkdir -p ~/.config/niri
mkdir -p ~/.config/systemd/user

# Copy auto-theme script
echo "Copying auto-theme script..."
cp "$SCRIPT_DIR/.config/niri/auto-theme.py" ~/.config/niri/auto-theme.py
chmod +x ~/.config/niri/auto-theme.py

# Copy systemd units
echo "Installing systemd units..."
cp "$SCRIPT_DIR/.config/systemd/user/auto-theme.service" ~/.config/systemd/user/
cp "$SCRIPT_DIR/.config/systemd/user/auto-theme.timer" ~/.config/systemd/user/

# Reload systemd and enable timer
echo "Enabling auto-theme timer..."
systemctl --user daemon-reload
systemctl --user enable auto-theme.timer
systemctl --user start auto-theme.timer

echo ""
echo "=== Installation Complete ==="
echo ""
echo "Auto theme switcher is now enabled!"
echo "It will automatically switch themes based on sunrise/sunset."
echo ""
echo "To check status: systemctl --user status auto-theme.timer"
echo "To view logs: journalctl --user -u auto-theme -f"
echo ""
