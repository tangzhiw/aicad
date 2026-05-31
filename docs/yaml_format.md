# YAML 格式说明

本 demo 使用的是非常简单的 YAML 格式，目标是让人和 AI 都容易理解。

## 1. 顶层结构

```yaml
version: 1
meta: {}
drawing: {}
layers: []
entities: []
```

说明：

```text
version   YAML 格式版本
meta      来源、描述、支持类型等元信息
drawing   图纸基础信息
layers    图层列表
entities  CAD 实体列表
```

---

## 2. drawing

```yaml
drawing:
  units: mm
  dxf_version: R2010
```

当前默认单位是 mm，DXF 版本为 R2010。

---

## 3. layers

```yaml
layers:
- name: OUTLINE
  color: 7
- name: HOLE
  color: 1
```

说明：

```text
name   图层名称
color  AutoCAD ACI 颜色编号
```

---

## 4. line

```yaml
- id: E001
  type: line
  layer: CENTER
  start: [0.0, 40.0]
  end: [160.0, 40.0]
```

---

## 5. circle

```yaml
- id: E002
  type: circle
  layer: HOLE
  center: [40.0, 40.0]
  radius: 8.0
```

---

## 6. arc

```yaml
- id: E003
  type: arc
  layer: OUTLINE
  center: [80.0, 40.0]
  radius: 20.0
  start_angle: 0
  end_angle: 180
```

---

## 7. polyline

```yaml
- id: E004
  type: polyline
  layer: OUTLINE
  points:
  - [0.0, 0.0]
  - [160.0, 0.0]
  - [160.0, 80.0]
  - [0.0, 80.0]
  closed: true
```

---

## 8. text

```yaml
- id: E005
  type: text
  layer: TEXT
  value: SIMPLE PLATE
  insert: [45.0, 92.0]
  height: 8.0
```

---

## 9. 为什么这个 YAML 比参数型 YAML 更适合 demo

之前的焊接 YAML 是“业务参数型 YAML”，例如连接板宽度、焊缝参数、塔径配置等。它需要额外的业务绘图模板才能生成 CAD。

本 demo 使用的是“基础图元型 YAML”，每个实体都能直接对应到一个 DXF 图元，所以更适合验证：

```text
DXF → YAML → DXF → 正确性校验
```

等这个闭环跑通后，再升级到业务参数型 YAML。
