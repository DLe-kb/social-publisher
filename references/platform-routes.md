# 平台路线与费用边界

核验日期：2026-08-04。平台政策可能变化，真实接入前重新检查官方文档和账号控制台。

| 平台 | 免费默认路线 | 官方 API | 费用判断 | 主要限制 |
| --- | --- | --- | --- | --- |
| B站 | 已有 `biliup` | 不作为本 Skill 前置 | 工具免费 | 使用本地登录态，发布后回读 BV/AV/CID |
| 抖音 | 可见浏览器 | `video.create` | 有免费基础配额，额外流量可付费 | 权限默认关闭，需申请并让用户明确感知发布动作 |
| 小红书 | 可见浏览器 | 未发现普通创作者公开视频发布 API | 免费 | 页面变化和登录验证可能中断自动化 |
| 视频号 | 可见浏览器 | 未发现普通视频号公开视频发布 API | 免费 | 微信扫码、页面变化和账号权限可能中断自动化 |
| YouTube | YouTube Data API | YouTube Data API | 默认免费配额；默认约 100 次 `videos.insert`/日 | OAuth、项目配额和合规审查 |
| X | 可见浏览器 | X API | 新开发者为按量计费，无可规划的通用免费层 | 免费 Skill 不得要求配置 X API |
| TikTok | 可见浏览器 | Content Posting API | 未公布调用费 | 未审核客户端只能私密发布，公开发布需应用审核 |

## 路线选择

1. 抖音、小红书、视频号、X、TikTok 默认选择 `browser-local-free`。
2. 用户已经稳定使用 `biliup` 时，B站选择 `external-biliup`。
3. YouTube 固定选择 `youtube-data-api-free-quota`。
4. 只有用户明确要求、账号具备权限且不会产生未确认费用时，才为其他平台选择官方 API。
5. X API 必须同时满足“用户主动选择”和“用户确认费用”，否则拒绝切换。
6. 不接入声称免费但需要上传账号 Cookie 到第三方云端的服务。

## 权威来源

- 抖音开放平台：`video.create` 权限、上传与创建视频文档、付费常见问题。
- YouTube Data API：`videos.insert`、Quota Calculator、Quota and Compliance Audits。
- TikTok for Developers：Content Posting API、Query Creator Info、Content Sharing Guidelines。
- X Developer Console：当前费用和账户可用能力应以控制台为准；公共资料显示 2026 年新开发者采用 pay-per-use（按量计费）。
