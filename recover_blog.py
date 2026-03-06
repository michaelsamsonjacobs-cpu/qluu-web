import pygetwindow as gw
import pyautogui
import pyperclip
import time
import os

pyautogui.FAILSAFE = False

def recover_blog_page():
    print("Searching for the Blog window...")
    # Target window based on the previous list: "QLUU | cUAS News & Insights"
    target_title = "QLUU | cUAS News & Insights"
    windows = gw.getWindowsWithTitle(target_title)
    
    if not windows:
        # Fallback to general QLUU if the title changed or is partial
        windows = [w for w in gw.getAllWindows() if "QLUU" in w.title and ("Blog" in w.title or "Insights" in w.title)]
    
    if not windows:
        print("Blog window not found.")
        return

    target_w = windows[0]
    print(f"Targeting window: {target_w.title}")
    
    try:
        target_w.restore()
        target_w.activate()
        time.sleep(1)
        
        # Click in viewport
        pyautogui.click(target_w.left + (target_w.width // 2), target_w.top + 300)
        time.sleep(0.5)

        # View source
        print("Opening view-source...")
        pyautogui.hotkey('ctrl', 'u')
        time.sleep(3)
        
        # Source tab
        source_w = gw.getActiveWindow()
        print(f"Source window: {source_w.title}")
        
        # Copy
        pyautogui.hotkey('ctrl', 'a')
        time.sleep(0.5)
        pyautogui.hotkey('ctrl', 'c')
        time.sleep(1)
        
        source = pyperclip.paste()
        
        if source and '<html' in source.lower():
            filename = "blog_recovered.html"
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(source)
            print(f"SUCCESS! Saved to: {os.path.abspath(filename)}")
            
            # Close source tab
            pyautogui.hotkey('ctrl', 'w')
            time.sleep(0.5)
        else:
            print("Failed to capture valid source.")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    recover_blog_page()
