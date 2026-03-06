import os
import glob

html_files = glob.glob("*.html")

target_string = '<a href="government.html" class="hover:text-gray-900 dark:text-white transition-colors">Government'
replacement_string = '''<a href="os.html" class="hover:text-gray-900 dark:text-white transition-colors">Operating System</a>
            <a href="government.html" class="hover:text-gray-900 dark:text-white transition-colors">Government'''

for file in html_files:
    try:
        with open(file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        if 'href="os.html"' not in content and target_string in content:
            new_content = content.replace(target_string, replacement_string)
            with open(file, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"Updated {file}")
        elif 'href="os.html"' in content:
            print(f"Already updated {file}")
        else:
            print(f"Could not find target string in {file}")
            
    except Exception as e:
        print(f"Error processing {file}: {e}")
