import os, re, shutil
import numpy as np
from PIL import Image

def make_crisp_transparent(input_path, output_path, target_color=(3, 9, 20)): 
    if not os.path.exists(input_path): return
    try:
        img = Image.open(input_path).convert('RGBA')
        data = np.array(img)
        r, g, b = data[:,:,0], data[:,:,1], data[:,:,2]
        intensity = (0.2989 * r + 0.5870 * g + 0.1140 * b)
        alpha = np.where(intensity > 25, 255, 0).astype(np.uint8) # Binary sharp mask
        new_data = np.zeros_like(data)
        new_data[:,:,0] = target_color[0]
        new_data[:,:,1] = target_color[1]
        new_data[:,:,2] = target_color[2]
        new_data[:,:,3] = alpha
        out_img = Image.fromarray(new_data, 'RGBA')
        out_img.save(output_path)
    except Exception as e:
        print("Error processing image:", e)

src = 'c:/Users/Mike/Desktop/new-qluu-website/inspiration/QLUU AI OS Software Icon.jpg'
if os.path.exists(src):
    shutil.copy(src, 'c:/Users/Mike/Desktop/new-qluu-website/assets/hive_dark.jpg')
    make_crisp_transparent(src, 'c:/Users/Mike/Desktop/new-qluu-website/assets/hive_light_transparent.png', target_color=(10, 20, 50))
else:
    print("No hive source found")

# Patch HTML
htmls = ["index.html", "government.html", "drones.html"]
for h in htmls:
    with open(h, 'r', encoding='utf-8') as f: content = f.read()
    
    if "hiveMat" in content: continue # Already patched
    
    # 1. Texture Definitions
    tex_inject = """const ugvTexLight = textureLoader.load('./assets/ugv_light_transparent.png' + cb);
        const droneTexLight = textureLoader.load('./assets/drone_light_transparent.png' + cb);
        const hiveTexDark = textureLoader.load('./assets/hive_dark.jpg' + cb);
        const hiveTexLight = textureLoader.load('./assets/hive_light_transparent.png' + cb);"""
    content = content.replace("const ugvTexLight = textureLoader.load('./assets/ugv_light_transparent.png' + cb);\n        const droneTexLight = textureLoader.load('./assets/drone_light_transparent.png' + cb);", tex_inject)
    
    # 2. Material Definition
    mat_inject = """const hiveMat = new THREE.MeshBasicMaterial({ map: isDarkMode ? hiveTexDark : hiveTexLight, transparent: true, opacity: 0.85, side: THREE.DoubleSide, blending: isDarkMode ? THREE.AdditiveBlending : THREE.NormalBlending, depthWrite: false, color: isDarkMode ? 0x1e3a8a : 0xffffff });
        const materials = [droneMat1, ugvMat, hiveMat];"""
    content = content.replace("const materials = [droneMat1, ugvMat];", mat_inject)
    
    # 3. Theme toggle update
    theme_inject = """ugvMat.needsUpdate = true;
            
            hiveMat.map = isDarkMode ? hiveTexDark : hiveTexLight;
            hiveMat.blending = blendMode;
            hiveMat.color.setHex(modelColor);
            hiveMat.needsUpdate = true;"""
    content = content.replace("ugvMat.needsUpdate = true;", theme_inject, 1)
    
    with open(h, 'w', encoding='utf-8') as f: f.write(content)

print("Hive injected successfully")
