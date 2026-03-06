import os

with open('summary.txt', 'w', encoding='utf-8') as out:
    for f in os.listdir('.'):
        if f.endswith('.html') and os.path.getsize(f) > 0:
            try:
                with open(f, 'r', encoding='utf-8') as f_in:
                    content = f_in.read()
                    title = "None"
                    if '<title>' in content:
                        title = content.split('<title>')[1].split('</title>')[0].strip()
                    out.write(f"File: {f} | Title: {title}\n")
            except:
                pass
