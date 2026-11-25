#!/usr/bin/env python3
# SPDX-License-Identifier: Unlicense
"""Make this template a headset of its own: its codename, name and SoC everywhere, once.

    python scripts/new-headset.py CODENAME "Headset name" "SoC name"

CODENAME is the vendor's internal name for the headset, a lowercase Python identifier (the repository is
overpressure/CODENAME, cloned into devices/CODENAME). It replaces the template's myheadset, MyHeadset,
MYHEADSET_, "My Headset" and "My SoC" in every file of the repository, then removes TEMPLATE.md and itself. Run
it once, right after creating the repository from the template; then commit. In URLs (the README's chat badge)
"My%20Headset" becomes the name with its spaces and other characters escaped.
"""

from __future__ import annotations

import re
import subprocess
import sys
import urllib.parse
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CODENAME = re.compile(r"[a-z][a-z0-9_]*")


def replacements(codename: str, name: str, soc: str) -> list[tuple[str, str]]:
    """Return the template's words and what they become, the longest first."""
    camel = "".join(part.capitalize() for part in codename.split("_"))
    return [
        ("My%20Headset", urllib.parse.quote(name, safe="")),
        ("MYHEADSET_", codename.upper() + "_"),
        ("MyHeadset", camel),
        ("My Headset", name),
        ("My SoC", soc),
        ("myheadset", codename),
    ]


def tracked() -> list[Path]:
    """Return the repository's files, as Git knows them."""
    out = subprocess.run(["git", "-C", str(ROOT), "ls-files", "-z"], capture_output=True, check=True)  # noqa: S603, S607  # git from PATH, no shell
    return [ROOT / name for name in out.stdout.decode().split("\0") if name]


def main(argv: list[str]) -> int:
    """Rename the template once."""
    if len(argv) != 3 or not CODENAME.fullmatch(argv[0]):  # noqa: PLR2004  # codename, name, SoC
        print(__doc__, file=sys.stderr)
        return 2
    words = replacements(*argv)
    me = Path(__file__).resolve()
    guide = ROOT / "TEMPLATE.md"
    for path in tracked():
        if path.resolve() in (me, guide.resolve()) or not path.is_file():
            continue
        try:
            text = path.read_bytes().decode("utf-8")
        except UnicodeDecodeError:
            continue  # a binary file
        changed = text
        for old, new in words:
            changed = changed.replace(old, new)
        if changed != text:
            path.write_bytes(changed.encode("utf-8"))
            print(f"  {path.relative_to(ROOT).as_posix()}")
    guide.unlink(missing_ok=True)
    me.unlink()
    print(f"The template is {argv[1]} ({argv[0]}) now: review the changes, then commit.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
