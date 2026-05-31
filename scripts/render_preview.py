from __future__ import annotations

import argparse
from pathlib import Path
from typing import Iterable

import ezdxf
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]


def p2(value: Iterable[float]) -> tuple[float, float]:
    v = list(value)
    return float(v[0]), float(v[1])


def draw_dxf(ax, path: Path, title: str) -> None:
    doc = ezdxf.readfile(path)
    ax.set_aspect("equal", adjustable="box")
    ax.set_title(title)
    ax.grid(True, linewidth=0.3)

    for e in doc.modelspace():
        t = e.dxftype()
        if t == "LINE":
            x1, y1 = p2(e.dxf.start)
            x2, y2 = p2(e.dxf.end)
            ax.plot([x1, x2], [y1, y2], linewidth=1)
        elif t == "CIRCLE":
            x, y = p2(e.dxf.center)
            circle = plt.Circle((x, y), float(e.dxf.radius), fill=False, linewidth=1)
            ax.add_patch(circle)
        elif t == "ARC":
            # demo 中默认不使用 ARC。这里保留占位，避免预览失败。
            pass
        elif t == "LWPOLYLINE":
            pts = [p2(p) for p in e.get_points(format="xy")]
            if e.closed and pts:
                pts.append(pts[0])
            if pts:
                xs, ys = zip(*pts)
                ax.plot(xs, ys, linewidth=1)
        elif t == "TEXT":
            x, y = p2(e.dxf.insert)
            ax.text(x, y, e.plain_text(), fontsize=8)

    ax.autoscale()


def main() -> None:
    parser = argparse.ArgumentParser(description="生成原始 DXF 与再生成 DXF 的对比预览图")
    parser.add_argument("--original", default=str(ROOT / "examples" / "original_simple.dxf"))
    parser.add_argument("--generated", default=str(ROOT / "outputs" / "regenerated_from_yaml.dxf"))
    parser.add_argument("-o", "--output", default=str(ROOT / "outputs" / "original_vs_regenerated.png"))
    args = parser.parse_args()

    fig, axes = plt.subplots(1, 2, figsize=(10, 4))
    draw_dxf(axes[0], Path(args.original), "Original DXF")
    draw_dxf(axes[1], Path(args.generated), "Regenerated DXF")
    plt.tight_layout()

    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output, dpi=160)
    plt.close(fig)
    print(f"preview written: {output}")


if __name__ == "__main__":
    main()
