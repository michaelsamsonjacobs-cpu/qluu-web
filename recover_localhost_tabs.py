import pygetwindow as gw
import pyautogui
import pyperclip
import time
import os

pyautogui.FAILSAFE = False

def recover_window_tabs(window_title):
    print(f"Targeting window: {window_title}")
    windows = [w for w in gw.getWindowsWithTitle(window_title) if 'Google Chrome' in w.title]
    if not windows:
        print("Window not found")
        return
    
    w = windows[0]
    w.restore()
    w.activate()
    time.sleep(1)
    
    # Start at tab 1
    pyautogui.hotkey('ctrl', '1')
    time.sleep(0.5)
    
    sources = []
    
    for i in range(15): # Try more tabs
        print(f"Tab {i+1}...")
        w.activate()
        time.sleep(0.3)
        
        # Get source via Ctrl+U
        pyautogui.hotkey('ctrl', 'u')
        time.sleep(2)
        
        # Active window should be the source tab
        pyautogui.hotkey('ctrl', 'a')
        time.sleep(0.3)
        pyautogui.hotkey('ctrl', 'c')
        time.sleep(1)
        
        source = pyperclip.paste()
        if source and '<html' in source.lower():
            title = "unknown"
            if '<title>' in source:
                title = source.split('<title>')[1].split('</title>')[0].strip()
            
            # Simple hash to avoid duplicates
            source_hash = hash(source)
            if source_hash not in sources:
                sources.append(source_hash)
                filename = f"recovered_tab_{int(time.time())}_{i}_{title.replace('|', '').replace(' ', '_')}.html"
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(source)
                print(f"Saved: {filename}")
            
            # Close source tab
            pyautogui.hotkey('ctrl', 'w')
            time.sleep(0.5)
        else:
            print("No valid source found")
            
        # Next tab
        pyautogui.hotkey('ctrl', 'tab')
        time.sleep(0.5)

recover_window_tabs("localhost")
