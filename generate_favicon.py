from PIL import Image, ImageDraw, ImageFont
import os

size = 512
img = Image.new('RGBA', (size, size), (3, 9, 20, 255))  # brand-navy
draw = ImageDraw.Draw(img)

cx, cy = size // 2, size // 2

# Draw crosshair lines (red)
red = (220, 38, 38, 255)
line_w = 4
# Horizontal crosshair
draw.rectangle([0, cy - line_w//2, size, cy + line_w//2], fill=red)
# Vertical crosshair
draw.rectangle([cx - line_w//2, 0, cx + line_w//2, size], fill=red)

# Tick marks on crosshairs (red)
tick_len = 24
tick_w = 4
for offset in [80, 160, 240]:
    # Horizontal ticks
    for x in [cx - offset, cx + offset]:
        draw.rectangle([x - tick_w//2, cy - tick_len//2, x + tick_w//2, cy + tick_len//2], fill=red)
    # Vertical ticks
    for y in [cy - offset, cy + offset]:
        draw.rectangle([cx - tick_len//2, y - tick_w//2, cx + tick_len//2, y + tick_w//2], fill=red)

# Draw Q circle (white)
white = (255, 255, 255, 255)
ring_outer = 180
ring_inner = 150
for angle_step in range(360 * 4):
    import math
    angle = math.radians(angle_step / 4)
    for r in range(ring_inner, ring_outer + 1):
        x = int(cx + r * math.cos(angle))
        y = int(cy + r * math.sin(angle))
        if 0 <= x < size and 0 <= y < size:
            img.putpixel((x, y), white)

# Draw Q tail (blue, diagonal slash bottom-right)
blue = (0, 174, 239, 255)
tail_w = 28
for i in range(-tail_w, tail_w):
    for t in range(60, 140):
        x = int(cx + 120 + t * 0.7 + i * 0.5)
        y = int(cy + 120 + t * 0.7 - i * 0.5)
        if 0 <= x < size and 0 <= y < size:
            img.putpixel((x, y), blue)

# Center dot (red)
dot_r = 12
for dx in range(-dot_r, dot_r+1):
    for dy in range(-dot_r, dot_r+1):
        if dx*dx + dy*dy <= dot_r*dot_r:
            img.putpixel((cx+dx, cy+dy), red)

# Save
out_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'assets', 'favicon_q.png')
img.save(out_path)

# Also save a 32x32 ICO-compatible version
img_small = img.resize((32, 32), Image.LANCZOS)
img_small.save(out_path.replace('.png', '_32.png'))

# Save an OG image (1200x630) for social sharing
og = Image.new('RGBA', (1200, 630), (3, 9, 20, 255))
og_draw = ImageDraw.Draw(og)

# Paste the favicon in the center-left
favicon_resized = img.resize((300, 300), Image.LANCZOS)
og.paste(favicon_resized, (80, 165), favicon_resized)

# Add text area
try:
    font_large = ImageFont.truetype("arial.ttf", 72)
    font_small = ImageFont.truetype("arial.ttf", 32)
except:
    font_large = ImageFont.load_default()
    font_small = ImageFont.load_default()

og_draw.text((440, 200), "QLUU AI OS", fill=(255, 255, 255, 255), font=font_large)
og_draw.text((440, 300), "Sovereign AI Defense Platform", fill=(0, 174, 239, 255), font=font_small)
og_draw.text((440, 360), "Deploy once. Defend forever.", fill=(247, 241, 213, 200), font=font_small)

og_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'assets', 'og_image.png')
og.save(og_path)

print(f"Favicon saved to: {out_path}")
print(f"OG image saved to: {og_path}")
