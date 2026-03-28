#!/usr/bin/env python3
"""Auto theme switcher based on sunrise/sunset with auto location detection.

Uses standard GTK/KDE color-scheme settings that apps check.
Supports: GTK3, GTK4, GTK2, Chrome, KDE Plasma
"""

import json
import sys
import time
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from subprocess import run

# =============================================================================
# Configuration
# =============================================================================

CACHE_DIR = Path.home() / ".cache"
CACHE_FILE = CACHE_DIR / "sun-times"
CACHE_DURATION = 3600  # Cache sunrise/sunset for 1 hour (seconds)
LOCATION_CACHE = CACHE_DIR / "auto-theme-location"

GTK_THEME_DARK = "Adwaita-dark"
GTK_THEME_LIGHT = "Adwaita"

GEO_APIS = [
    ("https://ipapi.co/json/", ["latitude", "longitude"]),
    ("http://ip-api.com/json/", ["lat", "lon"]),
]

SUN_API = "https://api.sunrise-sunset.org/json"


# =============================================================================
# Data Classes
# =============================================================================

@dataclass
class Location:
    latitude: str
    longitude: str


@dataclass
class SunTimes:
    sunrise: str
    sunset: str


# =============================================================================
# Helper Functions
# =============================================================================

def run_cmd(cmd: list[str], timeout: int = 5) -> tuple[bool, str]:
    """Run a shell command and return success status and output."""
    try:
        result = run(cmd, capture_output=True, text=True, timeout=timeout)
        return result.returncode == 0, result.stdout
    except (TimeoutError, FileNotFoundError):
        return False, ""


def fetch_json(url: str, timeout: int = 5) -> dict | None:
    """Fetch and parse JSON from URL."""
    success, response = run_cmd(["curl", "-s", "--max-time", str(timeout), url])
    if not success:
        return None
    try:
        return json.loads(response)
    except json.JSONDecodeError:
        return None


# =============================================================================
# Location Detection
# =============================================================================

def get_location() -> Location | None:
    """Auto-detect location using IP geolocation with fallback to cache."""
    # Try online detection
    for url, keys in GEO_APIS:
        data = fetch_json(url, timeout=5)
        if data:
            lat, lon = str(data.get(keys[0], "")), str(data.get(keys[1], ""))
            if lat and lon and lat != "null" and lon != "null":
                _cache_location(lat, lon)
                print(f"Location detected: {lat}, {lon} (via {url})", file=sys.stderr)
                return Location(lat, lon)

    # Fallback to cached location
    if LOCATION_CACHE.exists():
        try:
            lat, lon = LOCATION_CACHE.read_text().strip().split(",")
            if lat and lon:
                print(f"Using cached location: {lat}, {lon} (offline mode)", file=sys.stderr)
                return Location(lat, lon)
        except Exception:
            pass

    print("Failed to detect location. Check your internet connection.", file=sys.stderr)
    return None


def _cache_location(lat: str, lon: str) -> None:
    """Cache location for offline fallback."""
    LOCATION_CACHE.parent.mkdir(parents=True, exist_ok=True)
    LOCATION_CACHE.write_text(f"{lat},{lon}")


# =============================================================================
# Sun Times
# =============================================================================

def get_sun_times(loc: Location) -> SunTimes | None:
    """Get sunrise/sunset times from API with caching."""
    # Check cache
    if CACHE_FILE.exists():
        cache_time = CACHE_FILE.stat().st_mtime
        age = time.time() - cache_time
        if age < CACHE_DURATION:
            sun_times = _load_cached_sun_times()
            if sun_times:
                print(f"Using cached sun times (age: {int(age)}s)", file=sys.stderr)
                return sun_times

    # Fetch from API
    params = f"?lat={loc.latitude}&lng={loc.longitude}&formatted=0"
    data = fetch_json(SUN_API + params, timeout=10)

    if not data or data.get("status") != "OK":
        print("Failed to get sun times from API", file=sys.stderr)
        # Fallback to expired cache
        sun_times = _load_cached_sun_times()
        if sun_times:
            print("Using expired cached sun times as fallback", file=sys.stderr)
            return sun_times
        return None

    sunrise = data["results"]["sunrise"]
    sunset = data["results"]["sunset"]
    _cache_sun_times(sunrise, sunset)
    print(f"Sunrise: {sunrise}, Sunset: {sunset}", file=sys.stderr)
    return SunTimes(sunrise, sunset)


def _cache_sun_times(sunrise: str, sunset: str) -> None:
    """Cache sun times to file."""
    CACHE_FILE.parent.mkdir(parents=True, exist_ok=True)
    CACHE_FILE.write_text(f"SUNRISE={sunrise}\nSUNSET={sunset}\n")


