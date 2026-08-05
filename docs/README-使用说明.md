# Social Publisher 使用说明

`social-publisher` 是一个免费、本机优先的多平台视频发布 Skill。它把一个标准发布包适配到 B站、抖音、小红书、视频号、YouTube、X 和 TikTok，并在正式发布前保留明确的人类授权。

## 支持的平台与执行方式

| 平台 | 执行方式 |
| --- | --- |
| B站 | 调用用户已有的 `biliup`，Skill 不重新管理登录态 |
| 抖音 | 本机可见 Playwright 浏览器 |
| 小红书 | 本机可见 Playwright 浏览器 |
| 视频号 | 本机可见 Playwright 浏览器 |
| YouTube | YouTube Data API 免费默认配额 |
| X | 本机可见 Playwright 浏览器，不依赖付费 X API |
| TikTok | 本机可见 Playwright 浏览器，不要求应用审核 |

浏览器平台支持两步执行：`prepare` 自动上传和填写，`publish --execute --authorized` 在用户确认后点击最终发布按钮。YouTube 的 `prepare` 只校验发布内容，正式上传发生在授权后的 `publish`。

## 安装运行依赖

Skill 本身免费且开源。依赖也是开源软件，但平台账号、网络和内容权利由用户自行负责。

```bash
python3 scripts/bootstrap_runtime.py
```

要求 Python 3.10 或更高版本。依赖会安装到仓库外按 Python 版本隔离的虚拟环境。已有本机 Chrome 时，脚本会直接使用 Chrome；没有受支持浏览器时，增加 `--install-browser` 下载 Playwright Chromium。

下文的 `python3` 应替换为：

```text
bootstrap 输出的 runtime_python 路径
```

## 准备发布包

参考：

```text
assets/publish-package.example.json
```

不要把 OAuth 客户端文件、token、Cookie 或真实浏览器 profile 写进发布包。

## 诊断与校验

```bash
python3 scripts/social_publish.py doctor
```

```bash
python3 scripts/social_publish.py validate publish-package.json
```

只校验字段、不读取素材：

```bash
python3 scripts/social_publish.py validate \
  publish-package.json --metadata-only
```

## 浏览器平台

首次登录：

```bash
python3 scripts/social_publish.py login douyin --account main
```

免费试运行：

```bash
python3 scripts/social_publish.py prepare \
  publish-package.json --platform douyin --account main --dry-run
```

打开浏览器并填写，停在发布前：

```bash
python3 scripts/social_publish.py prepare \
  publish-package.json --platform douyin --account main
```

用户确认后发布：

```bash
python3 scripts/social_publish.py publish \
  publish-package.json --platform douyin --account main \
  --execute --authorized
```

脚本填写完成后仍会停在页面上。`prepare` 只有在人工检查并输入 `READY` 后才算通过；正式发布只有再次输入 `PUBLISH`，才会点击最终发布按钮。

浏览器路线会自动填写当前已适配的字段，但账号、视频预览、封面、可见范围、原创/版权声明和互动权限仍列为人工复核项。没有完成这些检查时不要输入 `READY` 或 `PUBLISH`。

把平台名替换为 `xiaohongshu`、`wechat-channels`、`x` 或 `tiktok`。

## YouTube

在 Google Cloud Console 创建 Desktop app（桌面应用）OAuth 客户端，启用 YouTube Data API v3，并把下载的客户端 JSON 保存在内容项目和 Git 仓库之外。

授权：

```bash
python3 scripts/social_publish.py login youtube \
  --account main --client-secrets /secure/path/client-secret.json
```

校验：

```bash
python3 scripts/social_publish.py prepare \
  publish-package.json --platform youtube --account main --dry-run
```

授权发布：

```bash
python3 scripts/social_publish.py publish \
  publish-package.json --platform youtube --account main \
  --client-secrets /secure/path/client-secret.json \
  --execute --authorized
```

OAuth token 默认保存在 `~/.config/social-publisher/oauth/`，权限设置为仅当前用户可读写。若本机已有旧目录 `~/.config/open-creator/social-publisher/`，程序会在新目录尚不存在时自动兼容使用旧目录。

## 结果与重复发布

每次运行报告保存在仓库外的 `runs/`，任务最新状态保存在 `ledgers/`。同一个 `content_id + platform + account + video SHA-256` 已产生 `published` 或 `uncertain` 记录时，脚本拒绝再次发布。只有人工确认平台没有创建作品后才能使用 `--force`。

浏览器点击后无法获得作品 ID、URL 或明确成功提示时，结果为 `uncertain`，不会自动重试。

查看稳定性证据：

```bash
python3 scripts/social_publish.py stability \
  --platform douyin --account main
```

最近三次真实执行必须全部成功并分布在三个不同日期，才会显示 `stable（稳定）`。一次成功或三次页面准备成功只会显示 `conditional（有条件可用）`。

## 兼容性与边界

浏览器平台使用本机登录态、可见浏览器和发布前人工确认。登录资料、截图和运行报告保存在仓库外，不随 Skill 分发。

平台页面会持续变化。选择器失效时应先更新并用低风险账号完成 `prepare` 验证，不要直接测试正式发布。
