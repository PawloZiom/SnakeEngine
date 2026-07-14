import os
import sys
import json
import math
from PIL import Image, ImageDraw, ImageFont


def generate_font_atlas(font_path, font_size=32, padding=2):
    if not os.path.exists(font_path):
        print(f"Error: Font file '{font_path}' does not exist!")
        sys.exit(1)

    chars = [chr(i) for i in range(32, 127)] + list("ąęśćźżółńĄĘŚĆŹŻÓŁŃ")

    try:
        font = ImageFont.truetype(font_path, font_size)
    except Exception as e:
        print(f"Couldn't load font: {e}")
        sys.exit(1)

    char_metrics = {}
    max_height = 0

    for c in chars:

        bbox = font.getbbox(c)
        if bbox:
            w = bbox[2] - bbox[0]
            h = bbox[3] - bbox[1]

            offset_x = bbox[0]
            offset_y = bbox[1]
        else:
            w, h, offset_x, offset_y = font_size // 2, font_size, 0, 0

        advance = font.getlength(c)

        char_metrics[c] = {
            "width": w,
            "height": h,
            "offset_x": offset_x,
            "offset_y": offset_y,
            "advance": int(advance),
        }
        if h > max_height:
            max_height = h

    cell_size = max(font_size, max_height) + (padding * 2)
    num_chars = len(chars)
    grid_size = math.ceil(math.sqrt(num_chars))

    texture_size = 64
    while texture_size < (grid_size * cell_size):
        texture_size *= 2

    atlas_img = Image.new("RGBA", (texture_size, texture_size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(atlas_img)

    meta_data = {
        "texture_size": texture_size,
        "font_size": font_size,
        "char_height": max_height,
        "characters": {},
    }

    current_x = padding
    current_y = padding

    for c in chars:
        metrics = char_metrics[c]

        if current_x + metrics["width"] + padding > texture_size:
            current_x = padding
            current_y += max_height + (padding * 2)

        draw.text(
            (current_x - metrics["offset_x"], current_y - metrics["offset_y"]),
            c,
            font=font,
            fill=(255, 255, 255, 255),
        )

        meta_data["characters"][c] = {
            "x": current_x,
            "y": current_y,
            "width": metrics["width"],
            "height": metrics["height"],
            "advance": metrics["advance"],
        }

        current_x += metrics["width"] + (padding * 2)

    base_name = os.path.splitext(os.path.basename(font_path))[0]
    output_png = f"{base_name}_atlas.png"
    output_json = f"{base_name}_atlas.json"

    atlas_img.save(output_png)
    with open(output_json, "w", encoding="utf-8") as f:
        json.dump(meta_data, f, indent=4, ensure_ascii=False)

    print(f"Atlas generated:")
    print(f" -> Texture: {os.path.abspath(output_png)}")
    print(f" -> Metrics:  {os.path.abspath(output_json)}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python fontAtlasGen.py <path_to_font.ttf>")
        sys.exit(1)

    generate_font_atlas(sys.argv[1])