def _load_cached_sun_times() -> SunTimes | None:
    """Load sun times from cache file."""
    try:
        content = CACHE_FILE.read_text()
        sunrise = sunset = ""
        for line in content.strip().split("\n"):
            if line.startswith("SUNRISE="):
                sunrise = line.split("=", 1)[1].strip('"')
            elif line.startswith("SUNSET="):
                sunset = line.split("=", 1)[1].strip('"')
        if sunrise and sunset:
            return SunTimes(sunrise, sunset)
    except Exception:
        pass
    return None


def is_night(sun: SunTimes) -> bool:
    """Check if current time is between sunset and sunrise (night time)."""
    try:
        now = datetime.now().astimezone()
        sunrise = datetime.fromisoformat(sun.sunrise.replace("Z", "+00:00")).astimezone()
        sunset = datetime.fromisoformat(sun.sunset.replace("Z", "+00:00")).astimezone()
        return now >= sunset or now <= sunrise
    except Exception as e:
        print(f"Failed to parse sun times: {e}", file=sys.stderr)
        return False


# =============================================================================
# Theme Switching
# =============================================================================

def switch_theme(is_dark: bool) -> None:
    """Switch system theme (GTK + Chrome support)."""
    scheme = "prefer-dark" if is_dark else "prefer-light"
    gtk_theme = GTK_THEME_DARK if is_dark else GTK_THEME_LIGHT

    # GTK settings
    run_cmd(["gsettings", "set", "org.gnome.desktop.interface", "color-scheme", scheme])
    run_cmd(["gsettings", "set", "org.gnome.desktop.interface", "gtk-theme", gtk_theme])

    # GTK3 config
    gtk3 = Path.home() / ".config" / "gtk-3.0" / "settings.ini"
    gtk3.parent.mkdir(parents=True, exist_ok=True)
    gtk3.write_text(f"[Settings]\ngtk-application-prefer-dark-theme={str(is_dark).lower()}\ngtk-theme-name={gtk_theme}\n")

    # GTK4 config
    gtk4 = Path.home() / ".config" / "gtk-4.0" / "settings.ini"
    gtk4.parent.mkdir(parents=True, exist_ok=True)
    gtk4.write_text(f"[Settings]\ngtk-application-prefer-dark-theme={str(is_dark).lower()}\n")

    # GTK2 config
    gtk2 = Path.home() / ".gtk-2.0" / "gtkrc"
    gtk2.parent.mkdir(parents=True, exist_ok=True)
    gtk2.write_text(f'gtk-theme-name="{gtk_theme}"\n')

    # Chrome config
    _update_chrome_theme(is_dark)

    # D-Bus signal for portal apps
    run_cmd([
        "gdbus", "emit", "--session",
        "--dest", "org.freedesktop.portal.Desktop",
        "--object-path", "/org/freedesktop/portal/desktop",
        "--interface", "org.freedesktop.portal.Settings",
        "--signal", "SettingChanged",
        "string:org.freedesktop.appearance",
        "string:color-scheme",
        "uint32:1" if is_dark else "uint32:0"
    ])

    print(f"GTK: Set color-scheme to {scheme}, gtk-theme to {gtk_theme}")


def _update_chrome_theme(is_dark: bool) -> None:
    """Update Chrome theme configuration."""
    theme = "dark" if is_dark else "light"
    chrome_dir = Path.home() / ".config" / "google-chrome"

    # Local State
    state_file = chrome_dir / "Local State"
    if state_file.exists():
        try:
            data = json.loads(state_file.read_text())
            data.setdefault("browser", {})["theme_name"] = theme
            state_file.write_text(json.dumps(data))
            print(f"Chrome Local State: Set theme_name to {theme}")
        except Exception as e:
            print(f"Failed to update Chrome Local State: {e}", file=sys.stderr)

    # Profile Preferences (Default profile)
    prefs_file = chrome_dir / "Default" / "Preferences"
    if prefs_file.exists():
        try:
            data = json.loads(prefs_file.read_text())
            data.setdefault("browser", {})["theme_name"] = theme
            data.setdefault("profile", {})["theme_name"] = theme
            prefs_file.write_text(json.dumps(data))
            print(f"Chrome Preferences: Set theme_name to {theme}")
        except Exception as e:
            print(f"Failed to update Chrome Preferences: {e}", file=sys.stderr)


# =============================================================================
# Main
# =============================================================================

def main() -> int:
    """Main entry point."""
    print("=== Auto Theme Switcher ===")
    print(f"Time: {datetime.now()}")

    # Get location
    loc = get_location()
    if not loc:
        return 1

    # Get sun times
    sun = get_sun_times(loc)
    if not sun:
        return 1

    # Determine theme
    night = is_night(sun)
    period = "Night" if night else "Day"
    theme = "dark" if night else "light"
    print(f"Period: {period} ({theme} theme)")

    print("\nSwitching themes...")
    switch_theme(night)

    print("\nTheme switch complete!")
    return 0


if __name__ == "__main__":
    sys.exit(main())
