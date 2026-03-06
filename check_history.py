import os, json

history_dirs = [
    os.path.expandvars(r'%APPDATA%\Code\User\History'),
    os.path.expandvars(r'%APPDATA%\Cursor\User\History')
]

for history_dir in history_dirs:
    if not os.path.exists(history_dir): continue
    for root, dirs, files in os.walk(history_dir):
        if 'entries.json' in files:
            entries_path = os.path.join(root, 'entries.json')
            try:
                with open(entries_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                res = str(data.get('resource', ''))
                
                # Check if it represents any html file from new-qluu-website
                if 'new-qluu-website' in res and res.endswith('.html'):
                    filename = res.split('/')[-1]
                    filename = filename.replace('%5c', '/').split('/')[-1]
                    
                    entries = data.get('entries', [])
                    entries_sorted = sorted(entries, key=lambda x: x.get('timestamp', 0), reverse=True)
                    
                    for entry in entries_sorted:
                        entry_id = entry.get('id')
                        src_file = os.path.join(root, entry_id)
                        
                        if os.path.exists(src_file) and os.path.getsize(src_file) > 1000:
                            print(f"Found backup for {filename}: {src_file}")
                            # Let's write it!
                            with open(src_file, 'rb') as sf:
                                content = sf.read()
                            with open(f"history_recovered_{filename}", 'wb') as outf:
                                outf.write(content)
                            break
            except Exception as e:
                pass

print("Done scanning history")
