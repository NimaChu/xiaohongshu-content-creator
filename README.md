# 小红书图文创作

[English](./README.en.md)

`xiaohongshu-content-creator` 是一个跨 Agent 的小红书图文创作技能，不绑定特定编码助手或运行时。Claude Code、OpenCode、OpenClaw、Hermes、Codex，以及其他能够读取 `SKILL.md` 并调用本地脚本或生图工具的 Agent 都可以使用。

技能负责：

- 调研与事实核验
- 小红书标题、正文和标签
- 分页、文案和分镜
- 3:4 封面与 9:16 内页
- 统一角色的漫画科普图
- 无生图工具时的本地 SVG → PNG 降级
- 发布前的文字、比例、事实和角色一致性检查

## 自动选择执行路径

### 有生图工具

默认使用生图工具，沿用固定眼镜漫画主持人、米白背景、黑色大标题和钴蓝强调色。先生成封面和一张代表性内页，确认风格后再生成整套。

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
  --x 100 --y 300 --width 880 --height 180 \
  --text "正确文字"
```

工具默认拒绝覆盖原图。

## 兼容性

原 `scripts/free_image_gen.py` 和 Story Plan 接口继续保留，已有本地工作流仍可使用。`agents/openai.yaml` 只提供支持该元数据格式的客户端界面信息，不限制其他 Agent 使用本技能。

## 测试

```bash
python3 -m unittest discover -s tests -v
python3 scripts/validate_project.py references/project.template.json
```

## License

MIT
