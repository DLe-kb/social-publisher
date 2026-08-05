---
name: social-publisher
description: Validate, prepare, and publish video packages to Bilibili, Douyin, Xiaohongshu, WeChat Channels, YouTube, X, and TikTok through free local browser workflows, the free YouTube Data API quota, and optional existing biliup integration. Use for multi-platform publishing, social video distribution, platform field adaptation, upload preparation, explicit-authorized publishing, publishing status checks, or requests involving 发布到抖音、小红书、视频号、YouTube、X、TikTok、B站.
---

# Social Publisher

使用免费的本机优先工作流，把同一视频发布包适配到多个社媒平台。默认使用可见浏览器和本地登录态，不要求购买 API、SaaS、代理服务或云发布套餐。

## 核心边界

- 默认路线必须免费；不要把 X API 或任何付费服务作为必需依赖。
- 登录态、Cookie、OAuth token 和浏览器 profile（配置档案）必须保存在 Skill 与内容项目之外。
- `validate` 和 `prepare` 不执行最终发布。
- 只有用户在当前对话明确授权后，才能运行 `publish --execute --authorized`。
- 不绕过验证码、二次验证、平台审核、账号权限或风控提示。
- 发布后没有作品 ID、URL 或明确成功反馈时，记录为 `uncertain（结果不确定）`，不要自动重试。
- 不把用户截图、账号头像、频道名或其他可识别信息提交到公共仓库。

## 工作流

1. 读取发布包 JSON，并确认目标账号、平台、视频、封面、文案和可见范围。
2. 运行免费路线诊断：

```bash
python3 scripts/bootstrap_runtime.py
<runtime_python> scripts/social_publish.py doctor
```

要求 Python 3.10 或更高版本。安装脚本会打印实际 `runtime_python` 路径，后续命令使用该解释器。

3. 校验字段和素材：

```bash
python3 scripts/social_publish.py validate /path/to/publish-package.json
```

4. 首次使用某个平台时建立本地登录态：

```bash
python3 scripts/social_publish.py login douyin --account main
```

YouTube 使用 Google OAuth 客户端文件授权：

```bash
python3 scripts/social_publish.py login youtube --account main \
  --client-secrets /path/to/client-secret.json
```

5. 先用试运行查看将执行的动作：

```bash
python3 scripts/social_publish.py prepare /path/to/publish-package.json \
  --platform douyin --account main --dry-run
```

6. 打开可见浏览器、上传并填写字段，停在最终发布前：

```bash
python3 scripts/social_publish.py prepare /path/to/publish-package.json \
  --platform douyin --account main
```

只有页面字段已填写、上传完成信号可确认，并且用户检查后输入 `READY`，才记录为 `prepared`。

7. 仅在用户明确确认后执行最终点击：

```bash
python3 scripts/social_publish.py publish /path/to/publish-package.json \
  --platform douyin --account main --execute --authorized
```

## 平台路线

- `bilibili`：保留并调用用户已有的 `biliup`，不要重新管理 B 站登录态。
- `douyin`、`xiaohongshu`、`wechat-channels`：默认使用本机 Playwright（浏览器自动化）。
- `youtube`：使用 YouTube Data API 的免费默认配额；不通过浏览器模拟上传。
- `x`：默认使用本机浏览器。X 官方 API 当前按量计费，不得作为免费模式依赖。
- `tiktok`：默认使用本机浏览器；Content Posting API 无公开调用费，但应用审核和公开发布权限不是免费模式的前置条件。

读取 [platform-routes.md](references/platform-routes.md) 了解费用和能力边界。读取 [platform-fields.md](references/platform-fields.md) 核对平台字段与规格。需要复核平台资料时读取 [platform-references_平台参考.md](references/platform-references_平台参考.md)。读取 [security-and-status.md](references/security-and-status.md) 处理凭证、重复发布和结果状态。

## 发布包

从 `assets/publish-package.example.json` 复制并按项目填写。平台特有字段放在 `platforms.<platform>` 中，不要强制所有平台共用完全相同的标题和正文。

发布包必须包含稳定的 `content_id`。脚本使用内容 ID、平台、账号别名和素材 SHA-256 生成任务指纹，避免同一任务被无意重复执行。

## 验收

- `doctor` 明确显示每个平台的免费默认路线和依赖状态。
- `validate` 能检查路径、字符限制、视频时长、文件大小、分辨率和封面比例。
- `prepare --dry-run` 不启动浏览器、不上传文件。
- `prepare` 使用可见浏览器并停在最终发布前。
- 缺少 `--execute --authorized` 时，`publish` 必须拒绝执行。
- API、浏览器页面或回读结果不明确时，不报告成功。
- 使用 `stability` 汇总仓库外的运行证据；最近三次真实发布必须跨三个日期且全部成功，才能标记为 `stable（稳定）`。
- 任何日志和示例都不包含真实凭证、私人路径或身份信息。

```bash
python3 scripts/social_publish.py stability --platform douyin --account main
```
