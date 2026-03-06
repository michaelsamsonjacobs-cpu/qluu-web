import pygetwindow as gw
import pyautogui
import pyperclip
import time
import os

pyautogui.FAILSAFE = False

def recover_government_page():
    print("Specifically targeting Government page...")
    windows = gw.getWindowsWithTitle("Government & Defense Solutions")
    if not windows:
        windows = [w for w in gw.getAllWindows() if "Government" in w.title]
    
    if not windows:
        print("Government window not found.")
        return

    target_w = windows[0]
    print(f"Targeting window: {target_w.title}")
    
    try:
        target_w.restore()
        target_w.activate()
        time.sleep(1)
        
        # Bring tab to front (assuming it might be one of several tabs)
        # We can't easily iterate tabs until we find it, but let's assume it's the active tab in this window
        pyautogui.click(target_w.left + 500, target_w.top + 300)
        time.sleep(0.5)

        # Ctrl+U
        pyautogui.hotkey('ctrl', 'u')
        time.sleep(4) # More time
        
        pyautogui.hotkey('ctrl', 'a')
        time.sleep(0.5)
        pyautogui.hotkey('ctrl', 'c')
        time.sleep(1)
        
        source = pyperclip.paste()
        if source and '<html' in source.lower():
            filename = "government_recovered.html"
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(source)
            print(f"SUCCESS! Saved to: {os.path.abspath(filename)}")
            pyautogui.hotkey('ctrl', 'w')
        else:
            print("Failed to capture source.")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    recover_government_page()
