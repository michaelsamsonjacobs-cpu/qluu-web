import pygetwindow as gw
import pyautogui
import time
import os

print("Available windows:", gw.getAllTitles())

windows = [w for w in gw.getAllWindows() if 'QLUU' in w.title or 'Browser' in w.title or 'localhost' in w.title.lower()]
if not windows:
    print("No matching windows found")
    exit(1)

# Pick the best window (first match)
target = windows[0]
for w in windows:
    if 'QLUU | Government & Defense' in w.title:
        target = w
        break
    
print("Target window:", target.title)

try:
    target.restore()
except:
    pass

try:
    target.activate()
except:
    pass

time.sleep(1)

# Click the window to ensure focus
pyautogui.click(target.left + 200, target.top + 200)
time.sleep(0.5)

print("Sending Ctrl+S")
pyautogui.hotkey('ctrl', 's')
time.sleep(2)

save_path = r"c:\Users\Mike\Desktop\new-qluu-website\os_recovered.html"
if os.path.exists(save_path):
    os.remove(save_path)

print(f"Typing path: {save_path}")
pyautogui.write(save_path)
time.sleep(1)

print("Pressing Enter")
pyautogui.press('enter')
time.sleep(2)

print("Done")
