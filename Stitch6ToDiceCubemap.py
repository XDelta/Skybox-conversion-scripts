from PIL import Image, ImageDraw, ImageFont

# Config
side_names = ["BK", "DN", "FR", "LF", "RT", "UP"] # Side name suffixes, assumed as skybox_{side_name}.jpg
side_size = (1024, 1024) # Size of each image
show_side_names = True # Prints side names in the center of each face for debugging
###

cubemap_size = (side_size[0] * 4, side_size[1] * 3)
cubemap = Image.new("RGB", cubemap_size)

# Remapping suffixes to sides can be done here if needed
positions = {
    "BK": (side_size[0], side_size[1]),
    "DN": (side_size[0], side_size[1] * 2),
    "RT": (side_size[0] * 2, side_size[1]),
    "LF": (0, side_size[1]),
    "FR": (side_size[0] * 3, side_size[1]),
    "UP": (side_size[0], 0)
}

draw = ImageDraw.Draw(cubemap)
font = ImageFont.truetype("arial.ttf", 80)

for side_name in side_names:
    side_image = Image.open(f"skybox_{side_name}.jpg")
    x, y = positions[side_name]
    cubemap.paste(side_image, (x, y))

    if show_side_names:
        side_label = f"[{side_name}]"
        label_bbox = draw.textbbox((0, 0), side_label, font=font)
        label_size = (label_bbox[2] - label_bbox[0], label_bbox[3] - label_bbox[1])
        label_position = (x + side_size[0] // 2 - label_size[0] // 2, y + side_size[1] // 2 - label_size[1] // 2)

        overlay = Image.new("RGBA", (label_size[0] + 16, label_size[1] + 16), (0, 0, 0, 192))
        overlay_position = (label_position[0] - 8, label_position[1]+4)
        cubemap.paste(overlay, overlay_position, mask=overlay)

        draw.text(label_position, side_label, fill=(255, 255, 255), font=font)

cubemap.save("cubemap.jpg")
