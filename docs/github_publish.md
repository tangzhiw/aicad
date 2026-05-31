# GitHub 上传说明

## 1. 初始化仓库

在项目根目录执行：

```bash
git init
git add .
git commit -m "Initial DXF YAML roundtrip demo"
```

## 2. 创建 GitHub 远程仓库

在 GitHub 页面创建一个新仓库，例如：

```text
simple-dxf-yaml-roundtrip-demo
```

建议仓库描述：

```text
A minimal Python demo for converting simple DXF drawings to YAML, regenerating DXF from YAML, and validating the roundtrip result.
```

## 3. 推送到 GitHub

```bash
git branch -M main
git remote add origin https://github.com/你的用户名/simple-dxf-yaml-roundtrip-demo.git
git push -u origin main
```

## 4. 建议 README 展示重点

建议在 GitHub 首页重点展示：

```text
1. 项目目标：DXF ↔ YAML 往返转换
2. 一键运行命令：python scripts/run_demo.py
3. YAML 示例
4. PASS 校验报告
5. 原图/生成图预览
6. 当前支持范围和未来扩展方向
```

## 5. 后续可以添加的 GitHub 内容

```text
GitHub Actions：自动跑 roundtrip 校验
Issues 模板：记录不支持的 DXF 实体
examples：添加更多简单 DXF 示例
docs：补充业务组件 YAML 设计
```
