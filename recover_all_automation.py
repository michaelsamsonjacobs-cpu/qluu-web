import pygetwindow as gw
import pyautogui
import pyperclip
import time
import os

# Disable failsafe for this critical recovery task
pyautogui.FAILSAFE = False

def recover_all_qluu_windows():
    print("Listing all windows to find QLUU pages...")
    all_windows = gw.getAllWindows()
    qluu_windows = [w for w in all_windows if ('QLUU' in w.title or 'localhost:4567' in w.title) and ('Google Chrome' in w.title or 'Microsoft Edge' in w.title)]
    
    print(f"Found {len(qluu_windows)} potential windows.")
    
    for i, w in enumerate(qluu_windows):
        print(f"Processing window {i}: {w.title}")
        try:
            w.restore()
            w.activate()
            time.sleep(1)
            
            # Click inside the window
            pyautogui.click(w.left + 500, w.top + 300)
            time.sleep(0.5)
            
            # Use Ctrl+U to view source
            pyautogui.hotkey('ctrl', 'u')
            time.sleep(3) # Wait for new tab to load
            
            # The active window should now be the view-source tab
            active_w = gw.getActiveWindow()
            print(f"Active window title: {active_w.title}")
            
            # Select all and copy
            pyautogui.hotkey('ctrl', 'a')
            time.sleep(0.5)
            pyautogui.hotkey('ctrl', 'c')
            time.sleep(1)
            
            # Get from clipboard
            source = pyperclip.paste()
            
            if source and '<html' in source.lower():
                # Try to guess filename from title
                title_clean = w.title.split('-')[0].strip().replace('|', '').replace(' ', '_')
                filename = f"recovered_{title_clean}_{int(time.time())}.html"
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(source)
                print(f"Saved source to {filename} ({len(source)} bytes)")
                
                # Close the source tab
                pyautogui.hotkey('ctrl', 'w')
                time.sleep(1)
            else:
                print(f"Failed to get valid source for {w.title}")
                # Try saving with Ctrl+S as fallback
                print("Trying Ctrl+S as fallback...")
                pyautogui.hotkey('ctrl', 's')
                time.sleep(2)
                pyautogui.write(os.path.abspath(f"fallback_{i}.html"))
                pyautogui.press('enter')
                time.sleep(2)
                
        except Exception as e:
            print(f"Error processing {w.title}: {e}")

recover_all_qluu_windows()
print("Done")
