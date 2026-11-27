#!/usr/bin/env python3
"""news-image-20261127 round 2 — entry program (Python 3.13, stdlib only).

Copies the pre-rendered entry.png beside this file to
$MAKEFUN_OUTPUT_DIR/entry.png. The image was drawn in-session by
build_image.py (same repo), a deterministic PIL renderer: fixed data,
fixed geometry, no randomness, no network, no clock reads. Two runs of
the renderer are byte-identical, and this program just copies those bytes.
"""
import os
import shutil
import sys


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "output")
    os.makedirs(out_dir, exist_ok=True)
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, "entry.png")
    with open(src, "rb") as f:
        magic = f.read(3)
    if magic != b"\xff\xd8\xff":
        sys.exit("entry.png is not a JPEG (bad magic bytes)")
    shutil.copyfile(src, os.path.join(out_dir, "entry.png"))


if __name__ == "__main__":
    main()
