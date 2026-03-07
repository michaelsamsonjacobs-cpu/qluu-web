import glob
import re

files = glob.glob('*.html')
count = 0

for f in files:
    with open(f, 'r', encoding='utf-8') as file:
        content = file.read()
    
    # Remove the entire style block for .q-target if it exists
    # This regex is a bit cautious to only catch the blocks we saw
    new_content = re.sub(r'/\* Q target graphic filters \*/.*?\n\s*\.q\-target \{.*?\}\n', '', content, flags=re.DOTALL)
    new_content = re.sub(r'/\* In light mode hover.*?\.q\-target:hover \{.*?\}\n', '', new_content, flags=re.DOTALL)
    new_content = re.sub(r'html\.dark \.q\-target \{.*?\}\n', '', new_content, flags=re.DOTALL)
    new_content = re.sub(r'html\.dark \.q\-target:hover \{.*?\}\n', '', new_content, flags=re.DOTALL)
    
    if new_content != content:
        with open(f, 'w', encoding='utf-8') as file:
            file.write(new_content)
        count += 1
        print(f'Cleaned CSS in {f}')

print(f'\nSuccessfully cleaned up q-target CSS in {count} HTML files.')
