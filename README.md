# Dotfiles

Personal dotfiles for Arch Linux with Wayland compositors.

## Components

| Component | Description |
|-----------|-------------|
| `labwc` | LabWC window manager with DMS integration |
| `niri` | Niri scrollable Wayland compositor |
| `wezterm` | WezTerm terminal with auto theme switching |
| `zsh` | ZSH with Oh My Zsh |
| `nvim` | Neovim configuration with LSP/DAP |
| `tmux` | Tmux terminal multiplexer |
| `kanata` | Keyboard remapping (CapsLock → arrows) |
| `systemd` | Auto-theme switcher service |
| `dms` | DankMaterialShell settings & greeter config |
| `wallpapers` | Wallpaper collection |

---

## Quick Start

### Prerequisites

```bash
# Base development tools
sudo pacman -Suy && sudo pacman -S --needed --noconfirm git base-devel
```

### Installation

**Main installer (recommended):**

```bash
./install.sh
```

**Installation options:**
```
1) Terminal Apps Only (TTY usage, no compositor)
2) LabWC (includes Terminal Apps)
3) Niri (includes Terminal Apps)
4) LabWC + Niri (includes Terminal Apps)
5) Exit
```

### Package Lists

| File | Packages |
|------|----------|
| `terminal-apps.lst` | btop, fzf, neovim, zsh, lazygit, lf, ripgrep, stow, tldr, jq, curl, nerd fonts |
| `common-apps.lst` | xwayland, xdg-desktop-portal, swayidle, wlogout, mako, dms-shell, nautilus, wezterm, chrome, flatpak |
| `labwc-apps.lst` | labwc |
| `niri-apps.lst` | niri |

---

## LabWC

Stacking Wayland window manager with DMS (Dank Material Shell) integration.

### Features

- DMS integration (launcher, clipboard, notifications, control center)
- Auto theme switching (sunrise/sunset)
- 5 virtual desktops
- Media keys support
- Keyboard layout switching (Alt+Shift)

### Keybindings

#### General

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
| `W-p` | Process list (top bar widget) |
| `W-Escape` | Power menu |
| `W-r` | Reload config |

#### Desktop Switching

| Key | Action |
|-----|--------|
| `W-1` to `W-5` | Switch to desktop 1-5 |
| `W-Shift-1` to `W-Shift-5` | Move window to desktop 1-5 |

#### Window Management

| Key | Action |
|-----|--------|
| `W-Left/Right/Up/Down` | Snap window to edge |
| `W-Shift-Left/Right/Up/Down` | Move window to edge |
| `W-Up` | Toggle maximize |

#### Audio & Brightness

| Key | Action |
|-----|--------|
| `XF86AudioRaiseVolume` | Volume +5% |
| `XF86AudioLowerVolume` | Volume -5% |
| `XF86AudioMute` | Toggle mute |
| `XF86AudioMicMute` | Toggle mic mute |
| `XF86MonBrightnessUp` | Brightness +10% |
| `XF86MonBrightnessDown` | Brightness -10% |

#### Keyboard Layout

| Key | Action |
|-----|--------|
| `Alt+Shift` | Toggle US ↔ Russian (Mac) layout |

### Configuration Files

| File | Purpose |
|------|---------|
| `labwc/.config/labwc/rc.xml` | Main config: keybindings, mouse, desktops |
| `labwc/.config/labwc/autostart` | Startup: DMS, mako, polkit, xdg-portal |
| `labwc/.config/labwc/environment` | Environment variables, keyboard layout |

---

## Niri

Scrollable Wayland compositor with smooth animations.

### Features

- Scrollable window layout
- Smooth animations
- Workspace management
- Multi-monitor support
- Auto theme switching

### Keybindings

| Key | Action |
|-----|--------|
| `Mod+T` | Open terminal (ghostty) |
| `Mod+E` | Open file manager (nautilus) |
| `Alt+Space` | Open launcher (fuzzel) |
| `Mod+Q` | Close window |
| `Mod+H/J/K/L` | Navigate windows |
| `Mod+Shift+H/J/K/L` | Move windows |
| `Mod+1-9` | Switch workspaces |
| `Mod+Ctrl+1-9` | Move column to workspace |
| `Mod+R` | Switch preset column width |
| `Mod+F` | Maximize column |
| `Mod+V` | Toggle floating |
| `Print` | Screenshot |
| `Mod+Shift+E` | Quit compositor |

### Configuration

| File | Purpose |
|------|---------|
| `niri/.config/niri/config.kdl` | Main config: input, layout, keybindings, animations |

---

## WezTerm

GPU-accelerated terminal emulator.

### Features

- Auto theme switching (Tokyo Night Day/Night)
- Tab bar at bottom
- Hide tab bar with single tab
- Font: 0xProto Nerd Font + JetBrains Mono fallback

### Configuration

Auto-switches color scheme based on system appearance:
- **Dark mode**: Tokyo Night
- **Light mode**: Tokyo Night Day

| File | Purpose |
|------|---------|
| `wezterm/.wezterm.lua` | Font, tabs, theme switching |

---

## ZSH

ZSH shell with Oh My Zsh.

### Features

- Theme: robbyrussell
- Plugins: git
- Aliases: `vc=nvim`, `ll=ls -lah`, `lg=lazygit`
- `fcd` function: fuzzy find directory

