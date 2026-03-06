import pygetwindow as gw
import pyautogui
import pyperclip
import time
import os

pyautogui.FAILSAFE = False

def recover_tabs_from_browser(window_title):
    print(f"Targeting window: {window_title}")
    windows = gw.getWindowsWithTitle(window_title)
    if not windows:
        print("Window not found")
        return
    
    w = windows[0]
    w.restore()
    w.activate()
    time.sleep(1)
    
    # Go to first tab
    pyautogui.hotkey('ctrl', '1')
    time.sleep(0.5)
    
    seen_sources = set()
    
    for i in range(10): # Try up to 10 tabs
        print(f"Processing tab {i+1}...")
        
        # Bring to front just in case
        w.activate()
        time.sleep(0.5)
        
        # Use Ctrl+U to view source
        pyautogui.hotkey('ctrl', 'u')
        time.sleep(3) # Wait for source tab
        
        # Select all and copy
        pyautogui.hotkey('ctrl', 'a')
        time.sleep(0.5)
        pyautogui.hotkey('ctrl', 'c')
        time.sleep(1)
        
        source = pyperclip.paste()
        
        if source and source not in seen_sources and '<html' in source.lower():
            seen_sources.add(source)
            
            # Extract title if possible
            title = "unknown"
            if '<title>' in source:
                title = source.split('<title>')[1].split('</title>')[0].strip()
            
            filename = f"recovered_tab_{i}_{title.replace('|', '').replace(' ', '_')}_{int(time.time())}.html"
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(source)
            print(f"Saved tab {i+1} source as {filename} ({len(source)} bytes)")
            
            # Close source tab
            pyautogui.hotkey('ctrl', 'w')
            time.sleep(0.5)
        else:
            print(f"Tab {i+1} already seen or invalid.")
            # Still close the source tab if it opened
            pyautogui.hotkey('ctrl', 'w')
            time.sleep(0.5)
            
        # Switch to next tab
        pyautogui.hotkey('ctrl', 'tab')
        time.sleep(0.5)

# Try both Chrome and Edge just in case
recover_tabs_from_browser("Google Chrome")
recover_tabs_from_browser("Microsoft Edge")
