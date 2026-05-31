from __future__ import annotations

import argparse
from pathlib import Path

from cad_yaml_common import read_yaml, yaml_data_to_dxf

ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    parser = argparse.ArgumentParser(description="将简单 YAML 描述文件重新生成 DXF")
    parser.add_argument("input", nargs="?", default=str(ROOT / "examples" / "simple_from_dxf.yaml"))
    parser.add_argument("-o", "--output", default=str(ROOT / "outputs" / "regenerated_from_yaml.dxf"))
    args = parser.parse_args()

    data = read_yaml(args.input)
    yaml_data_to_dxf(data, args.output)
    print(f"dxf written: {args.output}")


if __name__ == "__main__":
    main()
