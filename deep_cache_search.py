import os, io, gzip

def decompress_if_needed(data):
    try:
        if data.startswith(b'\x1f\x8b'):
            return gzip.decompress(data)
    except:
        pass
    return data

def check_edge_cache():
    cache_dir = os.path.expandvars(r'%LOCALAPPDATA%\Microsoft\Edge\User Data\Default\Cache\Cache_Data')
    if not os.path.exists(cache_dir): return
    
    found = 0
    files = []
    for f in os.listdir(cache_dir):
        if f.startswith('f_'):
            path = os.path.join(cache_dir, f)
            files.append((path, os.path.getmtime(path), os.path.getsize(path)))
            
    files.sort(key=lambda x: x[1], reverse=True)
    seen_titles = set()

    for path, modtime, size in files[:5000]: # Check more files
        if size < 500: continue
        try:
            with open(path, 'rb') as f:
                data = f.read()
            data = decompress_if_needed(data)
            content = data.decode('utf-8', errors='ignore')
            if ('<html' in content.lower()) and ('qluu' in content.lower()):
                start_idx = content.lower().find('<!doctype html')
                if start_idx == -1: start_idx = content.lower().find('<html')
                if start_idx != -1:
                    html_content = content[start_idx:]
                    title = "unknown"
                    if '<title>' in html_content:
                        title = html_content.split('<title>')[1].split('</title>')[0].strip()
                    if title not in seen_titles:
                        seen_titles.add(title)
                        safe_title = title.replace('|', '').replace(' ', '_').replace('-', '_').replace('__', '_')[:50]
                        out_path = f"cache_find_{safe_title}_{found}.html"
                        with open(out_path, 'w', encoding='utf-8') as out:
                            out.write(html_content)
                        print(f"Found: {title} -> {out_path}")
                        found += 1
        except: pass

check_edge_cache()
