import os
import numpy as np
from PIL import Image

def make_multiply_asset(input_path, output_path, thickness=50.0):
    if not os.path.exists(input_path): return
    img = Image.open(input_path).convert('RGB')
    data = np.array(img).astype(np.float32)
    
    r, g, b = data[:,:,0], data[:,:,1], data[:,:,2]
    intensity = (0.2989 * r + 0.5870 * g + 0.1140 * b)
    
    # Thicken lines by mapping 15-65 intensity directly to full navy blue.
    factor = np.clip((intensity - 15) / thickness, 0, 1.0)
    
    navy = np.array([5.0, 20.0, 60.0]) # High-contrast deep blue
    white = np.array([255.0, 255.0, 255.0])
    
    out_r = white[0] * (1 - factor) + navy[0] * factor
    out_g = white[1] * (1 - factor) + navy[1] * factor
    out_b = white[2] * (1 - factor) + navy[2] * factor
    
    new_data = np.zeros_like(data)
    new_data[:,:,0] = out_r
    new_data[:,:,1] = out_g
    new_data[:,:,2] = out_b
    
    out_img = Image.fromarray(new_data.astype(np.uint8), 'RGB')
    out_img.save(output_path)
    print(f"Multiply Asset Generated: {output_path}")

base = 'c:/Users/Mike/Desktop/new-qluu-website'
make_multiply_asset(f'{base}/inspiration/front-page.png', f'{base}/assets/drone_light_transparent.png')
make_multiply_asset(f'{base}/inspiration/UGV.jpg', f'{base}/assets/ugv_light_transparent.png')
make_multiply_asset(f'{base}/inspiration/QLUU AI OS Software Icon.jpg', f'{base}/assets/hive_light_transparent.png')
