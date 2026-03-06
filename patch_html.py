import os
import re

html_files = ["index.html", "government.html", "drones.html"]

for filename in html_files:
    if not os.path.exists(filename):
        continue
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Fix Logo Invert Toggle
    content = re.sub(r'class="(.*?)invert transition-all"', r'class="\1transition-all invert dark:invert-0"', content)

    # 2. Update Texture Loading to use the new exact transparent scripts
    content = re.sub(r"\./assets/ugv_light_clone\.png", "./assets/ugv_light_transparent.png", content)
    content = re.sub(r"\./assets/drone_light_clone\.png", "./assets/drone_light_transparent.png", content)

    # 3. Update Blending explicitly from MultiplyBlending to NormalBlending for transparent files
    content = content.replace("THREE.MultiplyBlending", "THREE.NormalBlending")

    # 4. Fix needsUpdate bug in the event listener to fix the "requires refresh" bug
    needs_update_code = """            droneMat1.color.setHex(modelColor);
            droneMat1.needsUpdate = true;
            
            ugvMat.map = ugvMap;
            ugvMat.blending = blendMode;
            ugvMat.color.setHex(modelColor);
            ugvMat.needsUpdate = true;"""
            
    content = re.sub(r'droneMat1\.color\.setHex\(modelColor\);\s*ugvMat\.map = ugvMap;\s*ugvMat\.blending = blendMode;\s*ugvMat\.color\.setHex\(modelColor\);', needs_update_code, content)

    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)
        
    print(f"Patched {filename}")
