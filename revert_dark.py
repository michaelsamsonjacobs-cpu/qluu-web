import os
import re

html_files = ["index.html", "government.html", "drones.html"]

for filename in html_files:
    if not os.path.exists(filename):
        continue
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 1. Strip all `dark:` prefixes (so it defaults strictly to the dark classes that were added)
    # Wait, the light mode colors were the default classes and the dark colors were prefixed by `dark:`!
    # e.g., `text-gray-900 dark:text-white`
    # If I just remove `dark:`, it becomes `text-gray-900 text-white`.
    # I actually need to remove the LIGHT mode class, and keep the DARK mode class without the prefix.
    # regex: find `<something> dark:<something_else>` and replace with `<something_else>`.
    # e.g., `text-gray-900 dark:text-white` -> `text-white`
    content = re.sub(r'([a-zA-Z0-9_-]+)\s+dark:([a-zA-Z0-9_-]+)', r'\2', content)
    
    # Run a few passes to catch multiple instances in a row
    for _ in range(3):
        content = re.sub(r'([a-zA-Z0-9_-]+)\s+dark:([a-zA-Z0-9_-]+)', r'\2', content)
        
    # Catch any remaining standalone `dark:` classes
    content = re.sub(r'dark:([a-zA-Z0-9_-]+)', r'\1', content)
            
    # Remove the toggle button
    toggle_html_regex = r'<button id="theme-toggle".*?</button>'
    content = re.sub(toggle_html_regex, '', content, flags=re.DOTALL)
    
    # Make sure html.dark is removed or neutralized, though without a toggle it doesn't matter too much,
    # but let's remove the JS toggle logic entirely.
    js_toggle_start = r'// Theme management(.*?)// Scene setup'
    content = re.sub(js_toggle_start, '// Scene setup', content, flags=re.DOTALL)
    
    js_texture_replacement = r'''        const textureLoader = new THREE.TextureLoader();.*?(const materials = \[.*?\];).*?const shapes = \[\];'''
    
    replacement_textures = '''        const textureLoader = new THREE.TextureLoader();
        const ugvTexDark = textureLoader.load('./assets/ugv_3d.png');
        const droneTexDark = textureLoader.load('./assets/drone_1.png');

        const droneMat1 = new THREE.MeshBasicMaterial({ map: droneTexDark, transparent: true, opacity: 0.85, side: THREE.DoubleSide, blending: THREE.AdditiveBlending, depthWrite: false, color: 0x1e3a8a });
        const ugvMat = new THREE.MeshBasicMaterial({ map: ugvTexDark, transparent: true, opacity: 0.85, side: THREE.DoubleSide, blending: THREE.AdditiveBlending, depthWrite: false, color: 0x1e3a8a });

        const materials = [droneMat1, ugvMat];
        const shapes = [];'''
    content = re.sub(js_texture_replacement, replacement_textures, content, flags=re.DOTALL)
    
    js_toggle_event = r'// Theme Toggle Logic for ThreeJS(.*?)// Layer 1'
    content = re.sub(js_toggle_event, '// Layer 1', content, flags=re.DOTALL)

    # Force fog and clear color to dark mode `#030914`
    content = re.sub(r'scene.fog = new THREE.FogExp2\(.*?\);', 'scene.fog = new THREE.FogExp2(0x030914, 0.015);', content)
    content = re.sub(r'renderer.setClearColor\(.*?\);', 'renderer.setClearColor(0x030914, 1);', content)
    
    # Body tag fix
    content = re.sub(r'<body class="bg-brand-lightBg bg-brand-navy">', '<body class="bg-brand-navy">', content)

    # CSS fixes: remove html.dark from the style block
    content = re.sub(r'html\.dark body \{.*?\}', '', content, flags=re.DOTALL)
    content = re.sub(r'html\.dark \.glass-nav \{.*?\}', '', content, flags=re.DOTALL)
    content = re.sub(r'html\.dark \.text-glow \{.*?\}', '', content, flags=re.DOTALL)
    content = re.sub(r'html\.dark \.q-target.*?\n.*?\n.*?\n.*?\n.*?\}', '', content, flags=re.DOTALL)
    
    # Q-target hover in original dark mode was just a brightness increase
    content = re.sub(r'/\* In light mode hover.*?\*/\s*\.q-target:hover.*?\n.*?\}', '.q-target:hover {\n            filter: hue-rotate(180deg) brightness(1.2);\n        }', content, flags=re.DOTALL)

    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)
        
    print(f"Reverted {filename}")
