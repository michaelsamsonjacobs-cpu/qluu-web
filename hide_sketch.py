import glob

files = glob.glob('*.html')
count = 0

for f in files:
    with open(f, 'r', encoding='utf-8') as file:
        content = file.read()
    
    # Target the known structure
    original = 'class="fixed inset-0 pointer-events-none z-0 mix-blend-overlay opacity-10"'
    replacement = 'class="hidden"'
    
    if original in content:
        content = content.replace(original, replacement)
        with open(f, 'w', encoding='utf-8') as file:
            file.write(content)
        count += 1
        print(f'Updated {f}')

print(f'\nSuccessfully hid background artwork in {count} HTML files.')
