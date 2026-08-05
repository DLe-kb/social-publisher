#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
import re
import sys


ROOT = Path(__file__).resolve().parents[1]


def fail(message: str) -> None:
    raise SystemExit(f"ERROR: {message}")


def main() -> int:
    required = [
        "SKILL.md",
        "agents/openai.yaml",
        "assets/publish-package.example.json",
        "references/platform-fields.md",
        "references/platform-routes.md",
        "references/platform-references_平台参考.md",
        "references/security-and-status.md",
        "scripts/bootstrap_runtime.py",
        "scripts/platform_specs.json",
        "scripts/requirements.txt",
        "scripts/social_publish.py",
        "tests/test_social_publisher.py",
        "README.md",
        "LICENSE",
        "SECURITY.md",
    ]
    missing = [path for path in required if not (ROOT / path).is_file()]
    if missing:
        fail(f"missing files: {', '.join(missing)}")

    skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
    if not skill.startswith("---\n") or "\nname: social-publisher\n" not in skill:
        fail("SKILL.md frontmatter is invalid")

    specs = json.loads((ROOT / "scripts/platform_specs.json").read_text(encoding="utf-8"))
    expected = {"bilibili", "douyin", "xiaohongshu", "wechat-channels", "youtube", "x", "tiktok"}
    if set(specs) != expected:
        fail("platform set is incorrect")
    if any(not data.get("free") for data in specs.values()):
        fail("all default routes must remain free")
    if specs["x"].get("default_route") != "browser-local-free":
        fail("X default route must not require a paid API")
    if specs["youtube"].get("default_route") != "youtube-data-api-free-quota":
        fail("YouTube must use the free API quota route")

    forbidden = [
        re.compile(r"gho_[A-Za-z0-9_]+"),
        re.compile(r"AIza[0-9A-Za-z_-]{20,}"),
        re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
        re.compile(r"/Users/[^/\s]+/"),
    ]
    text_files = [
        path
        for path in ROOT.rglob("*")
        if path.is_file()
        and ".git" not in path.parts
        and path != Path(__file__).resolve()
    ]
    for path in text_files:
        try:
            content = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        for pattern in forbidden:
            if pattern.search(content):
                fail(f"sensitive or private value pattern found in {path.relative_to(ROOT)}")

    print("Repository validation passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
