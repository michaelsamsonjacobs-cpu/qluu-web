from PIL import Image
import numpy as np

def process_image(input_path, output_path):
    print(f"Processing {input_path}...")
    img = Image.open(input_path).convert('RGB')
    data = np.array(img).astype(np.float32)
    
    # 1. Invert
    inverted = 255.0 - data
    
    # 2. Convert to HSV for hue rotation
    from matplotlib.colors import rgb_to_hsv, hsv_to_rgb
    # rgb_to_hsv expects 0-1
    hsv = rgb_to_hsv(inverted / 255.0)
    
    # Shift hue by 180 degrees (0.5 in 0-1 range)
    hsv[..., 0] = (hsv[..., 0] + 0.5) % 1.0
    
    # Convert back to RGB
    rgb = hsv_to_rgb(hsv) * 255.0
    
    out_img = Image.fromarray(np.clip(rgb, 0, 255).astype(np.uint8))
    out_img.save(output_path)
    print(f"Saved {output_path}")

process_image('assets/drone_1.png', 'assets/drone_1_light_exact.png')
process_image('assets/ugv_3d.png', 'assets/ugv_3d_light_exact.png')
