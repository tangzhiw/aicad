from __future__ import annotations

import argparse
from pathlib import Path

from cad_yaml_common import dxf_to_yaml_data, write_yaml

ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    parser = argparse.ArgumentParser(description="将简单 DXF 转换为 YAML 描述文件")
    parser.add_argument("input", nargs="?", default=str(ROOT / "examples" / "original_simple.dxf"))
    parser.add_argument("-o", "--output", default=str(ROOT / "examples" / "simple_from_dxf.yaml"))
    args = parser.parse_args()

    data = dxf_to_yaml_data(args.input)
    write_yaml(data, args.output)
    print(f"yaml written: {args.output}")


if __name__ == "__main__":
    main()
