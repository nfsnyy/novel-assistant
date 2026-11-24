"""novel.py - 小说创作工程初始化 CLI。

用法：python novel.py init <目录>

仅用 Python 3.11 标准库。初始化一个小说创作目录：
创建 manuscript / outline / characters / notes 四个子目录，
并写入 novel.json 项目元数据（format_version=1，project_name 为目录基名）。
已存在 novel.json 的目录拒绝重复初始化，且不做任何改动。
"""
import json
import sys
from pathlib import Path

USAGE = "usage: python novel.py init <目录>"

SUBDIRS = ["manuscript", "outline", "characters", "notes"]

NOVEL_JSON = "novel.json"

FORMAT_VERSION = 1


def cmd_init(target_arg):
    target = Path(target_arg)
    novel_json = target / NOVEL_JSON

    # 防覆盖红线：先检查再动手，保证拒绝时零改动。
    if novel_json.is_file():
        print(
            "error: %s 已存在，拒绝重复初始化（不会覆盖既有创作内容）" % novel_json,
            file=sys.stderr,
        )
        return 1

    # 目标目录（含缺失父目录）自动创建。
    target.mkdir(parents=True, exist_ok=True)

    for name in SUBDIRS:
        sub = target / name
        sub.mkdir(exist_ok=True)
        print(sub)

    data = {
        "format_version": FORMAT_VERSION,
        "project_name": target.name,
    }
    novel_json.write_text(
        json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(novel_json)
    return 0


def main(argv):
    args = argv[1:]
    if len(args) != 2 or args[0] != "init":
        print(USAGE, file=sys.stderr)
        print("初始化小说创作目录：python novel.py init <目录>", file=sys.stderr)
        return 2
    return cmd_init(args[1])


if __name__ == "__main__":
    sys.exit(main(sys.argv))
