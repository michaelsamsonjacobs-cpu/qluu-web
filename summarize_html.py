import os

html_files = [f for f in os.listdir('.') if f.endswith('.html')]
for f in html_files:
    if os.path.getsize(f) == 0: continue
    try:
        with open(f, 'r', encoding='utf-8') as f_in:
            content = f_in.read()
            title = "None"
            if '<title>' in content:
                title = content.split('<title>')[1].split('</title>')[0].strip()
            
            # Print title and first 100 chars of body
            body_start = ""
            if '<body' in content:
                body_start = content.split('<body')[1][:200].replace('\n', ' ')
            
            print(f"File: {f} | Title: {title} | Body: {body_start[:100]}...")
    except:
        pass
