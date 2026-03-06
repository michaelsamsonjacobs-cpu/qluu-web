import pygetwindow as gw
import pyautogui
import pyperclip
import time
import os

pyautogui.FAILSAFE = False

def recover_all_chrome():
    print("Finding all Google Chrome windows...")
    chrome_windows = [w for w in gw.getAllWindows() if "Google Chrome" in w.title]
    
    if not chrome_windows:
        print("No Chrome windows found.")
        return

    for w_idx, w in enumerate(chrome_windows):
        print(f"Processing window {w_idx}: {w.title}")
        try:
            w.restore()
            w.activate()
            time.sleep(1)
            
            # Click to focus
            pyautogui.click(w.left + 500, w.top + 300)
            time.sleep(0.5)

            for i in range(1, 9):
                print(f"  Switching to tab {i} (Ctrl+{i})...")
                pyautogui.hotkey('ctrl', str(i))
                time.sleep(1)
                
                # Get source
                pyautogui.hotkey('ctrl', 'u')
                time.sleep(3)
                
                source_w = gw.getActiveWindow()
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
                        
                        filename = f"chrome_w{w_idx}_t{i}_{title.replace('|', '').replace(' ', '_')[:30]}.html"
                        with open(filename, 'w', encoding='utf-8') as f:
                            f.write(source)
                        print(f"    SAVED: {filename}")
                    
                    pyautogui.hotkey('ctrl', 'w')
                    time.sleep(0.5)
                else:
                    print(f"    No source tab for tab {i}")
                
                w.activate()
                time.sleep(0.2)
        except Exception as e:
            print(f"Error in window {w_idx}: {e}")

if __name__ == "__main__":
    recover_all_chrome()
