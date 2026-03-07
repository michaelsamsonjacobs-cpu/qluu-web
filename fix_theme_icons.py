import glob
import os
import re

html_files = glob.glob('*.html')
primary_files = ['index.html', 'os.html', 'government.html', 'drones.html', 'blog.html', 'contact.html', 'article.html']
files_to_update = [f for f in html_files if f in primary_files or f.endswith('_recovered.html')]

def fix_icons(content):
    # Replace the '??' or problematic chars with moon/sun emojis
    # We'll target the specific innerText assignments and the initial span content
    content = content.replace('innerText = isDark ? \"??\" : \"??\"', 'innerText = isDark ? \"??\" : \"??\"')
    content = content.replace('innerText = document.documentElement.classList.contains(\"dark\") ? \"??\" : \"??\"', 'innerText = document.documentElement.classList.contains(\"dark\") ? \"??\" : \"??\"')
    content = content.replace('<span id=\"mobile-theme-icon\">??</span>', '<span id=\"mobile-theme-icon\">??</span>')
    # Also fix the desktop sync if it got corrupted
    content = content.replace('themeIcon.innerText = isDark ? \"??\" : \"??\"', 'themeIcon.innerText = isDark ? \"??\" : \"??\"')
    return content

count = 0
for f in files_to_update:
    with open(f, 'r', encoding='utf-8') as file:
        content = file.read()
    
    new_content = fix_icons(content)
    
    if new_content != content:
        with open(f, 'w', encoding='utf-8') as file:
            file.write(new_content)
        count += 1
        print(f'Fixed icons in {f}')

print(f'Done. Fixed icons in {count} files.')