| File | Purpose |
|------|---------|
| `zsh/.zshrc` | Shell configuration |

---

## Neovim

Modern Neovim configuration with Lua.

### Features

- Space as leader key
- LSP: gopls, ruff, basedpyright, lua_ls, clangd
- DAP debugging (Python, Go)
- Treesitter highlighting
- flash.nvim for navigation
- mini.nvim modules
- auto-dark-mode.nvim

### Keybindings

| Key | Action |
|-----|--------|
| `<Space>` | Leader key |
| `<Space>t` | Toggle terminal |
| `<Space>e` | File explorer |
| `<Space>gg` | Lazygit |
| `<Space>sg` | Ripgrep search |
| `<Space>bd` | Buffer delete |
| `<Space>qq` | Quit all |
| `F5/F7/F8/F9` | DAP debugging |
| `Ctrl+Arrows` | Resize windows |

| File | Purpose |
|------|---------|
| `nvim/.config/nvim/init.lua` | Full Lua configuration |

---

## Tmux

Terminal multiplexer.

### Features

- Prefix: `Ctrl+Space`
- Vim-style pane navigation
- Mouse support
- Vi mode in copy mode

### Plugins

- `tmux-plugins/tpm` - Plugin manager
- `tmux-plugins/tmux-sensible`
- `tmux-plugins/tmux-yank`
- `christoomey/vim-tmux-navigator`

### Keybindings

| Key | Action |
|-----|--------|
| `Ctrl+Space` | Prefix |
| `Prefix h/j/k/l` | Navigate panes |
| `Alt+arrows` | Navigate panes (no prefix) |
| `Shift+arrows` | Switch windows |

| File | Purpose |
|------|---------|
| `tmux/.tmux.conf` | Tmux configuration |

---

## Kanata

Keyboard remapping tool.

### Features

- Caps Lock as tap/hold
- **Tap**: Caps Lock
- **Hold**: Arrow keys layer (h→←, j→↓, k→↑, l→→)

| File | Purpose |
|------|---------|
| `kanata/etc/kanata/config.kbd` | Keyboard remapping |
| `kanata/etc/systemd/system/kanata.service` | Systemd service |

---

## Auto Theme

Sunrise/sunset based theme switcher.

### Features

- IP geolocation (with offline fallback)
- Caches sun times (1 hour) and location
- Switches GTK2/3/4, Chrome, DMS themes
- **Auto night mode (gamma adjustment at sunset)**
- D-Bus signals for app notifications
- Runs every 1 minute via systemd timer

### Behavior

| Time | Theme | Night Mode |
|------|-------|------------|
| Sunrise → Sunset | Light | Disabled (6500K) |
| Sunset → Sunrise | Dark | Enabled (4500K) |

### Affected Applications

- GTK2/3/4 apps (Firefox, GNOME apps)
- Chrome/Chromium browsers
- WezTerm (auto-detects)
- DMS (via IPC)
- Night mode (gamma/temperature adjustment)

### Manual Control

```bash
# Dark theme
gsettings set org.gnome.desktop.interface color-scheme 'prefer-dark'
gsettings set org.gnome.desktop.interface gtk-theme 'Adwaita-dark'

# Light theme
gsettings set org.gnome.desktop.interface color-scheme 'prefer-light'
gsettings set org.gnome.desktop.interface gtk-theme 'Adwaita'
```

### Status

```bash
# Check timer
systemctl --user list-timers | grep auto-theme

# View logs
journalctl --user -u auto-theme -f
```

| File | Purpose |
|------|---------|
| `systemd/.config/auto-theme.py` | Theme switcher script |
| `systemd/.config/systemd/user/auto-theme.service` | Systemd service |
| `systemd/.config/systemd/user/auto-theme.timer` | Timer (1 min interval) |

---

## DMS Greeter

Login screen theme management with greetd.

### Setup

```bash
# Enable greeter (requires sudo)
dms greeter install -y

# Sync user theme to greeter
dms greeter sync
```

### Theme Switching

The greeter automatically syncs with your DMS desktop theme:
- Manual: `dms greeter sync` after changing themes
- Auto: Via `auto-theme.py` (sunrise/sunset)

### Configuration

| File | Purpose |
|------|---------|
| `dms/.config/DankMaterialShell/settings.json` | Greeter theme settings |
| `/etc/greetd/config.toml` | Greetd configuration (dms-greeter + labwc) |

### Available Themes

Built-in themes: `blue`, `red`, `green`, `purple`, `orange`, `pink`, `teal`, `brown`

Edit `settings.json` to change:
```json
{
  "currentThemeName": "blue",
  "fontFamily": "Cantarell",
  "cornerRadius": 12
}
```

---

## Installation Structure

```
dotfiles/
├── install.sh                  # Main installer
├── terminal-apps.lst           # Terminal utilities
├── common-apps.lst             # Desktop apps
├── labwc-apps.lst              # LabWC
├── niri-apps.lst               # Niri
├── systemd/                    # Auto-theme service
│   └── .config/
│       ├── auto-theme.py
│       └── systemd/user/
│           ├── auto-theme.service
│           └── auto-theme.timer
├── labwc/
│   └── .config/labwc/
├── niri/
│   └── .config/niri/
├── nvim/
│   └── .config/nvim/
├── wezterm/
├── zsh/
├── tmux/
└── kanata/
```

---

## License

MIT
