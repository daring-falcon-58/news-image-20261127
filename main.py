#!/usr/bin/env python3
"""news-image-20261127 round 3 entrypoint.

Copies the pre-rendered entry.png (drawn by build_image.py, same repo) to
$MAKEFUN_OUTPUT_DIR/entry.png after a JPEG magic-byte sanity check.
Python 3.13, standard library only. No network, no clock, no randomness:
two runs write identical bytes.
"""

import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "out")
    os.makedirs(out_dir, exist_ok=True)
    src = os.path.join(HERE, "entry.png")
    with open(src, "rb") as f:
        head = f.read(2)
    if head != b"\xff\xd8":
        sys.exit("entry.png is not a JPEG (bad magic bytes)")
    dst = os.path.join(out_dir, "entry.png")
    shutil.copyfile(src, dst)
    print("wrote %s (%d bytes)" % (dst, os.path.getsize(dst)))


if __name__ == "__main__":
    main()
