#!/usr/bin/env python3
"""Рендерить PSD-макет у PNG-прев'ю для візуальної перевірки та структури шарів.

Використання:
    python tools/render_psd.py Main.psd                  # -> Main-preview.png
    python tools/render_psd.py path/to/mockup.psd -o out.png
    python tools/render_psd.py Main.psd --scale 0.5      # менше прев'ю

Виводить розмір полотна і дерево верхньорівневих шарів (секції макета) —
те, що агенту потрібно, щоб зрозуміти структуру макета без відкриття PSD.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path


def main() -> int:
    ap = argparse.ArgumentParser(description="Render a PSD mockup to PNG preview")
    ap.add_argument("psd", type=Path, help="path to .psd file")
    ap.add_argument("-o", "--out", type=Path, default=None, help="output PNG (default: <name>-preview.png)")
    ap.add_argument("--scale", type=float, default=1.0, help="resize factor for the preview (default 1.0)")
    args = ap.parse_args()

    if not args.psd.is_file():
        print(f"error: file not found: {args.psd}", file=sys.stderr)
        return 1

    try:
        from psd_tools import PSDImage
    except ImportError:
        print("error: psd-tools is not installed -> pip install psd-tools", file=sys.stderr)
        return 1

    out = args.out or args.psd.with_name(f"{args.psd.stem}-preview.png")

    print(f"opening {args.psd} ...")
    psd = PSDImage.open(args.psd)
    print(f"canvas: {psd.width}x{psd.height}, color mode: {psd.color_mode.name}, top-level layers: {len(psd)}")

    print("top-level layers (sections of the mockup):")
    for i, layer in enumerate(psd):
        x1, y1, x2, y2 = layer.bbox  # psd-tools returns a plain tuple
        print(f"  [{i:02d}] {layer.kind:<8} {layer.name!r}  bbox=({x1},{y1})-({x2},{y2})")

    print("compositing ...")
    img = psd.composite()
    if args.scale != 1.0:
        img = img.resize((max(1, int(img.width * args.scale)), max(1, int(img.height * args.scale))))
    img.save(out, "PNG")
    print(f"saved: {out} ({img.width}x{img.height})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
