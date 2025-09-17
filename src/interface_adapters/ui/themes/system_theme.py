"""
system_theme.py
Detección multiplataforma del tema del sistema (dark/light) para Logger OA v2.
"""

import sys
import os
import platform
from config.settings_service import ThemeValue

if sys.platform == "win32":
    import winreg


def detect_system_theme():
    """
    Detecta el tema del sistema operativo.
    Retorna ThemeValue.DARK o ThemeValue.LIGHT.
    """
    # Windows
    if sys.platform == "win32":
        try:
            registry = winreg.ConnectRegistry(None, winreg.HKEY_CURRENT_USER)
            key = winreg.OpenKey(
                registry,
                r"Software\\Microsoft\\Windows\\CurrentVersion\\Themes\\Personalize",
            )
            value, _ = winreg.QueryValueEx(key, "AppsUseLightTheme")
            winreg.CloseKey(key)
            return ThemeValue.LIGHT if value == 1 else ThemeValue.DARK
        except Exception:
            return ThemeValue.LIGHT
    # MacOS
    elif sys.platform == "darwin":
        try:
            import subprocess

            result = subprocess.run(
                ["defaults", "read", "-g", "AppleInterfaceStyle"],
                capture_output=True,
                text=True,
            )
            if result.returncode == 0 and "Dark" in result.stdout:
                return ThemeValue.DARK
            else:
                return ThemeValue.LIGHT
        except Exception:
            return ThemeValue.LIGHT
    # Linux
    elif sys.platform.startswith("linux"):
        desktop = os.environ.get("XDG_CURRENT_DESKTOP", "")
        # GNOME: aceptar variantes como "ubuntu:GNOME", "GNOME", etc.
        if any("GNOME" in d for d in desktop.split(":")):
            try:
                import subprocess

                # color-scheme (GNOME 42+)
                result = subprocess.run(
                    ["gsettings", "get", "org.gnome.desktop.interface", "color-scheme"],
                    capture_output=True,
                    text=True,
                )
                color_scheme = result.stdout.strip().lower()
                if result.returncode == 0 and "dark" in color_scheme:
                    return ThemeValue.DARK
                if result.returncode == 0 and "default" in color_scheme:
                    result_gtk = subprocess.run(
                        [
                            "gsettings",
                            "get",
                            "org.gnome.desktop.interface",
                            "gtk-theme",
                        ],
                        capture_output=True,
                        text=True,
                    )
                    gtk_theme = result_gtk.stdout.strip().lower().replace("'", "")
                    if "dark" in gtk_theme:
                        return ThemeValue.DARK
            except Exception:
                pass
        # KDE: ColorScheme y plasma-looks
        elif "KDE" in desktop:
            kdeglobals = os.path.expanduser("~/.config/kdeglobals")
            try:
                with open(kdeglobals, "r") as f:
                    for line in f:
                        if "ColorScheme=" in line and "Dark" in line:
                            return ThemeValue.DARK
            except Exception:
                pass
            # plasma-looks
            try:
                lookandfeel = os.path.expanduser("~/.config/plasmarc")
                with open(lookandfeel, "r") as f:
                    for line in f:
                        if "LookAndFeelPackage=" in line and "dark" in line.lower():
                            return ThemeValue.DARK
            except Exception:
                pass
        # XFCE: xfconf-query y xsettings.xml
        elif "XFCE" in desktop:
            try:
                import subprocess

                result = subprocess.run(
                    ["xfconf-query", "-c", "xsettings", "-p", "/Net/ThemeName"],
                    capture_output=True,
                    text=True,
                )
                if result.returncode == 0 and "dark" in result.stdout.lower():
                    return ThemeValue.DARK
            except Exception:
                pass
            try:
                xsettings = os.path.expanduser(
                    "~/.config/xfce4/xfconf/xfce-perchannel-xml/xsettings.xml"
                )
                if os.path.exists(xsettings):
                    with open(xsettings, "r") as f:
                        if "dark" in f.read().lower():
                            return ThemeValue.DARK
            except Exception:
                pass
        # LXDE/LXQt: variable de entorno GTK_THEME
        elif "LXDE" in desktop or "LXQt" in desktop:
            gtk_theme = os.environ.get("GTK_THEME", "")
            if "dark" in gtk_theme.lower():
                return ThemeValue.DARK
        # Variable de entorno GTK_THEME (aplicable a varios entornos)
        gtk_theme_env = os.environ.get("GTK_THEME", "")
        if "dark" in gtk_theme_env.lower():
            return ThemeValue.DARK
        # Variable de entorno QT_QPA_PLATFORMTHEME (Qt apps)
        qt_theme_env = os.environ.get("QT_QPA_PLATFORMTHEME", "")
        if "dark" in qt_theme_env.lower():
            return ThemeValue.DARK
        # Otros entornos: intentar leer tema desde archivos comunes
        # Cinnamon
        if "X-Cinnamon" in desktop:
            try:
                import subprocess

                result = subprocess.run(
                    ["gsettings", "get", "org.cinnamon.desktop.interface", "gtk-theme"],
                    capture_output=True,
                    text=True,
                )
                if result.returncode == 0 and "dark" in result.stdout.lower():
                    return ThemeValue.DARK
            except Exception:
                pass
        # Mate
        if "MATE" in desktop:
            try:
                import subprocess

                result = subprocess.run(
                    ["gsettings", "get", "org.mate.interface", "gtk-theme"],
                    capture_output=True,
                    text=True,
                )
                if result.returncode == 0 and "dark" in result.stdout.lower():
                    return ThemeValue.DARK
            except Exception:
                pass
        # Si no se detecta, usar claro por defecto
        return ThemeValue.LIGHT
    # Otros sistemas
    return ThemeValue.LIGHT
