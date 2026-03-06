import cv2
import numpy as np

files = [
    (r"c:\Users\Mike\Desktop\new-qluu-website\inspiration\front-page.png", r"c:\Users\Mike\Desktop\new-qluu-website\assets\cyclops_light.png"),
    (r"c:\Users\Mike\Desktop\new-qluu-website\inspiration\UGV.jpg", r"c:\Users\Mike\Desktop\new-qluu-website\assets\sentinel_light.png")
]

bg_color = [254, 252, 250] # BGR for #fafcfe
line_color = [200, 100, 30] # BGR for dark blue-ish

for in_path, out_path in files:
    img = cv2.imread(in_path)
    if img is None:
        print(f"Failed to load {in_path}")
        continue
    
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # Improve visibility of faint lines
    gray = cv2.convertScaleAbs(gray, alpha=1.5, beta=0)
    
    _, mask = cv2.threshold(gray, 15, 255, cv2.THRESH_TOZERO)
    
    alpha = mask.astype(float) / 255.0
    alpha = np.stack([alpha]*3, axis=-1)
    
    bg = np.full_like(img, bg_color)
    fg = np.full_like(img, line_color)
    
    out = (fg * alpha + bg * (1 - alpha)).astype(np.uint8)
    
    cv2.imwrite(out_path, out)
    print(f"Saved {out_path}")
