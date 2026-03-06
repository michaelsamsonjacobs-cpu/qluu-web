import os
import re

html_files = ["index.html", "government.html", "drones.html"]

for filename in html_files:
    if not os.path.exists(filename):
        continue
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Update the body class
    content = re.sub(r'<body class="bg-brand-navy">', '<body class="bg-brand-lightBg text-gray-900 transition-colors dark:bg-brand-navy dark:text-white">', content)

    # 2. Update the glass-nav class
    # Add dark mode variant logic specifically for text and nav elements
    content = re.sub(r'class="(.*?)opacity-80 uppercase transition-colors"', r'class="\1uppercase transition-colors text-gray-700 dark:text-brand-sepia dark:opacity-80"', content)
    
    # 3. Add the toggle button back to the nav
    toggle_btn = '''            <button id="theme-toggle" class="p-2 rounded-full hover:bg-gray-200 dark:hover:bg-gray-800 transition-colors cursor-pointer text-xl">
                <span id="theme-icon">🌙</span>
            </button>
            <a href="#"'''
    content = re.sub(r'            <a href="#"', toggle_btn, content)

    # 4. Inject the comprehensive ThreeJS Toggle Logic
    js_target = r'import \* as THREE from "https://esm\.sh/three@0\.160\.0";\s*gsap\.registerPlugin\(ScrollTrigger\);\s*// Scene setup'
    
    js_replacement = '''import * as THREE from "https://esm.sh/three@0.160.0";
        gsap.registerPlugin(ScrollTrigger);

        // Theme management
        const themeToggle = document.getElementById('theme-toggle');
        const themeIcon = document.getElementById('theme-icon');
        const isSystemDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
        // Default to light mode (false = light, true = dark)
        let isDarkMode = localStorage.getItem('theme') === 'dark';

        function applyTheme(dark) {
            if (dark) {
                document.documentElement.classList.add('dark');
                themeIcon.textContent = '☀️';
            } else {
                document.documentElement.classList.remove('dark');
                themeIcon.textContent = '🌙';
            }
        }

        // Initialize theme
        applyTheme(isDarkMode);

        themeToggle.addEventListener('click', () => {
            isDarkMode = !isDarkMode;
            localStorage.setItem('theme', isDarkMode ? 'dark' : 'light');
            applyTheme(isDarkMode);
            // ThreeJS updates are handled in the event listener below
            window.dispatchEvent(new Event('themeChanged'));
        });

        // Scene setup'''
    content = re.sub(js_target, js_replacement, content)

    # 5. Scene clear color and fog initial state based on theme
    content = re.sub(r'scene\.fog = new THREE\.FogExp2\(0x030914, 0\.015\);', 'scene.fog = new THREE.FogExp2(isDarkMode ? 0x030914 : 0xfafcfe, 0.015);', content)
    content = re.sub(r'renderer\.setClearColor\(0x030914, 1\);', 'renderer.setClearColor(isDarkMode ? 0x030914 : 0xfafcfe, 1);', content)

    # 6. Re-write texture loading and materials
    texture_target = r'        const textureLoader = new THREE\.TextureLoader\(\);\s*.*?const materials = \[droneMat1, ugvMat\];'
    texture_replacement = '''        const textureLoader = new THREE.TextureLoader();
        const cb = '?v=' + Date.now();

        // Dark Textures
        const ugvTexDark = textureLoader.load('./assets/ugv_3d.png' + cb);
        const droneTexDark = textureLoader.load('./assets/drone_1.png' + cb);

        // Light Textures (Clones)
        const ugvTexLight = textureLoader.load('./assets/ugv_light_clone.png' + cb);
        const droneTexLight = textureLoader.load('./assets/drone_light_clone.png' + cb);

        // Initial material setup based on the current theme
        const droneMat1 = new THREE.MeshBasicMaterial({ 
            map: isDarkMode ? droneTexDark : droneTexLight, 
            transparent: true, opacity: 0.85, side: THREE.DoubleSide, 
            blending: isDarkMode ? THREE.AdditiveBlending : THREE.MultiplyBlending, 
            depthWrite: false, 
            color: isDarkMode ? 0x1e3a8a : 0xffffff 
        });
        const ugvMat = new THREE.MeshBasicMaterial({ 
            map: isDarkMode ? ugvTexDark : ugvTexLight, 
            transparent: true, opacity: 0.85, side: THREE.DoubleSide, 
            blending: isDarkMode ? THREE.AdditiveBlending : THREE.MultiplyBlending, 
            depthWrite: false, 
            color: isDarkMode ? 0x1e3a8a : 0xffffff 
        });

        const materials = [droneMat1, ugvMat];'''
    content = re.sub(texture_target, texture_replacement, content, flags=re.DOTALL)

    # 7. Add Theme Toggle Event Listener for ThreeJS
    listener_target = r'// Layer 1 - Foreground'
    listener_replacement = '''// Theme Toggle Logic for ThreeJS
        window.addEventListener('themeChanged', () => {
            const targetColor = isDarkMode ? 0x030914 : 0xfafcfe;
            const modelColor = isDarkMode ? 0x1e3a8a : 0xffffff;
            const blendMode = isDarkMode ? THREE.AdditiveBlending : THREE.MultiplyBlending;
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
            
            ugvMat.map = ugvMap;
            ugvMat.blending = blendMode;
            ugvMat.color.setHex(modelColor);
        });

        // Layer 1 - Foreground'''
    content = re.sub(listener_target, listener_replacement, content)
    
    # 8. Re-inject specific Light Mode CSS styles (like the dark hover black inversion)
    css_target = r'        \.q-target:hover \{\n            filter: hue-rotate\(180deg\) brightness\(1\.2\);\n        \}'
    css_replacement = '''        /* In light mode hover, invert makes it black, brightness 0 makes it true black */
        .q-target:hover {
            filter: hue-rotate(180deg) brightness(0);
        }

        html.dark .q-target {
            filter: hue-rotate(180deg) brightness(0.8);
        }

        html.dark .q-target:hover {
            filter: hue-rotate(180deg) brightness(1.2);
        }
        
        html.dark .text-glow {
            text-shadow: 0 0 20px rgba(0, 174, 239, 0.5);
        }
        
        .glass-nav {
            background: rgba(250, 252, 254, 0.7);
            backdrop-filter: blur(12px);
            -webkit-backdrop-filter: blur(12px);
            border-bottom: 1px solid rgba(0, 174, 239, 0.2);
            transition: background-color 0.5s;
        }

        html.dark .glass-nav {
            background: rgba(3, 9, 20, 0.6);
            border-bottom: 1px solid rgba(0, 174, 239, 0.1);
        }
'''
    content = re.sub(css_target, css_replacement, content)
    
    # Text changes
    content = re.sub(r'class="text-glow(.*?)"', r'class="\1"', content)
    content = re.sub(r'text-white', r'text-gray-900 dark:text-white', content)
    content = re.sub(r'text-brand-sepia', r'text-brand-navy dark:text-brand-sepia', content)

    # Write out
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)
        
    print(f"Updated {filename} with exact V2 Light Mode logic")
