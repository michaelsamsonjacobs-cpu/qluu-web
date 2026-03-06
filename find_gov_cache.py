import os, io, gzip

def decompress_if_needed(data):
    try:
        if data.startswith(b'\x1f\x8b'):
            return gzip.decompress(data)
    except:
        pass
    return data

def find_government_in_cache(cache_dir):
    if not os.path.exists(cache_dir): return
    
    files = []
    for f in os.listdir(cache_dir):
        if f.startswith('f_'):
            path = os.path.join(cache_dir, f)
            files.append(path)
            
    print(f"Checking {len(files)} cache files in {cache_dir}...")
    for path in files:
        try:
            with open(path, 'rb') as f:
                data = f.read()
            data = decompress_if_needed(data)
            content = data.decode('utf-8', errors='ignore')
            if 'Government & Defense Solutions' in content or 'government.html' in content.lower():
                # Extract HTML
                start_idx = content.lower().find('<!doctype html')
                if start_idx == -1: start_idx = content.lower().find('<html')
                if start_idx != -1:
                    html_content = content[start_idx:]
                    out_path = f"cache_gov_found_{os.path.basename(path)}.html"
                    with open(out_path, 'w', encoding='utf-8') as out:
                        out.write(html_content)
                    print(f"FOUND GOVERNMENT PAGE in {path} -> {out_path}")
        except: pass

find_government_in_cache(os.path.expandvars(r'%LOCALAPPDATA%\Microsoft\Edge\User Data\Default\Cache\Cache_Data'))
find_government_in_cache(os.path.expandvars(r'%LOCALAPPDATA%\Google\Chrome\User Data\Default\Cache\Cache_Data'))
