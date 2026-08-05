# Contributing

感谢你改进 Social Publisher。提交前请先说明目标平台、真实失败边界和验证方式。

## 贡献要求

- Skill 运行入口保留在根目录 `SKILL.md`，详细平台资料放入 `references/`。
- 平台选择器、字段规则和执行逻辑必须按平台隔离，避免把一个平台的页面假设复用到其他平台。
- 新增真实写入能力时，必须保留 dry-run、明确授权、最终确认和发布后回读。
- 凭证、Cookie、OAuth token、浏览器 profile、运行截图、账号名称和真实业务素材不得提交到仓库。
- 不复制许可证不明确的第三方项目代码；引用思路时保留来源链接和适用边界。

## 本地验证

```bash
python3 scripts/validate_repo.py
python3 -m unittest discover -s tests -p "test_*.py"
python3 scripts/social_publish.py doctor
```

浏览器 Adapter 的变更还应使用低风险账号先完成 `prepare`，再经明确授权进行私密或仅自己可见的真实发布验证。
