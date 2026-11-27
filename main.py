#!/usr/bin/env python3
"""Entry point for make.fun news-image-20261127, round 5.

Copies the pre-built entry image (drawn by build_image.py in this
session) to $MAKEFUN_OUTPUT_DIR/entry.png. Standard library only, no
network, no clock reads: both runs write the same bytes.
"""
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "entry.png")


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "out")
    os.makedirs(out_dir, exist_ok=True)
    with open(SRC, "rb") as f:
        head = f.read(3)
    if head != b"\xff\xd8\xff":
        sys.exit("entry.png is not a JPEG (bad magic bytes)")
    with open(SRC, "rb") as f:
        tail = f.read()[-2:]
    if tail != b"\xff\xd9":
        sys.exit("entry.png is not a complete JPEG (no end marker)")
    shutil.copyfile(SRC, os.path.join(out_dir, "entry.png"))


if __name__ == "__main__":
    main()
