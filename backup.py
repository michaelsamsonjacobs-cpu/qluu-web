import shutil
import os

source_dir = r"c:\Users\Mike\Desktop\new-qluu-website"
output_filename = r"c:\Users\Mike\Desktop\qluu-website-backup"

try:
    shutil.make_archive(output_filename, 'zip', source_dir)
    print(f"Archive created successfully at {output_filename}.zip")
except Exception as e:
    print(f"Error: {e}")
