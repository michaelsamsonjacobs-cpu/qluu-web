import urllib.request

pages = ["index.html", "os.html", "government.html", "drones.html", "blog.html", "gallery.html", "contact.html"]
base_url = "http://localhost:4567/"

for page in pages:
    url = base_url + page
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response:
            html = response.read()
            with open(page, "wb") as f:
                f.write(html)
            print(f"Recovered {page} from {url}")
    except Exception as e:
        print(f"Failed to recover {page}: {e}")
