import os

def check_chrome_cache():
    cache_dir = os.path.expandvars(r'%LOCALAPPDATA%\Google\Chrome\User Data\Default\Cache\Cache_Data')
    if not os.path.exists(cache_dir):
        print("Chrome cache not found")
        return
    
    print(f"Checking {cache_dir}")
    found = 0
    # Process files newest first
    files = []
    for f in os.listdir(cache_dir):
        if f.startswith('f_'):
            path = os.path.join(cache_dir, f)
            files.append((path, os.path.getmtime(path)))
            
    files.sort(key=lambda x: x[1], reverse=True)
    
    # Check top 500 files
    for path, _ in files[:500]:
        try:
            with open(path, 'rb') as f:
                content = f.read(1000).decode('utf-8', errors='ignore')
                # Check for signs of our html files
                if '<html' in content.lower() and ('qluu' in content.lower() or 'Qluu' in content):
                    print(f"Found match: {path}")
                    print("Preview:", content[:200].replace('\n', ' '))
                    with open(f"cache_recovery_{found}.html", 'w', encoding='utf-8') as out:
                        with open(path, 'rb') as f2:
                            out.write(f2.read().decode('utf-8', errors='ignore'))
                    found += 1
        except Exception:
            pass

check_chrome_cache()
