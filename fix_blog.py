import re
import os

with open('index.html', 'r', encoding='utf-8') as f:
    idx = f.read()

with open('blog_recovered.html', 'r', encoding='utf-8') as f:
    blg = f.read()

# 1. Grab three.js module correctly by looking for the FIRST </script> after the opening tag
module_start = idx.find('<script type="module">')
module_end = idx.find('</script>', module_start) + 9
module_script = idx[module_start:module_end]

# 2. Grab canvas style
style_block = re.search(r'<style>.*?</style>', idx, re.DOTALL).group(0)

# Inject canvas into body precisely
blg = re.sub(r'(<body.*?>)', r'\1\n    <!-- Background Animation Canvas -->\n    <canvas id="canvas"></canvas>', blg, count=1)

# Replace <style> block
blg = re.sub(r'<style>.*?</style>', style_block, blg, flags=re.DOTALL)

# Find and replace the basic theme management script
theme_management_start = blg.find('// Theme management')
if theme_management_start != -1:
    theme_management_end = blg.find('// Load blog posts from posts.json', theme_management_start)
    if theme_management_end != -1:
        # Cut it out
        blg = blg[:theme_management_start] + '// Theme handled by global module below\n        ' + blg[theme_management_end:]

# Finally, append the three module scripts to end of body
blg = blg.replace('</body>', module_script + '\n</body>')

with open('blog.html', 'w', encoding='utf-8') as f:
    f.write(blg)
