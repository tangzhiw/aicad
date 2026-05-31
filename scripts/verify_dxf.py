from __future__ import annotations

import argparse
import json
from pathlib import Path

from cad_yaml_common import compare_dxf

ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    parser = argparse.ArgumentParser(description="验证两个 DXF 在 demo 支持的实体范围内是否一致")
    parser.add_argument("original", nargs="?", default=str(ROOT / "examples" / "original_simple.dxf"))
    parser.add_argument("generated", nargs="?", default=str(ROOT / "outputs" / "regenerated_from_yaml.dxf"))
    parser.add_argument("-o", "--output", default=str(ROOT / "outputs" / "validation_report.json"))
    parser.add_argument("--tolerance", type=float, default=1e-6)
    args = parser.parse_args()

    report = compare_dxf(args.original, args.generated, tolerance=args.tolerance)
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")

    print("PASS" if report["passed"] else "FAIL")
    print(f"report written: {output}")
    if not report["passed"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
