# 小红书图文创作

[English](./README.en.md)

`xiaohongshu-content-creator` 是一个跨 Agent 的小红书图文创作技能，不绑定特定编码助手或运行时。Claude Code、OpenCode、OpenClaw、Hermes、Codex，以及其他能够读取 `SKILL.md` 并调用本地脚本或生图工具的 Agent 都可以使用。

技能负责：

- 调研与事实核验
- 小红书标题、正文和标签
- 用“认知锚点”筛选真正值得成页的内容
- 原创视觉隐喻、文案和分镜
- 3:4 封面与 9:16 内页
- 可选择的 IP 与视觉风格档案
- 让所选 IP 承担每页核心动作
- 无生图工具时的本地 SVG → PNG 降级
- 带明确修复动作的发布前 QA

## 自动选择执行路径

### 有生图工具

默认使用生图工具。每个项目先选择一个 `visual_profile`，每次生图只传入该档案的一张 `character-sheet.png`，不会同时传多个角色参考。先生成封面和一张代表性内页，确认角色、隐喻和风格后再生成整套。

分页不按原文段落平均分配，而是选择会改变读者理解的“认知锚点”。每页用三步法从抽象概念找到物理动作和日常物件，再让角色执行这个动作，形成当前主题独有的视觉隐喻。

内置两套视觉档案：

| `visual_profile` | IP | 默认风格 |
|---|---|---|
| `alpaca-line-art`（默认） | 白色羊驼创作者 | 纯白背景、黑色细线手绘、大量留白、少量蓝色强调 |
| `glasses-chibi-blue` | 原眼镜漫画主持人 | 暖米白纸张、较完整的漫画平涂、钴蓝笔刷与浅蓝卡片 |

角色资产分别放在 `assets/characters/<profile-id>/character-sheet.png`。新增 IP 时只需增加资产与 `references/visual-profiles.json` 中的档案配置，现有工作流无需重写。

### 没有生图工具

自动使用原 `free-imagegen` 本地渲染能力，生成中文稳定、可复现的知识卡式 PNG。它是完整的本地降级方案，但不会伪装成模型生成的漫画插画。

### 用户明确反馈文字错误

先尝试局部图片编辑或重绘。问题仍未解决时，才使用 SVG 文字覆盖工具修复指定区域。主流程不会为了预防错字而提前拆分文字和插画。

## 小红书默认规格

| 图片 | 比例 | 推荐尺寸 |
|---|---:|---:|
| 封面 | 3:4 | 1080 × 1440 |
| 内页 | 9:16 | 1080 × 1920 |

默认生成 1 张封面和 5–8 张内页，一页只讲一个核心观点。

## 核心创作机制

- **认知锚点选页**：只保留核心判断、认知转折、关键对比、断点、边界、常见误区和状态变化；删掉不影响理解的页。
- **角色承担动作**：如果去掉所选角色后隐喻仍完全成立，就重写分镜，让角色真正造成、阻断、修复、转换或揭示结果。
- **原创视觉隐喻三步法**：抽象概念 → 物理动作 → 日常低科技物件；每页一个主结构，不复刻旧构图。
- **修复闭环 QA**：每个问题都记录“缺陷 → 修复动作 → 复检结果”，而不只输出检查清单。

## 在不同 Agent 中使用

克隆仓库：

```bash
git clone https://github.com/NimaChu/xiaohongshu-content-creator.git
cd xiaohongshu-content-creator
```

根据 Claude Code、OpenCode、OpenClaw、Hermes、Codex 或其他 Agent 的技能目录约定安装本仓库，或者直接让 Agent 读取仓库根目录的 `SKILL.md`。如果当前 Agent 支持 `$skill-name` 调用方式，可以直接使用：

```text
使用 $xiaohongshu-content-creator，先调研“RAG 为什么不是给模型安装知识”，
再生成一张 3:4 封面和 6 张 9:16 小红书漫画科普图。
```

如果不支持 `$skill-name`，可以改为：

```text
请读取本仓库的 SKILL.md，先调研“RAG 为什么不是给模型安装知识”，
再生成一张 3:4 封面和 6 张 9:16 小红书漫画科普图。
```

技能会根据当前 Agent 可用的工具自动决定使用生图模型还是本地渲染，不需要用户提前选择模式。

## 项目产物

```text
output/<topic>/
├── project.json
├── research.md
├── post.md
├── storyboard.md
├── prompts/
├── images/
│   ├── cover.png
│   ├── page-01.png
│   └── ...
└── qa-report.md
```

## 本地渲染

校验项目：

```bash
python3 scripts/validate_project.py references/project.template.json
```

生成本地图片：

```bash
python3 scripts/render_xiaohongshu_project.py \
  references/project.template.json \
  --output-dir output/terminal
```

只生成本地渲染提示词：

```bash
python3 scripts/render_xiaohongshu_project.py \
  references/project.template.json \
  --output-dir output/terminal \
  --prompts-only
```

生成生图模型使用的逐页 Prompt：

```bash
python3 scripts/make_prompt_pack.py \
  references/project.template.json \
  --output-dir output/terminal/prompts
```

## 局部文字修复

仅在用户明确指出文字问题后使用：

```bash
python3 scripts/patch_image_text.py \
  --input output/terminal/images/page-01.png \
  --output output/terminal/images/page-01-fixed.png \
  --visual-profile alpaca-line-art \
  --x 100 --y 300 --width 880 --height 180 \
  --text "正确文字"
```

工具默认拒绝覆盖原图，并从视觉档案读取补丁背景色；可用 `--background` 覆盖。

## 兼容性

原 `scripts/free_image_gen.py` 和 Story Plan 接口继续保留，已有本地工作流仍可使用。`agents/openai.yaml` 只提供支持该元数据格式的客户端界面信息，不限制其他 Agent 使用本技能。

## 测试

```bash
python3 -m unittest discover -s tests -v
python3 scripts/validate_project.py references/project.template.json
```

## License

MIT
