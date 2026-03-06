import os
import shutil

# Copy image
src_img = r'C:\Users\Mike\.gemini\antigravity\brain\38945b9c-3397-48a1-a6fd-7fdd8c71ee70\world_map_red_1772609005095.png'
dest_img = r'c:\Users\Mike\Desktop\new-qluu-website\assets\defense_learns.png'
if os.path.exists(src_img):
    shutil.copyfile(src_img, dest_img)

# Update HTML files
for f in os.listdir('.'):
    if f.endswith('.html'):
        with open(f, 'r', encoding='utf-8') as file:
            content = file.read()
            
        # 1. Update favicons
        content = content.replace('href="./assets/favicon.png"', 'href="./assets/favicon_q.png"')
        
        # 2. Update index.html specifically for the image
        if f == 'index.html':
            content = content.replace('<img src="./assets/world_model.png" alt="QLUUos Defense"', '<img src="./assets/defense_learns.png" alt="Defense That Learns"')
            
        with open(f, 'w', encoding='utf-8') as file:
            file.write(content)
            
print("Bulk updates complete.")
