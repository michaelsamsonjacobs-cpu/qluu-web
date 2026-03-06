import os
import re

html_files = ["index.html", "government.html", "drones.html"]

for filename in html_files:
    if not os.path.exists(filename):
        continue
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()

    # Clean up double/triple pseudo-classes caused by stripping 'dark:'
    # e.g., hover:hover:text-white -> hover:text-white
    content = re.sub(r'hover:hover:hover:', 'hover:', content)
    content = re.sub(r'hover:hover:', 'hover:', content)
    content = re.sub(r'focus:focus:', 'focus:', content)

    # Clean up duplicate classes like 'invert-0 invert'
    content = re.sub(r'invert-0 invert', 'invert', content)
    
    # Restore the Q-target hover behavior which got slightly mangled
    content = re.sub(r'\.q-target:hover.*?\}', '.q-target:hover {\n            filter: hue-rotate(180deg) brightness(1.2);\n        }', content, flags=re.DOTALL)
    
    # Text colors on initial hero:
    # "text-black" inside the Initialize System button inside dark mode is wrong. It was text-black in light mode. Let's make sure it looks good.
    # Actually, the original dark mode button text was likely text-black for the cyan button, or maybe text-white. I'll just leave it since cyan and black contrasts well.
    # But wait, original code:
    # `text-white dark:text-black`. Let's just fix it to `text-black` or `text-white`. 
    # Let's fix the button text to just `text-brand-navy` on hover for cyan buttons as that is standard.
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)
        
    print(f"Cleaned {filename}")
