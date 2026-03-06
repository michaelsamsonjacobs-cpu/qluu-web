import os
import re

html_files = [f for f in os.listdir('.') if f.endswith('.html') and not f.startswith('recover') and not f.startswith('cache') and not f.startswith('chrome')]

def process_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Opacities
    content = content.replace("opacity: 0.85", "opacity: 0.68")
    content = content.replace("dimmedMat.opacity = 0.3;", "dimmedMat.opacity = 0.24;")

    # Counts
    content = content.replace("for (let i = 0; i < 15; i++) {", "for (let i = 0; i < 10; i++) {")
    content = content.replace("for (let i = 0; i < 25; i++) {", "for (let i = 0; i < 16; i++) {")
    content = content.replace("for (let i = 0; i < 35; i++) {", "for (let i = 0; i < 23; i++) {")

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"Processed {file_path}")

for f in html_files:
    process_file(f)
