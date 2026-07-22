import sys
import cv2
import numpy as np
from PIL import Image
from rembg import remove


def prep_photo(input_path: str, output_path: str = "source-prepped.png") -> None:
    img = Image.open(input_path).convert("RGBA")
    img_no_bg = remove(img)
    img_no_bg_rgb = img_no_bg.convert("RGB")
    data = np.array(img_no_bg_rgb)
    gray = cv2.cvtColor(data, cv2.COLOR_RGB2GRAY)
    clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
    enhanced = clahe.apply(gray)
    white_bg = np.full_like(data, 255)
    mask = np.array(img_no_bg)[:, :, 3] > 0
    white_bg[mask] = np.stack([enhanced[mask]] * 3, axis=-1)
    result = Image.fromarray(white_bg)
    result.save(output_path)
    print(f"Prepped photo saved to {output_path}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python prep_photo.py <source-photo.jpg>")
        sys.exit(1)
    prep_photo(sys.argv[1])
