import glob

files = glob.glob('*.html')
count = 0

for f in files:
    with open(f, 'r', encoding='utf-8') as file:
        content = file.read()
    
    search_str = 'class="hidden"\n        style="background-image: linear-gradient(rgba(0, 174, 239, 0.4)'
    replace_str = 'class="fixed inset-0 pointer-events-none z-0 mix-blend-overlay opacity-10"\n        style="background-image: linear-gradient(rgba(0, 174, 239, 0.4)'
    
    search_str2 = 'class="hidden" style="background-image: linear-gradient(rgba(0, 174, 239, 0.4)'
    replace_str2 = 'class="fixed inset-0 pointer-events-none z-0 mix-blend-overlay opacity-10" style="background-image: linear-gradient(rgba(0, 174, 239, 0.4)'
    
    search_str3 = 'class="hidden"\r\n        style="background-image: linear-gradient(rgba(0, 174, 239, 0.4)'
    replace_str3 = 'class="fixed inset-0 pointer-events-none z-0 mix-blend-overlay opacity-10"\r\n        style="background-image: linear-gradient(rgba(0, 174, 239, 0.4)'

    modified = False
    if search_str in content:
        content = content.replace(search_str, replace_str)
        modified = True
    elif search_str2 in content:
        content = content.replace(search_str2, replace_str2)
        modified = True
    elif search_str3 in content:
        content = content.replace(search_str3, replace_str3)
        modified = True
        
    if modified:
        with open(f, 'w', encoding='utf-8') as file:
            file.write(content)
        count += 1
        print(f'Updated {f}')

print(f'\nSuccessfully restored blueprint grid in {count} HTML files.')
