import os, json

history_dir = os.path.expandvars(r'%APPDATA%\Code\User\History')
recover = {}

if not os.path.exists(history_dir):
    print("History directory doesn't exist.")

for root, dirs, files in os.walk(history_dir):
    if 'entries.json' in files:
        entries_path = os.path.join(root, 'entries.json')
        try:
            with open(entries_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            res = str(data.get('resource', ''))
            
            # Check if this history entry is for our project html files
            if 'new-qluu-website' in res and res.endswith('.html'):
                filename = res.split('/')[-1]
                entries = data.get('entries', [])
                
                # Sort entries newest to oldest
                entries_sorted = sorted(entries, key=lambda x: x.get('timestamp', 0), reverse=True)
                
                for entry in entries_sorted:
                    entry_id = entry.get('id')
                    src_file = os.path.join(root, entry_id)
                    
                    if os.path.exists(src_file):
                        # Skip if the backup is less than 1KB (so we skip the 0 byte mistake)
                        if os.path.getsize(src_file) > 1000:
                            if filename not in recover:
                                recover[filename] = src_file
                            break
        except Exception as e:
            pass

for filename, path in recover.items():
    dest = os.path.join('c:/Users/Mike/Desktop/new-qluu-website', filename)
    try:
        with open(path, 'rb') as f:
            content = f.read()
        with open(dest, 'wb') as f:
            f.write(content)
        print(f"Recovered {filename} from {path} (size: {len(content)})")
    except Exception as e:
        print(f"Error recovering {filename}: {e}")

if not recover:
    print("No valid backups found.")
