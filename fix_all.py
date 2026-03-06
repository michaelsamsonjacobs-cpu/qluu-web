import os
import re
from PIL import Image
import numpy as np

# 1. Regenerate crisp transparent assets
def make_crisp_transparent(input_path, output_path, target_color=(3, 9, 20)): 
    if not os.path.exists(input_path): 
        print(f"Skipping {input_path}")
        return
    img = Image.open(input_path).convert('RGBA')
    data = np.array(img)
    r, g, b = data[:,:,0], data[:,:,1], data[:,:,2]
    intensity = (0.2989 * r + 0.5870 * g + 0.1140 * b)
    
    # Binary mask for sharp, solid lines to overcome opacity washer
    alpha = np.where(intensity > 25, 255, 0).astype(np.uint8)
    new_data = np.zeros_like(data)
    new_data[:,:,0] = target_color[0]
    new_data[:,:,1] = target_color[1]
    new_data[:,:,2] = target_color[2]
    new_data[:,:,3] = alpha
    
    out_img = Image.fromarray(new_data, 'RGBA')
    out_img.save(output_path)
    print(f"Created exact crisp transparent asset: {output_path}")

drone_src = 'c:/Users/Mike/Desktop/new-qluu-website/inspiration/front-page.png'
ugv_src = 'c:/Users/Mike/Desktop/new-qluu-website/inspiration/UGV.jpg'
drone_out = 'c:/Users/Mike/Desktop/new-qluu-website/assets/drone_light_transparent.png'
ugv_out = 'c:/Users/Mike/Desktop/new-qluu-website/assets/ugv_light_transparent.png'

print("Generating images...")
make_crisp_transparent(drone_src, drone_out, target_color=(10, 20, 50))
make_crisp_transparent(ugv_src, ugv_out, target_color=(10, 20, 50))

# 2. Patch the HTML missing logic
print("Patching HTML...")
html_files = ["index.html", "government.html", "drones.html"]

for filename in html_files:
    if not os.path.exists(filename):
        continue
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()

    # Re-write the theme toggle block entirely to guarantee structural integrity
    # since it got mangled in the last patch attempt
    target_block = re.search(r'window\.addEventListener\(\'themeChanged\', \(\) => \{(.+?)// Layer 1 - Foreground', content, re.DOTALL)
    if target_block:
        new_block = """window.addEventListener('themeChanged', () => {
            const targetColor = isDarkMode ? 0x030914 : 0xfafcfe;
            const modelColor = isDarkMode ? 0x1e3a8a : 0xffffff;
            const blendMode = isDarkMode ? THREE.AdditiveBlending : THREE.NormalBlending;
            const uavMap = isDarkMode ? droneTexDark : droneTexLight;
            const ugvMap = isDarkMode ? ugvTexDark : ugvTexLight;

            gsap.to(scene.fog, { color: targetColor, duration: 1.0 });
            
            const colorObj = new THREE.Color(renderer.getClearColor(new THREE.Color()));
            gsap.to(colorObj, {
                r: new THREE.Color(targetColor).r,
                g: new THREE.Color(targetColor).g,
                b: new THREE.Color(targetColor).b,
                duration: 1.0,
                onUpdate: () => renderer.setClearColor(colorObj, 1)
            });

            // Update materials instantly
            droneMat1.map = uavMap;
            droneMat1.blending = blendMode;
            droneMat1.color.setHex(modelColor);
            droneMat1.needsUpdate = true;
            
            ugvMat.map = ugvMap;
            ugvMat.blending = blendMode;
            ugvMat.color.setHex(modelColor);
            ugvMat.needsUpdate = true;
        });

        // Layer 1 - Foreground"""
        content = content.replace(target_block.group(0), new_block)
        
    # Apply to disk
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)
        
    print(f"Patched {filename}")
