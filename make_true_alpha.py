import numpy as np
from PIL import Image

def process_file(in_path, out_path):
    print(f"Processing {in_path} to {out_path}...")
    img = Image.open(in_path).convert('RGB')
    data = np.array(img).astype(np.float32)
    
    # Luminance based on maximum color channel (preserves the brightest glowing parts fully)
    alpha = np.max(data, axis=2)
    
    # Avoid division by zero
    alpha_safe = np.where(alpha == 0, 1, alpha)
    
    # Normalize RGB to remove pre-multiplication
    # Because original image has black background, its RGB values fade to black.
    # We want the RGB to be the "un-dimmed" color, and let the Alpha channel handle the dimming/fading!
    rgba = np.zeros((data.shape[0], data.shape[1], 4), dtype=np.uint8)
    rgba[..., 0] = np.clip((data[..., 0] / alpha_safe) * 255, 0, 255).astype(np.uint8)
    rgba[..., 1] = np.clip((data[..., 1] / alpha_safe) * 255, 0, 255).astype(np.uint8)
    rgba[..., 2] = np.clip((data[..., 2] / alpha_safe) * 255, 0, 255).astype(np.uint8)
    # The alpha channel is just the brightness of the block
    rgba[..., 3] = alpha.astype(np.uint8)
    
    out = Image.fromarray(rgba, 'RGBA')
    out.save(out_path)
    print("Done")

process_file('assets/drone_1.png', 'assets/drone_1_exact_alpha.png')
process_file('assets/ugv_3d.png', 'assets/ugv_3d_exact_alpha.png')
