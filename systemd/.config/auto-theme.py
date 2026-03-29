#!/usr/bin/env python3
"""Auto theme switcher based on sunrise/sunset with auto location detection.

Uses DMS IPC for theme switching.
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
    """Switch system theme and night mode based on time of day."""
    theme_cmd = "dark" if is_dark else "light"

    # DMS theme
    run_cmd(["dms", "ipc", "theme", theme_cmd])
    print(f"DMS: Set theme to {theme_cmd}")

    # DMS greeter theme sync
    run_cmd(["dms", "greeter", "sync"])
    print(f"DMS Greeter: Synced theme")

    # DMS night mode (gamma adjustment for eye comfort)
    if is_dark:
        # Enable night mode with warmer color temperature (4500K)
        run_cmd(["dms", "ipc", "gamma", "night"])
        print("DMS: Night mode enabled (4500K)")
    else:
        # Disable night mode (return to normal 6500K)
        run_cmd(["dms", "ipc", "gamma", "off"])
        print("DMS: Night mode disabled")

    # Flatpak global theme override (for GTK apps)
    gtk_theme = "Adwaita-dark" if is_dark else "Adwaita"
    run_cmd(["flatpak", "override", "--user", f"--env=GTK_THEME={gtk_theme}"])
    print(f"Flatpak: Set global GTK_THEME to {gtk_theme}")

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
