import re

with open('index.html', 'r', encoding='utf-8') as f:
    index_html = f.read()

with open('blog_recovered.html', 'r', encoding='utf-8') as f:
    blog_html = f.read()

# 1. Grab importmap
importmap_match = re.search(r'<script type="importmap">.*?</script>', index_html, re.DOTALL)
importmap = importmap_match.group(0)

# 2. Grab three.js module script
module_match = re.search(r'<script type="module">.*?</script>', index_html, re.DOTALL)
module_script = module_match.group(0)

# 3. Grab canvas style
style_match = re.search(r'<style>.*?</style>', index_html, re.DOTALL)
style_block = style_match.group(0)

# Inject <canvas>
blog_html = re.sub(r'(<body.*?>)', r'\1\n    <!-- Background Animation Canvas -->\n    <canvas id="canvas"></canvas>', blog_html, count=1)

# Replace <style> block
blog_html = re.sub(r'<style>.*?</style>', style_block, blog_html, flags=re.DOTALL)

# Delete existing basic theme management script from blog.html
# It looks like:
#         // Theme management
#         const themeToggle = document.getElementById('theme-toggle');
# ... up to applyTheme(isDarkMode); });
theme_script_pattern = r'// Theme management[\s\S]*?applyTheme\(isDarkMode\);\s*}\s*applyTheme\(isDarkMode\);\s*themeToggle\.addEventListener\(\'click\', \(\) => {[\s\S]*?\}\);'
blog_html = re.sub(theme_script_pattern, '// Theme Management is now handled by the 3D canvas script below!', blog_html)

# Append threejs scripts just before </body>
scripts_to_inject = f"{importmap}\n{module_script}\n"
blog_html = blog_html.replace('</body>', scripts_to_inject + '\n</body>')

with open('blog.html', 'w', encoding='utf-8') as f:
    f.write(blog_html)

print("Blog successfully patched.")
