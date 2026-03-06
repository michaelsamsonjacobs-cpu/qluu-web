import os
htmls = ["index.html", "government.html", "drones.html"]
for h in htmls:
    with open(h, 'r', encoding='utf-8') as f: content = f.read()
    content = content.replace("THREE.NormalBlending", "THREE.MultiplyBlending")
    with open(h, 'w', encoding='utf-8') as f: f.write(content)
print("Blending fixed.")
