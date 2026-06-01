# Simple DXF ↔ YAML Roundtrip Demo

这是一个最小可运行 demo，用来验证下面这条技术路线：

```text
原始 DXF → 自动提取 YAML → YAML 重新生成 DXF → 与原始 DXF 做一致性校验
```

这个 demo 的目标不是覆盖所有 CAD 能力，而是证明一件事：**可以先把简单 DXF 抽象成可读、可编辑、可由 AI 生成的 YAML，再通过 Python 生成 DXF，并用程序验证生成结果是否正确。**

---

## 1. 项目结构

```text
simple-dxf-yaml-roundtrip-demo/
├── examples/
│   ├── original_simple.dxf        # 原始 DXF
│   └── simple_from_dxf.yaml       # 由原始 DXF 自动提取出的 YAML
├── outputs/
│   ├── regenerated_from_yaml.dxf  # 由 YAML 重新生成的 DXF
│   ├── validation_report.json     # 正确性校验报告
│   └── original_vs_regenerated.png# 原始/生成图的预览对比
├── scripts/
│   ├── create_original_dxf.py     # 创建一个简单原始 DXF
│   ├── dxf_to_yaml.py             # DXF → YAML
│   ├── yaml_to_dxf.py             # YAML → DXF
│   ├── verify_dxf.py              # 原始 DXF vs 生成 DXF 校验
│   ├── render_preview.py          # 生成预览图
│   ├── run_demo.py                # 一键跑完整流程
│   └── cad_yaml_common.py         # 公共解析、生成、比较函数
├── docs/
│   ├── workflow.md                # 流程说明
│   ├── yaml_format.md             # YAML 格式说明
│   └── github_publish.md          # GitHub 上传说明
├── requirements.txt
├── .gitignore
├── LICENSE
└── README.md
```

---

## 2. 安装依赖

```bash
python -m venv .venv

# Windows
.venv\Scripts\activate

# macOS / Linux
source .venv/bin/activate

pip install -r requirements.txt
```

---

## 3. 一键运行完整 demo

```bash
python scripts/run_demo.py
```

运行后会依次执行：

```text
1. 创建 examples/original_simple.dxf
2. 从 original_simple.dxf 提取 examples/simple_from_dxf.yaml
3. 从 simple_from_dxf.yaml 生成 outputs/regenerated_from_yaml.dxf
4. 对比原始 DXF 和生成 DXF，输出 outputs/validation_report.json
5. 生成 outputs/original_vs_regenerated.png 预览图
```

如果校验通过，终端会输出：

```text
PASS
```

---

## 4. 单独运行每一步

### 4.1 创建一个简单原始 DXF

```bash
python scripts/create_original_dxf.py
```

### 4.2 原始 DXF 转 YAML

```bash
python scripts/dxf_to_yaml.py examples/original_simple.dxf -o examples/simple_from_dxf.yaml
```

### 4.3 YAML 重新生成 DXF

```bash
python scripts/yaml_to_dxf.py examples/simple_from_dxf.yaml -o outputs/regenerated_from_yaml.dxf
```

### 4.4 校验两个 DXF 是否一致

```bash
python scripts/verify_dxf.py examples/original_simple.dxf outputs/regenerated_from_yaml.dxf -o outputs/validation_report.json
```

---

## 5. YAML 示例

当前 demo 生成的 YAML 很简单：

```yaml
version: 1
drawing:
  units: mm
  dxf_version: R2010
layers:
- name: OUTLINE
  color: 7
- name: HOLE
  color: 1
entities:
- id: E001
  type: polyline
  layer: OUTLINE
  points:
  - [0.0, 0.0]
  - [160.0, 0.0]
  - [160.0, 80.0]
  - [0.0, 80.0]
  closed: true
- id: E002
  type: circle
  layer: HOLE
  center: [40.0, 40.0]
  radius: 8.0
```

目前支持的简单实体：

```text
line       直线
circle     圆
arc        圆弧
polyline   多段线
text       单行文字
```

---

## 6. 校验逻辑

`verify_dxf.py` 会把两个 DXF 都转成标准化后的实体列表，再进行比较。它会比较：

```text
实体数量
实体类型
图层 layer
坐标 start/end/center/points
半径 radius
文字内容 value
文字高度 height
```

默认容差是：

```text
1e-6
```

校验报告示例：

```json
{
  "passed": true,
  "original_entity_count": 6,
  "generated_entity_count": 6,
  "diff_count": 0,
  "diffs": []
}
```

---

## 7. 当前 demo 的边界

这个 demo 是故意做得很简单的，它暂时不处理：

```text
DWG 文件
块 BLOCK / INSERT
尺寸标注 DIMENSION
填充 HATCH
样条曲线 SPLINE
复杂文字 MTEXT
线型、线宽、颜色覆盖
AutoCAD 扩展数据
布局空间 Paper Space
```

后续可以逐步扩展为：

```text
DXF → 业务 YAML → 参数化组件 → 化工 CAD 自动绘图
```

比如：

```yaml
components:
- type: connection_plate
  width: 160
  height: 80
  holes:
  - center: [40, 40]
    radius: 8
  - center: [120, 40]
    radius: 8
```

这样就可以从“基础图元 YAML”升级成“业务组件 YAML”。

---


```
