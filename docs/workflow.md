# DXF → YAML → DXF → 校验流程说明

## 1. 为什么要做这个 demo

在 CAD 自动绘图场景中，如果直接让 AI 生成 DXF，结果通常不稳定，也不方便调试。

更合适的方式是：

```text
AI / 规则 / 程序 → YAML → Python 渲染器 → DXF
```

YAML 相当于一个中间层，它比 DXF 更容易读，也更容易被 AI 生成和人工修改。

---

## 2. 本 demo 的完整流程

```text
examples/original_simple.dxf
        ↓
scripts/dxf_to_yaml.py
        ↓
examples/simple_from_dxf.yaml
        ↓
scripts/yaml_to_dxf.py
        ↓
outputs/regenerated_from_yaml.dxf
        ↓
scripts/verify_dxf.py
        ↓
outputs/validation_report.json
```

---

## 3. 每个脚本的作用

### create_original_dxf.py

创建一个简单 DXF，里面包含：

```text
1 个矩形外轮廓
2 个圆孔
2 条中心线
1 个文字
```

### dxf_to_yaml.py

读取原始 DXF 中的 modelspace 实体，并转换成 YAML。

目前只提取 demo 支持的简单实体：

```text
LINE
CIRCLE
ARC
LWPOLYLINE
TEXT
```

### yaml_to_dxf.py

读取 YAML，并用 ezdxf 重新生成 DXF。

### verify_dxf.py

把原始 DXF 和重新生成的 DXF 都转换成标准化实体列表，然后比较两者是否一致。

### render_preview.py

生成一张 PNG，用于人工快速查看原始 DXF 和生成 DXF 的图形是否一致。

---

## 4. 校验方法

校验不是比较 DXF 文件文本内容，因为 DXF 文件里会有 handle、header、时间戳等非几何信息。

本 demo 采用的是“语义校验”：

```text
DXF A → 标准化实体列表
DXF B → 标准化实体列表
比较两个实体列表是否一致
```

这更适合 CAD 自动生成系统。

---

## 5. 后续扩展方向

第一阶段：基础图元 YAML

```text
line / circle / arc / polyline / text
```

第二阶段：业务组件 YAML

```text
connection_plate / nozzle / tray / tower_shell / distributor
```

第三阶段：AI 生成 YAML

```text
用户需求 → 大模型生成 YAML → Python 生成 DXF → 自动校验
```

第四阶段：误差分析与自动修复

```text
生成 DXF → 与标准 DXF 比较 → 生成差异报告 → 自动修正 YAML 或渲染器
```
