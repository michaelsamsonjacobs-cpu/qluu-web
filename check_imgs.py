import os, glob
from PIL import Image

brain_dir = 'C:/Users/Mike/.gemini/antigravity/brain/c905bf25-b103-44f9-8f32-a30bd238ca04'
files = sorted(glob.glob(os.path.join(brain_dir, 'media__*.png')), key=os.path.getmtime)

for f in files[-3:]:
    img = Image.open(f)
    print(os.path.basename(f), img.size)

