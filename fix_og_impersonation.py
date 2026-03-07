import glob
import os
import re

# Simple, non-confrontational metadata
# Using relative image path for OG:image can sometimes trigger 'impersonation'
# if the metadata is overly specific about a domain that doesn't match the current hosting.
# We'll use a standard, minimal set.
meta_tags = """
    <meta property="og:title" content="QLUU">
    <meta property="og:description" content="Sovereign AI Defense Platform">
    <meta property="og:image" content="assets/og_preview_simple.png">
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:image" content="assets/og_preview_simple.png">
"""

files = ['index.html', 'os.html', 'government.html', 'drones.html', 'blog.html', 'contact.html', 'article.html']
existing_files = [f for f in files if os.path.exists(f)]

def clean_redundant_meta(content):
    # Remove all OG and Twitter tags to start fresh
    lines = content.split('\n')
    filtered_lines = []
    for line in lines:
        if 'property="og:' not in line and 'name="twitter:' not in line:
            filtered_lines.append(line)
    return '\n'.join(filtered_lines)

for f in existing_files:
    with open(f, 'r', encoding='utf-8') as file:
        content = file.read()
    
    content = clean_redundant_meta(content)
    
    # Inject simple tags after title
    if '</title>' in content:
        content = content.replace('</title>', '</title>' + meta_tags)
        with open(f, 'w', encoding='utf-8') as file:
            file.write(content)
        print(f'Simplified {f}')

print('\nDone.')
