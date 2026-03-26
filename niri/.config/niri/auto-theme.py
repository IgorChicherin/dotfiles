#!/usr/bin/env python3
"""Auto theme switcher based on sunrise/sunset with auto location detection.
Uses standard GTK/KDE color-scheme settings that apps check.
"""

import json
import os
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path

CACHE_FILE = Path.home() / ".cache" / "sun-times"
CACHE_DURATION = 3600  # Cache sunrise/sunset for 1 hour (seconds)


def run_command(cmd: list[str], timeout: int = 5) -> tuple[bool, str]:
    """Run a shell command and return success status and output."""
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=timeout
        )
        return result.returncode == 0, result.stdout
    except (subprocess.TimeoutExpired, FileNotFoundError):
        return False, ""


def get_location() -> tuple[bool, tuple[str, str]]:
    """Auto-detect location using IP geolocation."""
    # Method 1: ipapi.co (no auth required)
    success, response = run_command(
        ["curl", "-s", "--max-time", "5", "https://ipapi.co/json/"]
    )
    if success:
        try:
            data = json.loads(response)
            lat = data.get("latitude", "")
            lon = data.get("longitude", "")
            if lat and lon and lat != "null" and lon != "null":
                print(f"Location detected: {lat}, {lon} (via ipapi.co)", file=sys.stderr)
                return True, (str(lat), str(lon))
        except json.JSONDecodeError:
            pass

    # Method 2: ip-api.com (fallback)
    success, response = run_command(
        ["curl", "-s", "--max-time", "5", "http://ip-api.com/json/"]
    )
    if success:
        try:
            data = json.loads(response)
            lat = data.get("lat", "")
            lon = data.get("lon", "")
            if lat and lon:
                print(f"Location detected: {lat}, {lon} (via ip-api.com)", file=sys.stderr)
                return True, (str(lat), str(lon))
        except json.JSONDecodeError:
            pass

    print("Failed to detect location. Please check your internet connection.", file=sys.stderr)
    return False, ("", "")


def get_sun_times(lat: str, lon: str) -> tuple[bool, tuple[str, str]]:
    """Get sunrise/sunset times from API with caching."""
    # Check cache first
    if CACHE_FILE.exists():
        cache_time = CACHE_FILE.stat().st_mtime
        now = time.time()
        age = now - cache_time

        if age < CACHE_DURATION:
            sun_times = load_cached_sun_times()
            if sun_times:
                print(f"Using cached sun times (age: {int(age)}s)", file=sys.stderr)
                return True, sun_times

    # Fetch from API
    success, response = run_command(
        ["curl", "-s", "--max-time", "10",
         f"https://api.sunrise-sunset.org/json?lat={lat}&lng={lon}&formatted=0"],
        timeout=10
    )
    if not success:
        print("Failed to get sun times from API", file=sys.stderr)
        return False, ("", "")

    try:
        data = json.loads(response)
        if data.get("status") != "OK":
            print("Failed to get sun times from API", file=sys.stderr)
            return False, ("", "")

        sunrise = data["results"]["sunrise"]
        sunset = data["results"]["sunset"]

        # Cache the results
        CACHE_FILE.parent.mkdir(parents=True, exist_ok=True)
        CACHE_FILE.write_text(f"SUNRISE={sunrise}\nSUNSET={sunset}\n")

        print(f"Sunrise: {sunrise}, Sunset: {sunset}", file=sys.stderr)
        return True, (sunrise, sunset)

    except (json.JSONDecodeError, KeyError):
        print("Failed to parse sun times response", file=sys.stderr)
        return False, ("", "")


def load_cached_sun_times() -> tuple[str, str] | None:
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
            return sunrise, sunset
    except Exception:
        pass
    return None


def is_night(sunrise: str, sunset: str) -> bool:
    """Check if current time is between sunset and sunrise (night time)."""
    try:
        now = datetime.now()
        sunrise_dt = datetime.fromisoformat(sunrise.replace("Z", "+00:00"))
        sunset_dt = datetime.fromisoformat(sunset.replace("Z", "+00:00"))

        # Convert to local time for comparison
        now_ts = now.timestamp()
        sunrise_ts = sunrise_dt.timestamp()
        sunset_ts = sunset_dt.timestamp()

        return now_ts >= sunset_ts or now_ts <= sunrise_ts
    except Exception as e:
        print(f"Failed to parse sun times: {e}", file=sys.stderr)
        return False


def switch_gtk_theme(scheme: str) -> None:
    """Switch GTK color scheme (standard setting apps check)."""
    # Set GTK color scheme (used by Firefox, WezTerm, and GTK4 apps)
    run_command(["gsettings", "set", "org.gnome.desktop.interface", "color-scheme", scheme])

    # Also set legacy gtk-application-prefer-dark-theme for GTK3 apps
    success, keys = run_command(["gsettings", "list-keys", "org.gnome.desktop.interface"])
    if success and "gtk-application-prefer-dark-theme" in keys:
        value = "true" if scheme == "prefer-dark" else "false"
        run_command([
            "gsettings", "set", "org.gnome.desktop.interface",
            "gtk-application-prefer-dark-theme", value
        ])

    print(f"GTK: Set color-scheme to {scheme}")


def main() -> int:
    """Main entry point."""
    print("=== Auto Theme Switcher ===")
    print(f"Time: {datetime.now()}")

    # Get location
    success, location = get_location()
    if not success:
        return 1
    lat, lon = location

    # Get sun times
    success, sun_times = get_sun_times(lat, lon)
    if not success:
        return 1
    sunrise, sunset = sun_times

    # Determine theme
    if is_night(sunrise, sunset):
        gtk_scheme = "prefer-dark"
        print("Period: Night (dark theme)")
    else:
        gtk_scheme = "prefer-light"
        print("Period: Day (light theme)")

    print()
    print("Switching themes...")

    # Switch system-wide GTK theme (affects Firefox, WezTerm, GTK apps)
    switch_gtk_theme(gtk_scheme)

    print()
    print("Theme switch complete!")
    return 0


if __name__ == "__main__":
    sys.exit(main())
