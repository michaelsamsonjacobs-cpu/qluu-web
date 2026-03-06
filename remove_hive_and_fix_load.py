import os
import re

htmls = ["index.html", "government.html", "drones.html"]

for h in htmls:
    with open(h, 'r', encoding='utf-8') as f: content = f.read()

    # 1. REMOVE HIVE ASSET
    # Remove from textures
    tex_remove = """const hiveTexDark = textureLoader.load('./assets/hive_dark.jpg' + cb);
        const hiveTexLight = textureLoader.load('./assets/hive_light_transparent.png' + cb);"""
    content = content.replace(tex_remove, "")
    
    # Remove from materials array creation
    mat_remove = """const hiveMat = new THREE.MeshBasicMaterial({ map: isDarkMode ? hiveTexDark : hiveTexLight, transparent: true, opacity: 0.85, side: THREE.DoubleSide, blending: isDarkMode ? THREE.AdditiveBlending : THREE.MultiplyBlending, depthWrite: false, color: isDarkMode ? 0x1e3a8a : 0xffffff });
        const materials = [droneMat1, ugvMat, hiveMat];"""
    content = content.replace(mat_remove, "const materials = [droneMat1, ugvMat];")
    
    # Remove from event listener logic
    event_remove = """hiveMat.map = isDarkMode ? hiveTexDark : hiveTexLight;
            hiveMat.blending = blendMode;
            hiveMat.color.setHex(modelColor);
            hiveMat.needsUpdate = true;"""
    content = content.replace(event_remove, "")
    
    # 2. FIX INITIAL LOAD BUG
    # The materials are created with defaults like "color: isDarkMode ? 0x1e3a8a : 0xffffff". 
    # But `isDarkMode` comes from `localStorage.getItem('theme') === 'dark'`. 
    # Wait, if localStorage is empty, `isDarkMode` is false.
    # What if the user wants Dark Mode initial load? The CSS class uses `dark:`. 
    # Actually, the quickest fix is simply calling `window.dispatchEvent(new Event('themeChanged'));` 
    # IMMEDIATELY after ThreeJS setup, before the first `animate()` loop!
    
    if "window.dispatchEvent(new Event('themeChanged'));" not in content.split("// Initialize animation")[1]:
         content = content.replace("// Initialize animation\n        animate();", "// Guarantee material sync on load\n        window.dispatchEvent(new Event('themeChanged'));\n        // Initialize animation\n        animate();")

    with open(h, 'w', encoding='utf-8') as f: f.write(content)

print("Hive removed and initial trigger added.")
