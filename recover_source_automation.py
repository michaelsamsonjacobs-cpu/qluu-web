import pygetwindow as gw
import pyautogui
import pyperclip
import time
import os

def recover_window_source(title_keyword):
    print(f"Searching for windows with keyword: {title_keyword}")
    windows = [w for w in gw.getWindowsWithTitle(title_keyword) if 'Google Chrome' in w.title or 'Microsoft Edge' in w.title]
    
    if not windows:
        print(f"No windows found for {title_keyword}")
        return

    for i, w in enumerate(windows):
        print(f"Processing window: {w.title}")
        try:
            w.activate()
            time.sleep(1)
            
            # Click inside the window to ensure focus
            pyautogui.click(w.left + 500, w.top + 500)
            time.sleep(0.5)
            
            # Use Ctrl+U to view source
            pyautogui.hotkey('ctrl', 'u')
            time.sleep(2) # Wait for new tab to load
            
            # Focus new tab
            new_w = gw.getActiveWindow()
            print(f"New window title (source): {new_w.title}")
            
            # Select all and copy
            pyautogui.hotkey('ctrl', 'a')
            time.sleep(0.5)
            pyautogui.hotkey('ctrl', 'c')
            time.sleep(0.5)
            
            # Get from clipboard
            source = pyperclip.paste()
            
            if source:
                filename = f"recovered_source_{i}_{int(time.time())}.html"
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(source)
                print(f"Saved source to {filename} ({len(source)} bytes)")
                
                # Close the source tab
                pyautogui.hotkey('ctrl', 'w')
                time.sleep(0.5)
            else:
                print("Failed to get source from clipboard")
                
        except Exception as e:
            print(f"Error processing {w.title}: {e}")

recover_window_source("QLUU")
