#!/bin/bash
# Dotfiles installation script for Arch Linux
# Terminal apps are installed as common dependencies for all modes

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# =============================================================================
# Helper Functions
# =============================================================================

print_header() {
    echo -e "\n${BLUE}=== $1 ===${NC}\n"
}

print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠ $1${NC}"
}

print_error() {
    echo -e "${RED}✗ $1${NC}"
}

install_packages() {
    local list_file="$1"
    if [ -f "$list_file" ]; then
        echo "Installing packages from $list_file..."
        grep -v '^#' "$list_file" | grep -v '^$' | tr '\n' ' ' | xargs yay -S --needed --noconfirm
        print_success "Packages installed from $list_file"
    else
        print_warning "File not found: $list_file"
    fi
}

setup_stow() {
    local target="$1"
    echo "Creating symlinks for $target with GNU Stow..."
    stow "$target" -v
    print_success "Symlinks created for $target"
}

setup_systemd() {
    echo "Setting up systemd units (auto-theme timer)..."
    setup_stow "systemd"
    print_success "Systemd units installed"
}

# =============================================================================
# Main Installation
# =============================================================================

print_header "Dotfiles Installation"

# Select installation type
echo "Select installation type:"
echo "  1) Terminal Apps Only (TTY usage, no compositor)"
echo "  2) LabWC (includes Terminal Apps)"
echo "  3) Niri (includes Terminal Apps)"
echo "  4) LabWC + Niri (includes Terminal Apps)"
echo "  5) Exit"
echo ""
read -p "Enter choice [1-5]: " INSTALL_CHOICE

case $INSTALL_CHOICE in
    1)
        MODE="terminal"
        print_header "Terminal Apps Installation (TTY Only)"
        ;;
    2)
        MODE="labwc"
        print_header "LabWC Installation"
        ;;
    3)
        MODE="niri"
        print_header "Niri Installation"
        ;;
    4)
        MODE="full"
        print_header "Full Installation (LabWC + Niri)"
        ;;
    5)
        print_header "Exit"
        echo "Installation cancelled."
        exit 0
        ;;
    *)
        print_error "Invalid choice. Exiting."
        exit 1
        ;;
esac

# Update system
print_header "System Update"
echo "Updating system packages..."
sudo pacman -Suy

# Install base development tools
print_header "Base Development Tools"
echo "Installing base development tools..."
sudo pacman -S --needed --noconfirm git base-devel
print_success "Base development tools installed"

# Install yay AUR helper
print_header "Yay AUR Helper"
if [ ! -d "$SCRIPT_DIR/yay" ]; then
    echo "Cloning yay from AUR..."
    git clone https://aur.archlinux.org/yay.git "$SCRIPT_DIR/yay"
fi
cd "$SCRIPT_DIR/yay" && makepkg -si --noconfirm
cd "$SCRIPT_DIR"
print_success "Yay installed"

# Install terminal apps (common dependencies - always installed)
print_header "Terminal Applications (Common Dependencies)"
install_packages "$SCRIPT_DIR/terminal-apps.lst"

# Install common applications (skip for terminal-only mode)
if [ "$MODE" != "terminal" ]; then
    print_header "Common Applications"
    install_packages "$SCRIPT_DIR/common-apps.lst"
fi

# Install compositor-specific packages
case $MODE in
    labwc)
        install_packages "$SCRIPT_DIR/labwc-apps.lst"
        ;;
    niri)
        install_packages "$SCRIPT_DIR/niri-apps.lst"
        ;;
    full)
        install_packages "$SCRIPT_DIR/labwc-apps.lst"
        install_packages "$SCRIPT_DIR/niri-apps.lst"
        ;;
esac

# Setup symlinks with Stow (skip for terminal-only mode)
if [ "$MODE" != "terminal" ]; then
    print_header "GNU Stow Symlinks"
    
    # Setup systemd units first (auto-theme timer)
    setup_systemd
    
    case $MODE in
        labwc)
            setup_stow "labwc"
            ;;
        niri)
            setup_stow "niri"
            ;;
        full)
            setup_stow "labwc"
            setup_stow "niri"
            ;;
    esac
fi

# Enable auto-theme timer (skip for terminal-only mode)
if [ "$MODE" != "terminal" ]; then
    print_header "Auto Theme Setup"
    systemctl --user daemon-reload
    systemctl --user enable --now auto-theme.timer
    print_success "Auto-theme timer enabled"
fi

# Final configuration
print_header "Final Configuration"
if [ "$MODE" != "terminal" ]; then
    echo "Reloading systemd user daemon..."
    systemctl --user daemon-reload
fi

# =============================================================================
# Completion
# =============================================================================

print_header "Installation Complete!"

echo -e "${GREEN}Installed Components:${NC}"
case $MODE in
    terminal)
        echo "  • Terminal applications (btop, neovim, zsh, lazygit, etc.)"
        echo "  • TTY-only usage (no Wayland compositor)"
        ;;
    labwc)
        echo "  • LabWC Wayland Compositor"
        echo "  • Terminal applications (btop, neovim, zsh, lazygit, etc.)"
        echo "  • Common applications (nautilus, blueman, mako, etc.)"
        echo "  • Auto-theme switcher (sunrise/sunset based)"
        ;;
    niri)
        echo "  • Niri Scrollable Wayland Compositor"
        echo "  • Terminal applications (btop, neovim, zsh, lazygit, etc.)"
        echo "  • Common applications (nautilus, blueman, mako, etc.)"
        echo "  • Auto-theme switcher (sunrise/sunset based)"
        ;;
    full)
        echo "  • LabWC Wayland Compositor"
        echo "  • Niri Scrollable Wayland Compositor"
        echo "  • Terminal applications (btop, neovim, zsh, lazygit, etc.)"
        echo "  • Common applications (nautilus, blueman, mako, etc.)"
        echo "  • Auto-theme switcher (sunrise/sunset based)"
        ;;
esac

echo ""
echo -e "${YELLOW}Next Steps:${NC}"
case $MODE in
    terminal)
        echo "  • Terminal apps are ready to use!"
        echo "  • Try: btop, lf, lazygit, nvim, zsh"
        ;;
    labwc)
        echo "  1. Enable display manager: sudo systemctl enable lightdm"
        echo "  2. Reboot or logout"
        echo "  3. Select LabWC session at login"
        echo "  4. Reload config with W-r"
        ;;
    niri)
        echo "  1. Set niri as default session (see README.md)"
        echo "  2. Reboot or logout"
        echo "  3. Select Niri session at login"
        ;;
    full)
        echo "  1. Enable display manager: sudo systemctl enable lightdm"
        echo "  2. Reboot or logout"
        echo "  3. Select LabWC or Niri session at login"
        ;;
esac

echo ""
echo -e "${YELLOW}Useful Commands:${NC}"
if [ "$MODE" != "terminal" ]; then
    echo "  • Check auto-theme timer: systemctl --user list-timers | grep auto-theme"
    echo "  • View auto-theme logs: journalctl --user -u auto-theme -f"
    echo "  • Reload compositor config: W-r"
else
    echo "  • Terminal apps: btop, lf, lazygit, nvim"
fi

echo ""
