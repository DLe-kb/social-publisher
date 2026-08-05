# Social Publisher

Social Publisher 是一个免费、本机优先、带人工授权门禁的多平台视频发布 Skill。它使用统一发布包校验和准备 B站、抖音、小红书、视频号、YouTube、X 与 TikTok 的发布任务。

当前实现重点是可审查的发布编排，不承诺所有平台都能稳定无人值守发布。B站复用已有 `biliup`，YouTube 使用官方 Data API；其他平台当前以本机可见浏览器为主，并保留人工检查和最终确认。

## 能力

- 统一发布包和平台差异字段。
- 视频、封面、标题、正文与标签预检。
- `dry-run（试运行）`、明确授权和最终确认。
- 任务指纹、防重复发布、运行报告和稳定性汇总。
- 凭证、Cookie、OAuth token、截图和运行记录全部保存在仓库外。

## 当前验证状态

| 平台 | 当前状态 |
| --- | --- |
| B站 | 外部 `biliup` 路线，未在本仓库重新实现 |
| 抖音 | 已完成一次仅自己可见的真实发布闭环；浏览器 Adapter 仍需跨日稳定性验证 |
| 小红书 | 原型受页面状态识别阻塞，需按独立 Adapter 架构重构 |
| 视频号 | 尚未完成真实账号验证 |
| YouTube | 官方 API 代码与离线校验已具备，尚未完成真实 OAuth 上传 |
| X | 免费浏览器路线尚未完成真实账号验证 |
| TikTok | 免费浏览器路线尚未完成真实账号验证 |

因此当前版本应视为 `experimental（实验性）`，不要直接用于核心账号无人值守发布。

## 仓库结构

```text
social-publisher/
├── SKILL.md
├── agents/
├── assets/
├── references/
├── scripts/
├── docs/
├── examples/
├── tests/
└── .github/workflows/
```

## 安装

```bash
git clone https://github.com/DLe-kb/social-publisher.git
cd social-publisher
python3 scripts/bootstrap_runtime.py
```

将仓库作为 Codex Skill 使用时，可把仓库目录链接到用户级 Skill 目录：

```bash
ln -s /absolute/path/to/social-publisher ~/.agents/skills/social-publisher
```

完整用法见 [使用说明](docs/README-使用说明.md)。

## 快速验证

```bash
python3 scripts/validate_repo.py
python3 -m unittest discover -s tests -p "test_*.py"
python3 scripts/social_publish.py doctor
python3 scripts/social_publish.py validate examples/publish-package.example.json \
  --platform youtube --metadata-only
```

## 安全边界

- `validate` 和 `prepare` 不执行最终发布。
- 正式发布必须同时使用 `--execute --authorized`，并在可见页面再次输入 `PUBLISH`。
- 不绕过验证码、二次验证、平台审核或风控提示。
- 发布结果无法回读时记录为 `uncertain（结果不确定）`，不得自动重试。
- 不要在 issue、日志或提交中包含真实凭证、账号资料、私人路径和业务素材。

## 开源协议

本仓库使用 [MIT License](LICENSE)。
