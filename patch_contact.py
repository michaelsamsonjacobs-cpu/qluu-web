import re

with open('contact.html', 'r', encoding='utf-8') as f:
    contact_content = f.read()

with open('index.html', 'r', encoding='utf-8') as f:
    index_content = f.read()

# 1. Update Head Canvas CSS
canvas_css = """
        #canvas {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            z-index: 1;
            pointer-events: none;
        }

        /* Glassmorphism nav */
"""
if '#canvas' not in contact_content:
    contact_content = contact_content.replace('/* Glassmorphism nav */', canvas_css)

# 2. Add Canvas element
canvas_elem = """
<body class="bg-brand-lightBg text-gray-900 transition-colors dark:bg-brand-navy dark:text-white">
    <canvas id="canvas"></canvas>
"""
if '<canvas id="canvas"></canvas>' not in contact_content:
    contact_content = contact_content.replace('<body class="bg-brand-lightBg text-gray-900 transition-colors dark:bg-brand-navy dark:text-white">', canvas_elem)

# 3. Add Background Gradient and Script
scripts_to_add = """
    <!-- Background Blueprint Grid overlay for technical vibe -->
    <div class="fixed inset-0 pointer-events-none z-0 mix-blend-overlay opacity-10"
        style="background-image: linear-gradient(rgba(0, 174, 239, 0.4) 1px, transparent 1px), linear-gradient(90deg, rgba(0, 174, 239, 0.4) 1px, transparent 1px); background-size: 50px 50px;">
    </div>

    <!-- Background Blueprint Script -->
"""

index_scripts = index_content.split('<script type="module">')[1].split('</script>')[0]
scripts_to_add += '<script type="module">' + index_scripts + '</script>'

if 'import * as THREE' not in contact_content:
    contact_content = contact_content.replace('</body>', scripts_to_add + '\n</body>')

with open('contact.html', 'w', encoding='utf-8') as f:
    f.write(contact_content)
print("Updated contact.html")
