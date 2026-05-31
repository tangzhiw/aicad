from __future__ import annotations

import json
import math
from pathlib import Path
from typing import Any, Dict, Iterable, List, Tuple

import ezdxf
import yaml
from ezdxf.enums import TextEntityAlignment

SUPPORTED_TYPES = {"LINE", "CIRCLE", "ARC", "LWPOLYLINE", "TEXT"}


def as_point2(value: Iterable[float]) -> List[float]:
    vals = list(value)
    if len(vals) < 2:
        raise ValueError(f"坐标至少需要 x,y 两个值: {value}")
    return [round(float(vals[0]), 6), round(float(vals[1]), 6)]


def pt_tuple(value: Iterable[float]) -> Tuple[float, float]:
    p = as_point2(value)
    return float(p[0]), float(p[1])


class FlowSeq(list):
    """让坐标点在 YAML 中显示成 [x, y]，避免变成多行嵌套列表。"""


def _flow_seq_representer(dumper: yaml.Dumper, data: FlowSeq):
    return dumper.represent_sequence("tag:yaml.org,2002:seq", data, flow_style=True)


class CompactDumper(yaml.SafeDumper):
    pass


CompactDumper.add_representer(FlowSeq, _flow_seq_representer)


def _compact_coords(obj: Any) -> Any:
    """把 [x, y] / [x, y, z] 坐标列表转成 flow style，提升 YAML 可读性。"""
    if isinstance(obj, dict):
        return {k: _compact_coords(v) for k, v in obj.items()}
    if isinstance(obj, list):
        if len(obj) in (2, 3) and all(isinstance(v, (int, float)) for v in obj):
            return FlowSeq(obj)
        return [_compact_coords(v) for v in obj]
    return obj


def write_yaml(data: Dict[str, Any], path: str | Path) -> None:
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    compact_data = _compact_coords(data)
    with open(path, "w", encoding="utf-8") as f:
        yaml.dump(compact_data, f, allow_unicode=True, sort_keys=False, Dumper=CompactDumper)


