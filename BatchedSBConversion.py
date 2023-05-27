import os
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import py360convert

current_dir = os.path.dirname(os.path.abspath(__file__))

# Config
side_names = ["BK", "DN", "FR", "LF", "RT", "UP"] # Side name suffixes, assumed as skybox_{side_name}.jpg
side_size = (1024, 1024) # Size of each image
show_side_names = False # Prints side names in the center of each face for debugging
input_dir = os.path.join(current_dir, "InputFolders") 
output_dir = os.path.join(current_dir, "OutputFolder")

####
cubemap_size = (side_size[0] * 4, side_size[1] * 3) # Dice format cubemap
pano_size = (side_size[0] * 4, side_size[1] * 2) # Equirectangular panorama

for i in range(30):
    folder_name = f"sb{i:02d}" #Target folder structure is 30 folders named sb00, sb01, sb02, etc
    folder_path = os.path.join(input_dir, folder_name)

    if os.path.exists(folder_path):
        # Create cubemap
        cubemap = Image.new("RGB", cubemap_size)
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
            image_path = os.path.join(folder_path, f"skybox_{side_name}.jpg")
            
            if os.path.exists(image_path):
                side_image = Image.open(image_path)
                
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

            else:
                print(f"Side image {side_name} not found in {folder_name}.")
        
        output_filename = f"cubemap_{folder_name}.png"
        output_path = os.path.join(output_dir, output_filename)
        cubemap.save(output_path)
        print(f"Saved cubemap: {output_filename}")

        # Create equirectangular panorama
        pano = py360convert.c2e(np.array(cubemap), h=pano_size[1], w=pano_size[0], mode='bilinear')
        output_filename = f"pano_{folder_name}.png"
        output_path = os.path.join(output_dir, output_filename)
        Image.fromarray(pano.astype(np.uint8)).save(output_path)
        print(f"Saved equirectangular panorama: {output_filename}")
        
    else:
        print(f"Folder {folder_name} not found.")
