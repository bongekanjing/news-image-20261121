#!/usr/bin/env python3
"""news-image-20261121 — a square (1024x1024) one-page newspaper summing
up the world's news of Saturday 21 November 2026 (plus 12 breaking
stories from Sunday 22 November, woven in).

The picture itself was composed as HTML/CSS in news-20261121.html
(shipped in this repo) and rendered to entry.png with a headless
browser, so every headline, number and illustration is placed exactly
as designed. This program does not redraw the page: it delivers the
rendered entry.png as the program's output, copying it to
$MAKEFUN_OUTPUT_DIR/entry.png (default /output/entry.png) and exiting 0.

Pure standard library, no network, no randomness, no timestamps: two
runs produce byte-identical output, because the PNG is shipped beside
this file and copied verbatim.
"""

import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SOURCE = os.path.join(HERE, "entry.png")


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "entry.png")
    if not os.path.exists(SOURCE):
        print("entry.png not found beside main.py", file=sys.stderr)
        return 1
    shutil.copyfile(SOURCE, out_path)
    return 0


if __name__ == "__main__":
    sys.exit(main())
