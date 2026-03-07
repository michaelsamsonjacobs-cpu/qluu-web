import glob
import re

files = glob.glob('*.html')
count = 0

for f in files:
    with open(f, 'r', encoding='utf-8') as file:
        content = file.read()
    
    modified = False
    new_content = re.sub(r'\.q\-target:hover\s*\{\s*filter:\s*hue\-rotate\(180deg\)\s*brightness\([^)]+\);\s*\}', 
                         '.q-target:hover {\n            filter: hue-rotate(180deg) brightness(1);\n        }', content)
    
    if new_content != content:
        with open(f, 'w', encoding='utf-8') as file:
            file.write(new_content)
        count += 1
        print(f'Updated {f}')

print(f'\nSuccessfully fixed q-target in {count} HTML files.')
