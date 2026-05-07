# FreeCAD Product Engineering Skill

Codex skill for transforming technical engineering sketch concepts into parametric FreeCAD products for 3D printing.

## Scope

- Reads product concepts and sketches from `input/`.
- Builds or updates structured product specs in `specs/product-spec.json`.
- Generates CAD planning and printability reports.
- Uses FreeCAD as the source of truth for native files, STEP exports, and STL exports.
- Keeps printable physical parts separated as individual FreeCAD bodies or objects.

## Main Files

- `SKILL.md` - skill instructions and required workflow.
- `assets/concept.template.md` - starting template for product concepts.
- `assets/product-spec.template.json` - structured product specification template.
- `scripts/create_project_structure.py` - scaffold helper for new product projects.
- `scripts/generate_freecad_base.py` - base FreeCAD model generation helper.
- `scripts/run_freecad_smoke.py` - smoke-test runner that discovers `FreeCADCmd` and runs scaffold, CAD generation, and printability validation.
- `scripts/export_freecad_files.py` - export helper for native, STEP, and STL outputs.
- `scripts/validate_printability.py` - printability validation helper.

## Requirement

FreeCAD must be installed locally. For a full smoke test, run:

```powershell
python scripts/run_freecad_smoke.py
```

The runner checks `FREECADCMD`, `FREECAD_CMD`, `FREECADCMD_PATH`, PATH, Windows uninstall registry entries, and common install locations. If discovery still fails, set `FREECADCMD` to the full `freecadcmd.exe` path.
