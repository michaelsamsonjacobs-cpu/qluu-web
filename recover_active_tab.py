import pygetwindow as gw
import pyautogui
import pyperclip
import time
import os

pyautogui.FAILSAFE = False

def recover_active_tab():
    print("Finding active browser window...")
    active_w = gw.getActiveWindow()
    if not active_w:
        print("No active window found.")
        return

    print(f"Active window: {active_w.title}")
    
    # Check if it looks like a browser
    if not any(browser in active_w.title for browser in ["Google Chrome", "Microsoft Edge", "localhost"]):
        print("Active window does not appear to be a browser. Trying to find a browser window...")
        browsers = [w for w in gw.getAllWindows() if any(b in w.title for b in ["Google Chrome", "Microsoft Edge", "localhost"])]
        if not browsers:
            print("No browser windows found.")
            return
        active_w = browsers[0]
        print(f"Using window: {active_w.title}")
        active_w.activate()
        time.sleep(1)

    # View Source
    print("Sending Ctrl+U...")
    pyautogui.hotkey('ctrl', 'u')
    time.sleep(3) # Wait for source tab to open
    
    # New active window should be the source tab
    source_w = gw.getActiveWindow()
    print(f"Source window title: {source_w.title}")
    
    # Select All and Copy
    print("Copying source...")
    pyautogui.hotkey('ctrl', 'a')
    time.sleep(0.5)
    pyautogui.hotkey('ctrl', 'c')
    time.sleep(1)
    
    source = pyperclip.paste()
    if source and '<html' in source.lower():
        title = "recovered_active"
        if '<title>' in source:
            title = source.split('<title>')[1].split('</title>')[0].strip()
        
        filename = f"active_tab_{title.replace('|', '').replace(' ', '_')}_{int(time.time())}.html"
        filename = filename.replace(':', '_').replace('/', '_')
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(source)
        print(f"Successfully collected source! Saved to: {filename}")
        
        # Close the source tab
        pyautogui.hotkey('ctrl', 'w')
        time.sleep(0.5)
    else:
        print("Failed to collect valid HTML source. Source length:", len(source) if source else 0)

if __name__ == "__main__":
    recover_active_tab()
