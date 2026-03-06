import os
import re

html_files = ["index.html", "government.html", "drones.html"]
for filename in html_files:
    if not os.path.exists(filename): continue
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()
    
    content = content.replace("gsap.to(scene.fog, { color: targetColor, duration: 1.0 });",
                              "gsap.to(scene.fog, { color: targetColor, density: isDarkMode ? 0.015 : 0.005, duration: 1.0 });")
                              
    content = content.replace("scene.fog = new THREE.FogExp2(isDarkMode ? 0x030914 : 0xfafcfe, 0.015);",
                              "scene.fog = new THREE.FogExp2(isDarkMode ? 0x030914 : 0xfafcfe, isDarkMode ? 0.015 : 0.005);")
                              
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)
print("Fog updated successfully.")
