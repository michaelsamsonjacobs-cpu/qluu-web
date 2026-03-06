import os

htmls = ["index.html", "government.html", "drones.html"]
for h in htmls:
    with open(h, 'r', encoding='utf-8') as f: content = f.read()

    # 1. Eliminate cache-buster entirely to allow instantaneous caching loads
    content = content.replace("const cb = '?v=' + Date.now();", "const cb = '';")
    
    # 2. Fix GSAP scene.fog.color crash
    # GSAP crashes if you inject an integer directly into a THREE.Color object.
    # It attempts to write a raw int where an object API is expected.
    old_gsap = "gsap.to(scene.fog, { color: targetColor, density: isDarkMode ? 0.015 : 0.005, duration: 1.0 });"
    new_gsap = """const targetColorHex = new THREE.Color(targetColor);
            gsap.to(scene.fog.color, { r: targetColorHex.r, g: targetColorHex.g, b: targetColorHex.b, duration: 1.0 });
            gsap.to(scene.fog, { density: isDarkMode ? 0.015 : 0.005, duration: 1.0 });"""
    content = content.replace(old_gsap, new_gsap)
    
    with open(h, 'w', encoding='utf-8') as f: f.write(content)

print("Fixed load caching variables and resolved GSAP crash.")
