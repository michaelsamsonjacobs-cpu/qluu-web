import glob
import os
import re

html_files = glob.glob('*.html')
primary_files = ['index.html', 'os.html', 'government.html', 'drones.html', 'blog.html', 'contact.html', 'article.html']
files_to_update = [f for f in html_files if f in primary_files or f.endswith('_recovered.html')]

# Use Unicode escapes for sun and moon
SUN = '\u2600\uFE0F'
MOON = '\uD83C\uDF19'

def fix_icons_logic(content):
    # Standardize the ? expressions we injected
    # Pattern: '??' : '??'
    content = re.sub(r"'\?\?'\s*:\s*'\?\?'", f"'{SUN}' : '{MOON}'", content)
    content = re.sub(r'\"\?\?\"\s*:\s*\"\?\?\"', f'\"{SUN}\" : \"{MOON}\"', content)
    
    # Pattern: id="mobile-theme-icon">??</span>
    content = content.replace('>??</span>', f'>{MOON}</span>')
    
    return content

count = 0
for f in files_to_update:
    try:
        with open(f, 'r', encoding='utf-8') as file:
            content = file.read()
        
        new_content = fix_icons_logic(content)
        
        if new_content != content:
            with open(f, 'w', encoding='utf-8', newline='') as file:
                file.write(new_content)
            count += 1
            print(f'Fixed {f}')
    except Exception as e:
        print(f'Error processing {f}: {e}')

print(f'Done: {count}')
