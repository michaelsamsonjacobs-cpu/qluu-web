import glob
import re
import os

files = ['index.html', 'os.html', 'government.html', 'drones.html', 'blog.html', 'contact.html', 'article.html']
existing_files = [f for f in files if os.path.exists(f)]

meta_tags = """
    <meta property="og:site_name" content="QLUU">
    <meta property="og:type" content="website">
    <meta property="og:url" content="https://qluu.website/">
    <meta property="og:title" content="QLUU | Autonomous Counter-UAS Defense">
    <meta property="og:description" content="QLUUos: Sovereign AI platform for autonomous counter-UAS defense. Hardware-agnostic, self-improving defense for critical infrastructure.">
    <meta property="og:image" content="https://qluu.website/assets/og_image_new.png">
    <meta property="og:image:width" content="1200">
    <meta property="og:image:height" content="630">

    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:domain" content="qluu.website">
    <meta name="twitter:url" content="https://qluu.website/">
    <meta name="twitter:title" content="QLUU | Autonomous Counter-UAS Defense">
    <meta name="twitter:description" content="Sovereign AI platform for autonomous counter-UAS defense. Deploy in hours, not months.">
    <meta name="twitter:image" content="https://qluu.website/assets/og_image_new.png">
"""

def clean_tags(content):
    # Remove existing og and twitter tags
    lines = content.split('\n')
    new_lines = []
    for line in lines:
        if 'property="og:' not in line and 'name="twitter:' not in line:
            new_lines.append(line)
    return '\n'.join(new_lines)

for f in existing_files:
    with open(f, 'r', encoding='utf-8') as file:
        content = file.read()
    
    content = clean_tags(content)
    
    # Inject after title
    if '</title>' in content:
        content = content.replace('</title>', '</title>' + meta_tags)
        with open(f, 'w', encoding='utf-8') as file:
            file.write(content)
        print(f'Updated {f}')

print('\nDone.')
