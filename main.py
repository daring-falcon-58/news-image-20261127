#!/usr/bin/env python3
"""news-image-20261127 round 4: copy the entry image to the output dir.

Standard library only. The image is drawn by build_image.py (fixed data,
fixed geometry, no randomness, no network, no clock reads); this program
only copies the bytes it already holds, after a JPEG magic-byte check.
Deterministic: two runs write identical bytes.
"""
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "entry.png")


def main():
    outdir = os.environ.get("MAKEFUN_OUTPUT_DIR", "out")
    os.makedirs(outdir, exist_ok=True)
    with open(SRC, "rb") as f:
        head = f.read(3)
        if head != b"\xff\xd8\xff":
            print("entry.png is not a JPEG (bad magic bytes)", file=sys.stderr)
            return 1
    dst = os.path.join(outdir, "entry.png")
    shutil.copyfile(SRC, dst)
    print(f"wrote {dst}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
