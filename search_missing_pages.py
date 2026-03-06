import os, io, gzip

def decompress_if_needed(data):
    try:
        if data.startswith(b'\x1f\x8b'):
            return gzip.decompress(data)
    except:
        pass
    return data

def find_pages_in_cache():
    cache_dirs = [
        os.path.expandvars(r'%LOCALAPPDATA%\Microsoft\Edge\User Data\Default\Cache\Cache_Data'),
        os.path.expandvars(r'%LOCALAPPDATA%\Google\Chrome\User Data\Default\Cache\Cache_Data')
    ]
    
    found = 0
    for cache_dir in cache_dirs:
        if not os.path.exists(cache_dir): continue
        files = [os.path.join(cache_dir, f) for f in os.listdir(cache_dir) if f.startswith('f_')]
        for path in files:
            try:
                with open(path, 'rb') as f:
                    data = f.read()
                data = decompress_if_needed(data)
                content = data.decode('utf-8', errors='ignore')
                if '<title>' in content and 'QLUU' in content:
                    title = content.split('<title>')[1].split('</title>')[0].strip()
                    if 'Government' in title or 'Defense' in title or 'Gallery' in title:
                        out_path = f"recovered_cache_{found}_{title.replace(' ', '_')[:20]}.html"
                        with open(out_path, 'w', encoding='utf-8') as out:
                            out.write(content)
                        print(f"Found match: {title} in {path} -> {out_path}")
                        found += 1
            except: pass

find_pages_in_cache()
