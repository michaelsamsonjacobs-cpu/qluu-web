import pygetwindow as gw
import pyautogui
import pyperclip
import time
import os

# Disable failsafe to prevent accidental exits if cursor is near corners
pyautogui.FAILSAFE = False

def recover_contact_page():
    print("Searching for the browser window...")
    # Looking for windows that might be the site
    potential_windows = [w for w in gw.getAllWindows() if any(k in w.title for k in ["QLUU", "localhost", "Google Chrome", "Microsoft Edge"])]
    
    if not potential_windows:
        print("No potential browser windows found.")
        return

    # Try to find the one that is most likely the contact page
    # (Based on user saying "its our contact us")
    target_w = None
    for w in potential_windows:
        if "Contact" in w.title or "QLUU" in w.title:
            target_w = w
            break
    
    if not target_w:
        target_w = potential_windows[0]
        
    print(f"Targeting window: {target_w.title}")
    
    try:
        target_w.restore()
        target_w.activate()
        time.sleep(1)
        
        # Ensure we are actually on the browser by clicking in the viewport area
        pyautogui.click(target_w.left + (target_w.width // 2), target_w.top + 300)
        time.sleep(0.5)

        # Send Ctrl+U to view source
        print("Opening view-source (Ctrl+U)...")
        pyautogui.hotkey('ctrl', 'u')
        time.sleep(3) # Wait for the new tab to load source
        
        # The new tab should be titled "view-source:..."
        source_w = gw.getActiveWindow()
        print(f"Active window title: {source_w.title}")
        
        # Select All and Copy
        print("Copying source content...")
        pyautogui.hotkey('ctrl', 'a')
        time.sleep(0.5)
        pyautogui.hotkey('ctrl', 'c')
        time.sleep(1)
        
        raw_source = pyperclip.paste()
        
        if raw_source and '<html' in raw_source.lower():
            filename = "contact_recovered.html"
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(raw_source)
            print(f"SUCCESS! Recovered source saved to: {os.path.abspath(filename)}")
            print(f"Source size: {len(raw_source)} bytes")
            
            # Close the view-source tab
            pyautogui.hotkey('ctrl', 'w')
            time.sleep(0.5)
        else:
            print("Failed to capture valid HTML source from the clipboard.")
            
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    recover_contact_page()
