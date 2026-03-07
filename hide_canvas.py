import glob

files = glob.glob('*.html')
count = 0

for f in files:
    with open(f, 'r', encoding='utf-8') as file:
        content = file.read()
    
    # Target the known structure
    original = '<canvas id="canvas"></canvas>'
    replacement = '<canvas id="canvas" class="hidden"></canvas>'
    
    if original in content:
        content = content.replace(original, replacement)
        with open(f, 'w', encoding='utf-8') as file:
            file.write(content)
        count += 1
        print(f'Updated {f}')

print(f'\nSuccessfully hid 3D artwork canvas in {count} HTML files.')
