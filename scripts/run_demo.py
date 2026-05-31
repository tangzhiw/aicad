from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PYTHON = sys.executable


def run(args: list[str]) -> None:
    print("\n$", " ".join(args))
    subprocess.run(args, cwd=ROOT, check=True)


def main() -> None:
    run([PYTHON, "scripts/create_original_dxf.py"])
    run([PYTHON, "scripts/dxf_to_yaml.py"])
    run([PYTHON, "scripts/yaml_to_dxf.py"])
    run([PYTHON, "scripts/verify_dxf.py"])
    run([PYTHON, "scripts/render_preview.py"])
    print("\nDemo finished. Open outputs/validation_report.json to see the validation result.")


if __name__ == "__main__":
    main()
