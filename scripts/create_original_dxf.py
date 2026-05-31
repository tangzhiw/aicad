from __future__ import annotations

from pathlib import Path

import ezdxf
from ezdxf.enums import TextEntityAlignment

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT = ROOT / "examples" / "original_simple.dxf"


def create_original_dxf(output_path: Path = DEFAULT_OUTPUT) -> None:
    """创建一个很简单的原始 DXF，用于演示 DXF -> YAML -> DXF -> 校验。"""
    doc = ezdxf.new("R2010")

    # 图层颜色只是示例，便于在 CAD 软件中区分。
    doc.layers.add("OUTLINE", color=7)
    doc.layers.add("HOLE", color=1)
    doc.layers.add("CENTER", color=5)
    doc.layers.add("TEXT", color=3)

    msp = doc.modelspace()

    # 1) 外轮廓：一个 160 x 80 的矩形板。
    msp.add_lwpolyline(
        [(0, 0), (160, 0), (160, 80), (0, 80)],
        close=True,
        dxfattribs={"layer": "OUTLINE"},
    )

    # 2) 两个圆孔。
    msp.add_circle((40, 40), 8, dxfattribs={"layer": "HOLE"})
    msp.add_circle((120, 40), 8, dxfattribs={"layer": "HOLE"})

    # 3) 中心线。
    msp.add_line((0, 40), (160, 40), dxfattribs={"layer": "CENTER"})
    msp.add_line((80, 0), (80, 80), dxfattribs={"layer": "CENTER"})

    # 4) 一个简单文字。
    text = msp.add_text("SIMPLE PLATE", height=8, dxfattribs={"layer": "TEXT"})
    text.set_placement((45, 92), align=TextEntityAlignment.LEFT)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    doc.saveas(output_path)
    print(f"created: {output_path}")


if __name__ == "__main__":
    create_original_dxf()
