import sqlite3
import os
import shutil

def check_history_for_gov():
    paths = [
        os.path.expandvars(r'%LOCALAPPDATA%\Google\Chrome\User Data\Default\History'),
        os.path.expandvars(r'%LOCALAPPDATA%\Microsoft\Edge\User Data\Default\History')
    ]
    
    for path in paths:
        if not os.path.exists(path): continue
        temp_path = "temp_history_gov"
        shutil.copy2(path, temp_path)
        try:
            conn = sqlite3.connect(temp_path)
            c = conn.cursor()
            c.execute("SELECT url, title, last_visit_time FROM urls WHERE url LIKE '%government%' OR title LIKE '%Government%' ORDER BY last_visit_time DESC")
            results = c.fetchall()
            for r in results:
                print(f"History Match: {r[0]} | Title: {r[1]}")
            conn.close()
        except: pass
        if os.path.exists(temp_path): os.remove(temp_path)

check_history_for_gov()
