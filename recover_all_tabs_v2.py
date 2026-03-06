import pygetwindow as gw
import pyautogui
import pyperclip
import time
import os

# Disable failsafe to prevent disruption
pyautogui.FAILSAFE = False

def recover_all_tabs_from_active_window():
    print("Finding the QLUU window...")
    # Target the window that is likely the one in the screenshot
    windows = [w for w in gw.getAllWindows() if "QLUU" in w.title and "Google Chrome" in w.title]
    
    if not windows:
        print("QLUU Chrome window not found.")
        return

    w = windows[0]
    print(f"Targeting window: {w.title}")
    
    try:
        w.restore()
        w.activate()
        time.sleep(1)
        
        # Go to the first tab (Ctrl+1)
        print("Jumping to first tab...")
        pyautogui.hotkey('ctrl', '1')
        time.sleep(0.5)

        seen_sources = set()
        
        # Iterate through tabs
        for i in range(15): # Assuming no more than 15 tabs
            print(f"Processing tab {i+1}...")
            
            # Re-activate just in case focus was lost
            w.activate()
            time.sleep(0.3)
            
            # Get current source
            pyautogui.hotkey('ctrl', 'u')
            time.sleep(3) # Wait for source tab
            
            # The active window should now be the source
            source_w = gw.getActiveWindow()
            print(f"  Source tab title: {source_w.title}")
            
            if "view-source" not in source_w.title:
                print("  Failed to open source tab or window focus issue. Moving to next tab.")
            else:
                # Copy everything
                pyautogui.hotkey('ctrl', 'a')
                time.sleep(0.3)
                pyautogui.hotkey('ctrl', 'c')
                time.sleep(1)
                
                source = pyperclip.paste()
                
                if source and '<html' in source.lower():
                    # Check if we've seen this content before
                    content_preview = source[:500]
                    if content_preview not in seen_sources:
                        seen_sources.add(content_preview)
                        
                        title = "unknown"
                        if '<title>' in source:
                            title = source.split('<title>')[1].split('</title>')[0].strip()
                        
                        safe_title = title.replace('|', '').replace(' ', '_').replace(':', '_')[:50]
                        filename = f"recovered_tab_{int(time.time())}_{i}_{safe_title}.html"
                        
                        with open(filename, 'w', encoding='utf-8') as f:
                            f.write(source)
                        print(f"  SAVED: {filename} ({len(source)} bytes)")
                    else:
                        print("  Duplicate content detected, skipping save.")
                    
                    # Close ONLY the source tab
                    pyautogui.hotkey('ctrl', 'w')
                    time.sleep(0.5)
                else:
                    print("  Failed to capture valid HTML source.")
                    # Close source tab anyway if it opened
                    pyautogui.hotkey('ctrl', 'w')
                    time.sleep(0.5)
            
            # Switch to next tab in the main window
            w.activate()
            time.sleep(0.2)
            pyautogui.hotkey('ctrl', 'tab')
            time.sleep(0.5)
            
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    recover_all_tabs_from_active_window()
