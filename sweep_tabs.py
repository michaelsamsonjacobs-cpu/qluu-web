import pygetwindow as gw
import pyautogui
import pyperclip
import time
import os

pyautogui.FAILSAFE = False

def recover_all_possible_tabs():
    print("Listing all browser windows...")
    potential_browsers = [w for w in gw.getAllWindows() if any(b in w.title for b in ["Google Chrome", "Microsoft Edge", "localhost"])]
    
    if not potential_browsers:
        print("No browser windows found.")
        return

    for w_idx, w in enumerate(potential_browsers):
        print(f"Processing window {w_idx}: {w.title}")
        try:
            w.restore()
            w.activate()
            time.sleep(1)
            
            # Start at tab 1
            pyautogui.hotkey('ctrl', '1')
            time.sleep(0.5)
            
            for t_idx in range(12): # Check up to 12 tabs per window
                print(f"  Window {w_idx}, Tab {t_idx+1}...")
                w.activate()
                time.sleep(0.3)
                
                # Get source
                pyautogui.hotkey('ctrl', 'u')
                time.sleep(3)
                
                source_w = gw.getActiveWindow()
                if "view-source" not in source_w.title:
                    print(f"    Failed to open source for Tab {t_idx+1}. Skipping.")
                    pyautogui.hotkey('ctrl', 'tab')
                    continue
                
                pyautogui.hotkey('ctrl', 'a')
                time.sleep(0.5)
                pyautogui.hotkey('ctrl', 'c')
                time.sleep(1)
                
                source = pyperclip.paste()
                if source and '<html' in source.lower():
                    title = "unknown"
                    if '<title>' in source:
                        title = source.split('<title>')[1].split('</title>')[0].strip()
                    
                    # Target specific keywords for files we might be missing
                    if any(k in title.lower() or k in source.lower() for k in ["government", "solutions", "gallery", "portfolio"]):
                        filename = f"recovered_tab_{w_idx}_{t_idx}_{title.replace('|', '').replace(' ', '_')}.html"
                        filename = filename.replace(':', '_').replace('/', '_')
                        with open(filename, 'w', encoding='utf-8') as f:
                            f.write(source)
                        print(f"    SAVED: {filename}")
                    else:
                        print(f"    Skipping (title: {title})")
                    
                    # Close source tab
                    pyautogui.hotkey('ctrl', 'w')
                    time.sleep(0.5)
                else:
                    print("    No source captured.")
                
                # Next tab
                pyautogui.hotkey('ctrl', 'tab')
                time.sleep(0.5)
                
        except Exception as e:
            print(f"  Error in window {w_idx}: {e}")

if __name__ == "__main__":
    recover_all_possible_tabs()
