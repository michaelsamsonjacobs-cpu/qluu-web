from PIL import Image
import numpy as np
import os

def make_transparent_dark_lines(input_path, output_path, target_color=(30, 58, 138)): # Deep Navy Blue
    if not os.path.exists(input_path):
        print(f"File not found: {input_path}")
        return
        
    img = Image.open(input_path).convert('RGBA')
    data = np.array(img)
    
    # Original is dark bg with light blue lines.
    # We want transparency to be based on brightness (closer to black = more transparent)
    # Get grayscale intensity (Luma)
    r, g, b, a = data[:,:,0], data[:,:,1], data[:,:,2], data[:,:,3]
    intensity = (0.2989 * r + 0.5870 * g + 0.1140 * b)
    
    # Normalize intensity to 0-255 for alpha channel
    # Increase contrast so faint lines don't disappear entirely.
    # Subtacting 20 removes dark background noise. multiplying by 1.5 boosts the lines.
    alpha = np.clip((intensity - 20) * 1.5, 0, 255).astype(np.uint8)
    
    # Create new image data with target color and calculated alpha
    new_data = np.zeros_like(data)
    new_data[:,:,0] = target_color[0]
    new_data[:,:,1] = target_color[1]
    new_data[:,:,2] = target_color[2]
    new_data[:,:,3] = alpha
    
    out_img = Image.fromarray(new_data, 'RGBA')
    out_img.save(output_path)
    print(f"Created transparent asset: {output_path}")

# Source files from inspiration folder
drone_src = 'c:/Users/Mike/Desktop/new-qluu-website/inspiration/front-page.png'
ugv_src = 'c:/Users/Mike/Desktop/new-qluu-website/inspiration/UGV.jpg'

# Output files directly to assets
drone_out = 'c:/Users/Mike/Desktop/new-qluu-website/assets/drone_light_transparent.png'
ugv_out = 'c:/Users/Mike/Desktop/new-qluu-website/assets/ugv_light_transparent.png'

make_transparent_dark_lines(drone_src, drone_out, target_color=(10, 25, 60)) # Even darker navy to contrast with white
make_transparent_dark_lines(ugv_src, ugv_out, target_color=(10, 25, 60))
