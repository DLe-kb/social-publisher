#!/usr/bin/env python3
from __future__ import annotations

import argparse
import os
from pathlib import Path
import shutil
import subprocess
import sys
import venv


SCRIPT_DIR = Path(__file__).resolve().parent
DEFAULT_HOME = Path.home() / ".config" / "social-publisher"
LEGACY_HOME = Path.home() / ".config" / "open-creator" / "social-publisher"


def default_runtime_home() -> Path:
    configured = os.environ.get("SOCIAL_PUBLISHER_HOME")
    if configured:
        return Path(configured)
    if LEGACY_HOME.exists() and not DEFAULT_HOME.exists():
        return LEGACY_HOME
    return DEFAULT_HOME


def main() -> int:
    if sys.version_info < (3, 10):
        print("Social Publisher requires Python 3.10 or newer.", file=sys.stderr)
        return 2

    parser = argparse.ArgumentParser(description="Install the free Social Publisher runtime")
    parser.add_argument(
        "--runtime-home",
        type=Path,
        default=default_runtime_home(),
    )
    parser.add_argument(
        "--install-browser",
        action="store_true",
        help="Download Playwright Chromium when no supported local browser is available",
    )
    parser.add_argument(
        "--upgrade-pip",
        action="store_true",
        help="Upgrade pip before installing dependencies",
    )
    parser.add_argument(
        "--index-url",
        help="Optional Python package index URL; the default remains the official package index",
    )
    parser.add_argument(
        "--venv-name",
        help="Optional runtime environment directory name",
    )
    args = parser.parse_args()

    runtime_home = args.runtime_home.expanduser().resolve()
    runtime_home.mkdir(parents=True, exist_ok=True, mode=0o700)
    environment_name = args.venv_name or f"venv-py{sys.version_info.major}{sys.version_info.minor}"
    if not environment_name.replace("-", "").replace("_", "").isalnum():
        print("Invalid --venv-name; use letters, numbers, hyphens, or underscores.", file=sys.stderr)
        return 2
    environment = runtime_home / environment_name
    uv = shutil.which("uv")
    if not environment.exists():
        if uv:
            subprocess.run(
                [uv, "venv", "--python", sys.executable, str(environment)],
                check=True,
            )
        else:
            venv.EnvBuilder(with_pip=True).create(environment)

    python = environment / "bin" / "python"
    common_pip_args = ["--timeout", "120", "--retries", "5"]
    if args.index_url:
        common_pip_args.extend(["--index-url", args.index_url])
    if args.upgrade_pip:
        subprocess.run(
            [str(python), "-m", "pip", "install", *common_pip_args, "--upgrade", "pip"],
            check=True,
        )
    if uv:
        command = [
            uv,
            "pip",
            "install",
            "--python",
            str(python),
            "-r",
            str(SCRIPT_DIR / "requirements.txt"),
        ]
        if args.index_url:
            command.extend(["--index-url", args.index_url])
    else:
        command = [
            str(python),
            "-m",
            "pip",
            "install",
            *common_pip_args,
            "-r",
            str(SCRIPT_DIR / "requirements.txt"),
        ]
    subprocess.run(command, check=True)
    if args.install_browser:
        subprocess.run([str(python), "-m", "playwright", "install", "chromium"], check=True)

    print(f"runtime_python={python}")
    print(f"doctor_command={python} {SCRIPT_DIR / 'social_publish.py'} doctor")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
