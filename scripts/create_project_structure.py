#!/usr/bin/env python3
from pathlib import Path


PROJECT_DIRS = [
    ".codex",
    "input/sketches",
    "input/references",
    "specs",
    "output/cad",
    "output/print",
    "output/reports",
]


def create_concept_placeholder(root: Path) -> None:
    concept_path = root / "input" / "concept.md"
    if concept_path.exists():
        print(f"exists: {concept_path}")
        return

    template_path = Path(__file__).resolve().parents[1] / "assets" / "concept.template.md"
    if template_path.exists():
        concept_path.write_text(template_path.read_text(encoding="utf-8"), encoding="utf-8")
    else:
        concept_path.write_text("# Technical Engineering Sketch Concept\n", encoding="utf-8")
    print(f"created: {concept_path}")


def main() -> None:
    root = Path.cwd()
    for directory in PROJECT_DIRS:
        path = root / directory
        path.mkdir(parents=True, exist_ok=True)
        print(f"ok: {path}")
    create_concept_placeholder(root)


if __name__ == "__main__":
    main()
