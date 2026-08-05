from __future__ import annotations

from datetime import datetime, timezone
import importlib.util
import os
from pathlib import Path
import json
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "scripts" / "social_publish.py"
SPEC = importlib.util.spec_from_file_location("social_publish", MODULE_PATH)
assert SPEC and SPEC.loader
social_publish = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(social_publish)


class SocialPublisherTests(unittest.TestCase):
    def test_task_fingerprint_is_deterministic(self):
        first = social_publish.task_fingerprint("content", "douyin", "main", "abc")
        second = social_publish.task_fingerprint("content", "douyin", "main", "abc")
        changed = social_publish.task_fingerprint("content", "x", "main", "abc")
        self.assertEqual(first, second)
        self.assertNotEqual(first, changed)

    def test_account_alias_rejects_path_characters(self):
        with self.assertRaises(social_publish.PublishError):
            social_publish.safe_account_name("../../account")
        self.assertEqual(social_publish.safe_account_name("test-account_1"), "test-account_1")

    def test_unconfigured_field_is_not_treated_as_missing(self):
        result = social_publish.fill_configured(None, {}, "tags", "example")
        self.assertFalse(result["requested"])
        self.assertEqual(result["reason"], "field_not_configured_for_platform")

    def test_empty_douyin_topics_require_no_page(self):
        result = social_publish.add_douyin_topics(None, {}, None, [])
        self.assertFalse(result["requested"])
        self.assertFalse(result["filled"])

    def test_douyin_requires_both_cover_slots(self):
        with tempfile.TemporaryDirectory() as temporary:
            package_path = Path(temporary) / "package.json"
            package_path.write_text(json.dumps({
                "version": 1,
                "content_id": "cover-test",
                "video": "./missing.mp4",
                "platforms": {"douyin": {"title": "测试标题"}},
            }), encoding="utf-8")
            result = social_publish.validate_package(package_path, ["douyin"], metadata_only=True)
            self.assertIn("douyin: 缺少封面 vertical_3_4", result["errors"])
            self.assertIn("douyin: 缺少封面 horizontal_4_3", result["errors"])

    def test_stability_requires_three_published_days(self):
        records = [
            {
                "execute": True,
                "status": "published",
                "finished_at": f"2026-08-0{day}T01:00:00Z",
                "finished_at_unix": day,
            }
            for day in (1, 2, 3)
        ]
        result = social_publish.evaluate_stability(records)
        self.assertEqual(result["level"], "stable")
        self.assertEqual(result["published_days"], 3)

    def test_stability_does_not_accept_same_day_repeats(self):
        records = [
            {
                "execute": True,
                "status": "published",
                "finished_at": f"2026-08-01T0{hour}:00:00Z",
                "finished_at_unix": hour,
            }
            for hour in (1, 2, 3)
        ]
        self.assertEqual(social_publish.evaluate_stability(records)["level"], "conditional")

    def test_persist_run_keeps_history_and_latest_ledger(self):
        with tempfile.TemporaryDirectory() as temporary:
            previous = os.environ.get("SOCIAL_PUBLISHER_HOME")
            os.environ["SOCIAL_PUBLISHER_HOME"] = temporary
            try:
                payload = {
                    "platform": "douyin",
                    "account": "test",
                    "status": "prepared",
                    "finished_at_unix": 1,
                    "finished_at": "2026-08-01T00:00:00Z",
                }
                fingerprint = "abc123"
                first = social_publish.persist_run(payload, fingerprint)
                second = social_publish.persist_run(payload, fingerprint)
                self.assertNotEqual(first, second)
                self.assertTrue(first.is_file())
                self.assertTrue(second.is_file())
                self.assertEqual(
                    social_publish.load_previous_report(fingerprint)["status"],
                    "prepared",
                )
            finally:
                if previous is None:
                    os.environ.pop("SOCIAL_PUBLISHER_HOME", None)
                else:
                    os.environ["SOCIAL_PUBLISHER_HOME"] = previous

    def test_run_report_path_has_no_private_project_path(self):
        with tempfile.TemporaryDirectory() as temporary:
            previous = os.environ.get("SOCIAL_PUBLISHER_HOME")
            os.environ["SOCIAL_PUBLISHER_HOME"] = temporary
            try:
                path = social_publish.run_report_path(
                    "x",
                    "test-account",
                    "fingerprint",
                    datetime(2026, 8, 4, tzinfo=timezone.utc),
                )
                self.assertIn("runs/x/test-account", str(path))
            finally:
                if previous is None:
                    os.environ.pop("SOCIAL_PUBLISHER_HOME", None)
                else:
                    os.environ["SOCIAL_PUBLISHER_HOME"] = previous


if __name__ == "__main__":
    unittest.main()
