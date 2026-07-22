"""
_process_photo.py
Processes pic.jpeg:
  1. Removes background using rembg (onnxruntime-based, high quality)
  2. Crops to a centered square around the face + shoulders
  3. Creates a circular crop with transparent background + soft edge
  4. Saves pic-circle.png  (committed asset, used in SVGs via GitHub URL)
  5. Saves scripts/pic-b64.txt  (base64 data URI for inline SVG embedding)

Usage: python scripts/_process_photo.py
Run from repo root.
"""

import base64
import io
import os
import sys

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
from rembg import remove

SRC  = "pic.jpeg"
CIRC = "pic-circle.png"
B64  = "scripts/pic-b64.txt"
SIZE = 320   # final circle diameter in pixels


def remove_bg_rembg(src_path: str) -> Image.Image:
    """Use rembg for high-quality background removal."""
    with open(src_path, "rb") as f:
        raw = f.read()
    out = remove(raw)
    return Image.open(io.BytesIO(out)).convert("RGBA")


def make_circle(img_rgba: Image.Image, size: int) -> Image.Image:
    """Crop to square head+shoulder area, resize, apply circular alpha mask."""
    w, h = img_rgba.size

    # Crop: center-width, top ~88% of height (cuts off body, keeps head+chest)
    crop_h = int(h * 0.88)
    crop_w = min(w, crop_h)
    x_off  = (w - crop_w) // 2
    y_off  = 0
    cropped = img_rgba.crop((x_off, y_off, x_off + crop_w, y_off + crop_h))

    # Resize to target
    resized = cropped.resize((size, size), Image.Resampling.LANCZOS)

    # Circular alpha mask with soft anti-aliased edge
    mask = Image.new("L", (size, size), 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0, size - 1, size - 1), fill=255)
    mask = mask.filter(ImageFilter.GaussianBlur(radius=1.2))

    # Apply mask on top of existing alpha
    r, g, b, a = resized.split()
    a_new = Image.fromarray(
        np.minimum(np.array(a), np.array(mask)).astype(np.uint8)
    )
    return Image.merge("RGBA", (r, g, b, a_new))


def to_b64_uri(img: Image.Image) -> str:
    buf = io.BytesIO()
    img.save(buf, format="PNG", optimize=True)
    b64 = base64.b64encode(buf.getvalue()).decode("ascii")
    return f"data:image/png;base64,{b64}"


def main() -> None:
    if not os.path.exists(SRC):
        print(f"ERROR: {SRC} not found. Run from repo root.", file=sys.stderr)
        sys.exit(1)

    print(f"Loading {SRC} …")
    print("Removing background with rembg (first run downloads model ~170 MB) …")
    img_rgba = remove_bg_rembg(SRC)
    print(f"  → {img_rgba.size[0]}×{img_rgba.size[1]} RGBA")

    print("Creating circular crop …")
    circle_img = make_circle(img_rgba, SIZE)

    print(f"Saving {CIRC} …")
    circle_img.save(CIRC, "PNG", optimize=True)

    print(f"Encoding base64 → {B64} …")
    uri = to_b64_uri(circle_img)
    os.makedirs(os.path.dirname(B64), exist_ok=True)
    with open(B64, "w") as f:
        f.write(uri)

    kb = os.path.getsize(CIRC) // 1024
    print(f"\nDone.")
    print(f"  pic-circle.png : {SIZE}×{SIZE}px  ({kb} KB)")
    print(f"  pic-b64.txt    : {len(uri):,} chars")


if __name__ == "__main__":
    main()
