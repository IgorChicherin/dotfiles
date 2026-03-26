# Dotfiles

Personal dotfiles for Arch Linux with Wayland compositors.

## Components

| Component | Description |
|-----------|-------------|
| `labwc` | LabWC window manager with DMS integration and auto-theme |
| `niri` | Niri scrollable Wayland compositor |
| `wezterm` | WezTerm terminal with auto theme switching |
| `zsh` | ZSH with Oh My Zsh |
| `nvim` | Neovim configuration |
| `tmux` | Tmux terminal multiplexer |
| `kanata` | Keyboard remapping with Kanata |
| `slick-greeter` | LightDM greeter theme |
| `wallpapers` | Wallpaper collection |

## Quick Start

### Prerequisites

```bash
# Base development tools
sudo pacman -Suy && sudo pacman -S --needed --noconfirm git base-devel

# AUR helper (yay)
git clone https://aur.archlinux.org/yay.git
cd yay && makepkg -si
cd ..
```

### Installation

Each component has its own install script:

```bash
# LabWC (with auto-theme)
cd labwc && ./labwc-install.sh

# Niri
cd niri && ./niri-install.sh
```

---

## LabWC

LabWC window manager with Dank Material Shell (DMS) integration.

### Features

- **DMS Keybinds**: Full integration with Dank Material Shell
- **Auto Theme Switching**: Automatically switches themes based on sunset/sunrise
- **Window Management**: Snap/move windows to edges with keybinds

### Keybindings

| Key | Action |
|-----|--------|
| `W-Return` | Open terminal (wezterm) |
| `W-d` | Open app launcher (DMS) |
| `W-e` | File browser |
| `W-l` | Lock screen |
| `W-Tab` | Window switcher |
| `W-c` | Control Center |
| `W-v` | Clipboard |
| `W-n` | Notifications |
| `W-Escape` | Power menu (shutdown, restart, logout) |
| `W-r` | Reload config |
| `W-Left/Right/Up/Down` | Snap window to edge |
| `W-Shift-Left/Right/Up/Down` | Move window to edge |

### Auto Theme

Automatically switches between light/dark themes based on your location and sunset/sunrise times.

**Affected Applications:**
- GTK4/Libadwaita apps (Firefox, GNOME apps)
- WezTerm (auto-detects system color scheme)
- DMS (via IPC)

**Manual control:**
```bash
# Set dark theme
gsettings set org.gnome.desktop.interface color-scheme 'prefer-dark'

# Set light theme
gsettings set org.gnome.desktop.interface color-scheme 'prefer-light'
```

**Check status:**
```bash
systemctl --user list-timers | grep auto-theme
journalctl --user -u auto-theme -f
```

---

## Niri

Scrollable Wayland compositor with smooth animations.

### Features

- Scrollable window layout
- Smooth animations and transitions
- Workspace management
- Multi-monitor support

### Installation

```bash
cd niri && ./niri-install.sh
```

---

## WezTerm

GPU-accelerated terminal emulator with Lua configuration.

### Features

- Auto theme switching (Tokyo Night Day/Night)
- Tab bar at bottom
- Hide tab bar with single tab
- Font: 0xProto Nerd Font + JetBrains Mono fallback

### Configuration

Auto-switches color scheme based on system appearance:
- **Dark mode**: Tokyo Night
- **Light mode**: Tokyo Night Day

---

## ZSH

ZSH shell with Oh My Zsh framework.

### Features

- Theme: robbyrussell
- Oh My Zsh plugins
- Custom PATH and exports

### Configuration

Edit `zsh/.zshrc` for personal settings.

---

## Neovim

Modern Neovim configuration with Lua.

### Features

- Space as leader key
- Relative line numbers
- Mouse support
- Vim-style navigation
- Undofile persistence
- Smart case search
- Cursor line highlight

### Key Settings

- `mapleader = " "`
- `number + relativenumber`
- `mouse = "a"`
- `breakindent = true`

---

## Tmux

Terminal multiplexer with productivity enhancements.

### Features

- Ctrl+Space as prefix
- Vim-style pane navigation (hjkl)
- Alt+arrow keys for panes
- Shift+arrow for windows
- Mouse support
- Vi mode in copy mode

### Plugins

- `tmux-plugins/tpm` - Plugin manager
- `tmux-plugins/tmux-sensible` - Sensible defaults
- `tmux-plugins/tmux-yank` - Copy to system clipboard
- `christoomey/vim-tmux-navigator` - Vim navigation

### Keybindings

| Key | Action |
|-----|--------|
| `Ctrl+Space` | Prefix |
| `Prefix h/j/k/l` | Navigate panes |
| `Alt+arrows` | Navigate panes |
| `Shift+arrows` | Switch windows |

---

## Kanata

Keyboard remapping tool.

### Features

- Caps Lock as tap/hold layer switcher
- **Tap**: Caps Lock
- **Hold**: Arrow keys layer (hjkl → ←↓↑→)

### Configuration

Edit `kanata/etc/kanata/config.kbd` for custom keymaps.

---

## Slick Greeter

LightDM display manager theme.

### Configuration

Located in `slick-greeter/etc/lightdm/`.

---

## Wallpapers

Collection of wallpapers for different themes and setups.

---

## License

MIT
