import re

with open(r"c:\Users\Mike\Desktop\new-qluu-website\inspiration\COPY\Marketing Material  2.rtf", "rb") as f:
    raw = f.read()

content = raw.decode("utf-8", errors="ignore")

# Simple RTF-to-text: remove control words, braces, and hex escapes
# Remove font/color tables
content = re.sub(r'\{\\fonttbl[^}]*\}', '', content)
content = re.sub(r'\{\\colortbl[^}]*\}', '', content)
content = re.sub(r'\{\\expandedcolortbl[^}]*\}', '', content)
content = re.sub(r'\{\\listtable[^}]*\}', '', content)
content = re.sub(r'\{\\listoverridetable[^}]*\}', '', content)
content = re.sub(r'\{\\info[^}]*\}', '', content)

# Replace special chars
content = content.replace("\\'97", "—")
content = content.replace("\\'96", "–")
content = content.replace("\\'93", '"')
content = content.replace("\\'94", '"')
content = content.replace("\\'92", "'")
content = content.replace("\\'a0", " ")
content = content.replace("\\'b7", "·")
content = content.replace("\\tab", "\t")
content = content.replace("\\par", "\n")
content = content.replace("\\line", "\n")

# Remove remaining control words
content = re.sub(r'\\[a-zA-Z]+\d*\s?', '', content)
# Remove hex codes
content = re.sub(r"\\'[0-9a-fA-F]{2}", '', content)
# Remove braces
content = re.sub(r'[{}]', '', content)
# Clean up
content = re.sub(r'\n\s*\n', '\n\n', content)
content = re.sub(r'  +', ' ', content)

print(content.strip()[:10000])