def read_yaml(path: str | Path) -> Dict[str, Any]:
    with open(path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    if not isinstance(data, dict):
        raise ValueError("YAML 根节点必须是对象")
    return data


def setup_layers(doc: ezdxf.EzDxf, layers: List[Dict[str, Any]]) -> None:
    for layer in layers:
        name = str(layer.get("name", "0"))
        if name == "0":
            continue
        color = int(layer.get("color", 7))
        if name not in doc.layers:
            doc.layers.add(name=name, color=color)


def extract_layers(doc: ezdxf.EzDxf, used_layers: set[str]) -> List[Dict[str, Any]]:
    layers = []
    for name in sorted(used_layers):
        if name == "0":
            layers.append({"name": "0", "color": 7})
            continue
        try:
            layer = doc.layers.get(name)
            color = int(layer.dxf.color)
        except Exception:
            color = 7
        layers.append({"name": name, "color": color})
    return layers


def entity_to_yaml(entity: Any, index: int) -> Dict[str, Any] | None:
    etype = entity.dxftype()
    layer = entity.dxf.layer

    if etype == "LINE":
        return {
            "id": f"E{index:03d}",
            "type": "line",
            "layer": layer,
            "start": as_point2(entity.dxf.start),
            "end": as_point2(entity.dxf.end),
        }

    if etype == "CIRCLE":
        return {
            "id": f"E{index:03d}",
            "type": "circle",
            "layer": layer,
            "center": as_point2(entity.dxf.center),
            "radius": round(float(entity.dxf.radius), 6),
        }

    if etype == "ARC":
        return {
            "id": f"E{index:03d}",
            "type": "arc",
            "layer": layer,
            "center": as_point2(entity.dxf.center),
            "radius": round(float(entity.dxf.radius), 6),
            "start_angle": round(float(entity.dxf.start_angle), 6),
            "end_angle": round(float(entity.dxf.end_angle), 6),
        }

    if etype == "LWPOLYLINE":
        return {
            "id": f"E{index:03d}",
            "type": "polyline",
            "layer": layer,
            "points": [as_point2(p) for p in entity.get_points(format="xy")],
            "closed": bool(entity.closed),
        }

    if etype == "TEXT":
        return {
            "id": f"E{index:03d}",
            "type": "text",
            "layer": layer,
            "value": entity.plain_text(),
            "insert": as_point2(entity.dxf.insert),
            "height": round(float(entity.dxf.height), 6),
        }

    return None


def dxf_to_yaml_data(dxf_path: str | Path) -> Dict[str, Any]:
    doc = ezdxf.readfile(dxf_path)
    msp = doc.modelspace()
    entities = []
    used_layers: set[str] = set()
    ignored = []

    for i, entity in enumerate(msp, start=1):
        item = entity_to_yaml(entity, i)
        if item is None:
            ignored.append(entity.dxftype())
            continue
        entities.append(item)
        used_layers.add(item.get("layer", "0"))

    return {
        "version": 1,
        "meta": {
            "source": Path(dxf_path).name,
            "description": "由简单 DXF 自动提取的 YAML。仅覆盖 demo 支持的 CAD 实体。",
            "supported_entities": ["line", "circle", "arc", "polyline", "text"],
            "ignored_entity_types": sorted(set(ignored)),
        },
        "drawing": {
            "units": "mm",
            "dxf_version": "R2010",
        },
        "layers": extract_layers(doc, used_layers),
        "entities": entities,
    }


def add_entity_from_yaml(msp: ezdxf.layouts.Modelspace, item: Dict[str, Any]) -> None:
    etype = str(item.get("type", "")).lower()
    layer = str(item.get("layer", "0"))
    attribs = {"layer": layer}

    if etype == "line":
        msp.add_line(pt_tuple(item["start"]), pt_tuple(item["end"]), dxfattribs=attribs)
        return

    if etype == "circle":
        msp.add_circle(pt_tuple(item["center"]), float(item["radius"]), dxfattribs=attribs)
        return

    if etype == "arc":
        msp.add_arc(
            center=pt_tuple(item["center"]),
            radius=float(item["radius"]),
            start_angle=float(item["start_angle"]),
            end_angle=float(item["end_angle"]),
            dxfattribs=attribs,
        )
        return

    if etype == "polyline":
        points = [pt_tuple(p) for p in item["points"]]
        msp.add_lwpolyline(points, close=bool(item.get("closed", False)), dxfattribs=attribs)
        return

    if etype == "text":
        text = msp.add_text(
            str(item.get("value", "")),
            height=float(item.get("height", 20)),
            dxfattribs=attribs,
        )
        text.set_placement(pt_tuple(item["insert"]), align=TextEntityAlignment.LEFT)
        return

    raise ValueError(f"不支持的 YAML 实体类型: {etype}")


def yaml_data_to_dxf(data: Dict[str, Any], output_path: str | Path) -> None:
    version = data.get("drawing", {}).get("dxf_version", "R2010")
    doc = ezdxf.new(version)
    setup_layers(doc, data.get("layers", []))
    msp = doc.modelspace()

    for item in data.get("entities", []):
        add_entity_from_yaml(msp, item)

    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    doc.saveas(output_path)


def canonical_entity(entity: Any) -> Dict[str, Any] | None:
    item = entity_to_yaml(entity, 0)
    if item is None:
        return None
    item.pop("id", None)

    # LINE 的起点终点方向不影响几何结果，因此排序后再比较。
    if item["type"] == "line":
        a, b = item["start"], item["end"]
        if tuple(a) > tuple(b):
            item["start"], item["end"] = b, a

    return item


def canonical_dxf(path: str | Path) -> List[Dict[str, Any]]:
    doc = ezdxf.readfile(path)
    records = []
    for entity in doc.modelspace():
        item = canonical_entity(entity)
        if item is not None:
            records.append(item)
    return sorted(records, key=lambda x: json.dumps(x, ensure_ascii=False, sort_keys=True))


def numbers_close(a: Any, b: Any, tol: float) -> bool:
    if isinstance(a, (int, float)) and isinstance(b, (int, float)):
        return math.isclose(float(a), float(b), rel_tol=0, abs_tol=tol)
    if isinstance(a, list) and isinstance(b, list) and len(a) == len(b):
        return all(numbers_close(x, y, tol) for x, y in zip(a, b))
    if isinstance(a, dict) and isinstance(b, dict) and set(a.keys()) == set(b.keys()):
        return all(numbers_close(a[k], b[k], tol) for k in a)
    return a == b


def compare_dxf(original_path: str | Path, generated_path: str | Path, tolerance: float = 1e-6) -> Dict[str, Any]:
    original = canonical_dxf(original_path)
    generated = canonical_dxf(generated_path)

    diffs = []
    if len(original) != len(generated):
        diffs.append({
            "type": "entity_count_mismatch",
            "original_count": len(original),
            "generated_count": len(generated),
        })

    max_len = max(len(original), len(generated))
    for i in range(max_len):
        if i >= len(original):
            diffs.append({"type": "extra_generated_entity", "index": i, "generated": generated[i]})
            continue
        if i >= len(generated):
            diffs.append({"type": "missing_generated_entity", "index": i, "original": original[i]})
            continue
        if not numbers_close(original[i], generated[i], tolerance):
            diffs.append({
                "type": "entity_mismatch",
                "index": i,
                "original": original[i],
                "generated": generated[i],
            })

    return {
        "passed": len(diffs) == 0,
        "tolerance": tolerance,
        "original": str(original_path),
        "generated": str(generated_path),
        "original_entity_count": len(original),
        "generated_entity_count": len(generated),
        "diff_count": len(diffs),
        "diffs": diffs,
    }
