#!/usr/bin/env python3
import os
import shutil
import sys
from pathlib import Path


def candidate_paths() -> list[Path]:
    candidates: list[Path] = []

    for env_name in ("FREECADCMD", "FREECAD_CMD", "FREECADCMD_PATH"):
        value = os.environ.get(env_name)
        if value:
            candidates.append(Path(value))

    for name in ("FreeCADCmd", "freecadcmd", "FreeCADCmd.exe", "freecadcmd.exe"):
        resolved = shutil.which(name)
        if resolved:
            candidates.append(Path(resolved))

    if os.name == "nt":
        candidates.extend(windows_registry_candidates())
        candidates.extend(
            Path(path)
            for path in (
                r"C:\Program Files\FreeCAD 1.1\bin\freecadcmd.exe",
                r"C:\Program Files\FreeCAD 1.0\bin\freecadcmd.exe",
                r"C:\Program Files\FreeCAD 0.21\bin\freecadcmd.exe",
                r"C:\Program Files (x86)\FreeCAD 1.1\bin\freecadcmd.exe",
                r"D:\Program Files\FreeCAD 1.1\bin\freecadcmd.exe",
            )
        )

    seen: set[Path] = set()
    unique: list[Path] = []
    for candidate in candidates:
        normalized = candidate.expanduser()
        if normalized not in seen:
            seen.add(normalized)
            unique.append(normalized)
    return unique


def windows_registry_candidates() -> list[Path]:
    if os.name != "nt":
        return []

    try:
        import winreg
    except ImportError:
        return []

    roots = (winreg.HKEY_LOCAL_MACHINE, winreg.HKEY_CURRENT_USER)
    subkeys = (
        r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall",
        r"SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall",
    )
    candidates: list[Path] = []

    for root in roots:
        for subkey in subkeys:
            try:
                with winreg.OpenKey(root, subkey) as parent:
                    count = winreg.QueryInfoKey(parent)[0]
                    for index in range(count):
                        try:
                            app_key_name = winreg.EnumKey(parent, index)
                            with winreg.OpenKey(parent, app_key_name) as app_key:
                                name = registry_value(app_key, "DisplayName")
                                if "freecad" not in name.lower():
                                    continue
                                candidates.extend(paths_from_registry(app_key))
                        except OSError:
                            continue
            except OSError:
                continue

    return candidates


def registry_value(key, name: str) -> str:
    try:
        import winreg

        value, _ = winreg.QueryValueEx(key, name)
    except OSError:
        return ""
    return str(value).strip().strip('"')


def paths_from_registry(key) -> list[Path]:
    candidates: list[Path] = []
    install_location = registry_value(key, "InstallLocation")
    display_icon = registry_value(key, "DisplayIcon").split(",", 1)[0]

    if install_location:
        install_path = Path(install_location)
        candidates.extend(
            [
                install_path / "bin" / "freecadcmd.exe",
                install_path / "freecadcmd.exe",
            ]
        )
    if display_icon:
        icon_path = Path(display_icon)
        candidates.append(icon_path.with_name("freecadcmd.exe"))
        if icon_path.parent.name.lower() != "bin":
            candidates.append(icon_path.parent / "bin" / "freecadcmd.exe")
    return candidates


def find_freecadcmd() -> Path:
    for candidate in candidate_paths():
        if candidate.is_file():
            return candidate.resolve()
    checked = "\n".join(f"- {path}" for path in candidate_paths())
    raise RuntimeError(
        "FreeCADCmd/freecadcmd was not found. Set FREECADCMD to the full executable path.\n"
        f"Checked:\n{checked}"
    )


def bootstrap_freecad_python() -> Path:
    freecadcmd = find_freecadcmd()
    freecad_bin = freecadcmd.parent
    if os.name == "nt":
        os.add_dll_directory(str(freecad_bin))
    if str(freecad_bin) not in sys.path:
        sys.path.insert(0, str(freecad_bin))
    return freecadcmd
