import pygetwindow as gw
import pyautogui
import pyperclip
import time
import os

pyautogui.FAILSAFE = False

def recover_tabs_by_index():
    print("Finding the QLUU Chrome window...")
    windows = [w for w in gw.getWindowsWithTitle("QLUU | Autonomous Fleet") if "Google Chrome" in w.title]
    if not windows:
        print("Window not found.")
        return
    
    w = windows[0]
    w.restore()
    w.activate()
    time.sleep(1)
    
    # Click to focus
    pyautogui.click(w.left + 500, w.top + 300)
    time.sleep(0.5)

    seen_sources = {}
    
    for i in range(1, 10): # Try tabs 1 to 9
        print(f"Switching to tab {i} (Ctrl+{i})...")
        pyautogui.hotkey('ctrl', str(i))
        time.sleep(1)
        
        # Get source
        pyautogui.hotkey('ctrl', 'u')
        time.sleep(3)
        
        source_w = gw.getActiveWindow()
        print(f"  Active window: {source_w.title}")
        
        if "view-source" in source_w.title:
            pyautogui.hotkey('ctrl', 'a')
            time.sleep(0.3)
            pyautogui.hotkey('ctrl', 'c')
            time.sleep(1)
            
            source = pyperclip.paste()
            if source and '<html' in source.lower():
                title = "unknown"
                if '<title>' in source:
                    title = source.split('<title>')[1].split('</title>')[0].strip()
                
                if title not in seen_sources or len(source) > len(seen_sources[title]):
                    seen_sources[title] = source
                    filename = f"tab_{i}_{title.replace('|', '').replace(' ', '_')[:30]}.html"
                    with open(filename, 'w', encoding='utf-8') as f:
                        f.write(source)
                    print(f"  SAVED: {filename}")
                else:
                    print(f"  Already have better version of '{title}'")
            
            # Close source tab
            pyautogui.hotkey('ctrl', 'w')
            time.sleep(0.5)
        else:
            print(f"  Could not open source for tab {i}")
            
        # Re-focus main window
        w.activate()
        time.sleep(0.2)

if __name__ == "__main__":
    recover_tabs_by_index()
