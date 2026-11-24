"""novel.py init 业务 unittest：成功 / 重复初始化 / 缺参三路径。"""
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
NOVEL = REPO_ROOT / "novel.py"
SUBDIRS = ["manuscript", "outline", "characters", "notes"]


def run_novel(args, cwd):
    return subprocess.run(
        [sys.executable, str(NOVEL), *args],
        cwd=str(cwd),
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        timeout=30,
    )


def snapshot(root):
    root = Path(root)
    dirs = sorted(p.relative_to(root).as_posix() for p in root.rglob("*") if p.is_dir())
    files = sorted(p.relative_to(root).as_posix() for p in root.rglob("*") if p.is_file())
    return {"dirs": dirs, "files": files}


class TestNovelInit(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory(prefix="novel-init-test-")
        self.addCleanup(self._tmp.cleanup)
        self.tmp = Path(self._tmp.name)

    def test_init_success(self):
        target = self.tmp / "nested" / "proj"
        proc = run_novel(["init", str(target)], cwd=self.tmp)
        self.assertEqual(proc.returncode, 0, proc.stderr)
        self.assertTrue(target.is_dir())
        for name in SUBDIRS:
            self.assertTrue((target / name).is_dir(), name)
        data = json.loads((target / "novel.json").read_text(encoding="utf-8"))
        self.assertEqual(data["format_version"], 1)
        self.assertEqual(data["project_name"], "proj")
        output = (proc.stdout or "") + (proc.stderr or "")
        for name in SUBDIRS + ["novel.json"]:
            self.assertIn(str(target / name), output)

    def test_reinit_refused_without_changes(self):
        target = self.tmp / "proj"
        first = run_novel(["init", str(target)], cwd=self.tmp)
        self.assertEqual(first.returncode, 0, first.stderr)
        user_file = target / "manuscript" / "chapter1.txt"
        user_file.write_text("用户已写内容，绝不允许被覆盖。\n", encoding="utf-8")
        before = snapshot(target)
        before_bytes = user_file.read_bytes()
        second = run_novel(["init", str(target)], cwd=self.tmp)
        self.assertNotEqual(second.returncode, 0)
        self.assertTrue((second.stdout or "").strip() or (second.stderr or "").strip())
        self.assertEqual(before, snapshot(target))
        self.assertEqual(user_file.read_bytes(), before_bytes)

    def test_missing_arg_usage_error(self):
        before = snapshot(self.tmp)
        proc = run_novel(["init"], cwd=self.tmp)
        self.assertNotEqual(proc.returncode, 0)
        output = ((proc.stdout or "") + (proc.stderr or "")).lower()
        self.assertIn("usage", output)
        self.assertEqual(before, snapshot(self.tmp))


if __name__ == "__main__":
    unittest.main()
