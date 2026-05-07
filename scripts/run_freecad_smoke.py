#!/usr/bin/env python3
import subprocess
import sys
from pathlib import Path

from freecad_locator import find_freecadcmd

ROOT = Path(__file__).resolve().parents[1]


def run(command: list[str]) -> None:
    print("+ " + " ".join(command))
    subprocess.run(command, cwd=ROOT, check=True)


def run_freecad_script(freecadcmd: Path, script_path: str) -> None:
    command = [
        str(freecadcmd),
        "-c",
        f"import runpy; runpy.run_path({script_path!r}, run_name='__main__')",
    ]
    run(command)


def main() -> None:
    try:
        freecadcmd = find_freecadcmd()
    except RuntimeError as exc:
        raise SystemExit(str(exc)) from exc
    print(f"FreeCADCmd: {freecadcmd}")
    run([sys.executable, "scripts/create_project_structure.py"])
    run_freecad_script(freecadcmd, "scripts/generate_freecad_base.py")
    run([sys.executable, "scripts/validate_printability.py"])


if __name__ == "__main__":
    main()
