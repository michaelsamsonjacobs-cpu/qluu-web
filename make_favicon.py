from PIL import Image

def make_transparent_favicon(input_path, output_path, bg_color=(255, 255, 255), tolerance=30, new_size=(64, 64)):
    try:
        img = Image.open(input_path).convert("RGBA")
        datas = img.getdata()
        
        newData = []
        for item in datas:
            # Change all white (also shades of white)
            if (item[0] >= 255 - tolerance and item[1] >= 255 - tolerance and item[2] >= 255 - tolerance):
                newData.append((255, 255, 255, 0)) # Transparent
            else:
                newData.append(item)
                
        img.putdata(newData)
        
        # Resize to typical favicon sizes (e.g., 64x64) using high-quality resampling
        img = img.resize(new_size, resample=Image.Resampling.LANCZOS)
        
        img.save(output_path, "PNG")
        print(f"Successfully processed and saved to {output_path}")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    make_transparent_favicon("C:/Users/Mike/Desktop/new-qluu-website/assets/favicon_q_raw.png", "C:/Users/Mike/Desktop/new-qluu-website/assets/favicon_q.png", tolerance=5)
