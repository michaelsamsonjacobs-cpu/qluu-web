import glob
import os
import re

files = glob.glob('*.html')
count = 0

for f in files:
    with open(f, 'r', encoding='utf-8') as file:
        content = file.read()
    
    # regex to find orphan content= attributes that are not inside a <tag>
    # specifically focusing on the ones appearing at the top of the head
    # that look like: content="Not a wrapper. A Zero Cloud API sovereign AI OS built from the ground up.">
    
    pattern = r'\n\s*content="[^"]+">\s*'
    new_content = re.sub(pattern, '\n', content)
    
    if new_content != content:
        with open(f, 'w', encoding='utf-8') as file:
            file.write(new_content)
        count += 1
        print(f'Fixed orphans in {f}')

print(f'\nSuccessfully cleaned up malformed meta tags in {count} HTML files.')
