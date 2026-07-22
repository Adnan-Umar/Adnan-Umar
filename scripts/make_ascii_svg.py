import sys
import os
import math

try:
    from PIL import Image
except ImportError:
    print("Pillow is required: pip install Pillow")
    sys.exit(1)

RAMP = " .'`^\",:;Il!i~+_-?][}{1)(|\\/tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@$"

def image_to_ascii(image_path: str, width: int = 80, height: int = 40) -> str:
    img = Image.open(image_path).convert("L")
    img = img.resize((width, height), Image.Resampling.LANCZOS)
    pixels = list(img.getdata())
    chars = []
    for y in range(height):
        row = ""
        for x in range(width):
            brightness = pixels[y * width + x]
            index = int((brightness / 255) * (len(RAMP) - 1))
            row += RAMP[index]
        chars.append(row)
    return "\n".join(chars)


def make_ascii_svg(input_path: str, output_path: str = "ascii-art.svg") -> None:
    if not os.path.exists(input_path):
        print(f"Input not found: {input_path}")
        sys.exit(1)

    ascii_text = image_to_ascii(input_path, width=60, height=30)
    lines = ascii_text.split("\n")
    line_count = len(lines)
    max_len = max(len(line) for line in lines) if lines else 0

    font_size = 8
    line_height = 9
    width = max_len * font_size + 80
    height = line_count * line_height + 120

    svg_parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}">',
        "<defs>",
        '<linearGradient id="asciiGrad" x1="0%" y1="0%" x2="100%" y2="0%">',
        "<stop offset='0%' stop-color='#22D3EE'>",
        '<animate attributeName="stop-color" values="#22D3EE;#7C3AED;#22D3EE" dur="3s" repeatCount="indefinite"/>',
        "</stop>",
        "<stop offset='100%' stop-color='#7C3AED'>",
        '<animate attributeName="stop-color" values="#7C3AED;#22D3EE;#7C3AED" dur="3s" repeatCount="indefinite"/>',
        "</stop>",
        "</linearGradient>",
        '<filter id="glow">',
        "<feGaussianBlur stdDeviation='2' result='blur'/>",
        "<feMerge><feMergeNode in='blur'/><feMergeNode in='SourceGraphic'/></feMerge>",
        "</filter>",
        '<clipPath id="asciiClip">',
        f'<rect x="0" y="0" width="{width}" height="0">',
        f'<animate attributeName="height" values="0;{height}" dur="3s" fill="freeze" calcMode="spline" keySplines="0.4 0 0.2 1"/>',
        f'<animate attributeName="y" values="{height};0" dur="3s" fill="freeze" calcMode="spline" keySplines="0.4 0 0.2 1"/>',
        "</rect>",
        "</clipPath>",
        "</defs>",
    ]

    svg_parts.append(f'<rect width="{width}" height="{height}" fill="#0F172A"/>')

    svg_parts.append('<g clip-path="url(#asciiClip)">')
    svg_parts.append('<animateTransform attributeName="transform" type="translate" values="0,0; 0,-3; 0,0" dur="6s" repeatCount="indefinite"/>')

    for i, line in enumerate(lines):
        y = 20 + i * line_height
        safe_line = line.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        svg_parts.append(f'<text x="40" y="{y}" font-family="monospace" font-size="{font_size}" fill="url(#asciiGrad)" filter="url(#glow)">{safe_line}</text>')

    svg_parts.append("</g>")

    cursor_x = 40 + max_len * font_size + 4
    cursor_y = 20 + line_count * line_height - line_height + 6
    svg_parts.append(f'<rect x="{cursor_x}" y="{cursor_y}" width="6" height="{font_size}" fill="#22D3EE">')
    svg_parts.append('<animate attributeName="opacity" values="0;1;0" dur="1s" repeatCount="indefinite"/>')
    svg_parts.append("</rect>")

    svg_parts.append("</svg>")

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(svg_parts))
    print(f"ASCII SVG written to {output_path}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python make_ascii_svg.py <prepped-image.png> [output.svg]")
        sys.exit(1)
    make_ascii_svg(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else "ascii-art.svg")
