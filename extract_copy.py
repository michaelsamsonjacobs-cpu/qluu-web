import os
try:
    import pypdf
    from striprtf.striprtf import rtf_to_text
except ImportError:
    pass # handled by pip

pdf_path = 'c:/Users/Mike/Desktop/new-qluu-website/inspiration/COPY/Copy of Qluu AI Executive Summary.pdf'
rtf1 = 'c:/Users/Mike/Desktop/new-qluu-website/inspiration/COPY/Marketing Material 1.rtf'
rtf2 = 'c:/Users/Mike/Desktop/new-qluu-website/inspiration/COPY/Marketing Material  2.rtf'

with open('c:/Users/Mike/Desktop/new-qluu-website/extracted_copy.txt', 'w', encoding='utf-8') as out:
    out.write("==== PDF EXECUTIVES SUMMARY ====\n")
    try:
        reader = pypdf.PdfReader(pdf_path)
        for page in reader.pages:
            out.write(page.extract_text() + "\n")
    except Exception as e:
        out.write(f"Error reading PDF: {e}\n")
    
    out.write("\n==== MARKETING MATERIAL 1 ====\n")
    try:
        with open(rtf1, 'r', encoding='latin1') as f:
            out.write(rtf_to_text(f.read()))
    except Exception as e:
        out.write(f"Error reading RTF1: {e}\n")

    out.write("\n==== MARKETING MATERIAL 2 ====\n")
    try:
        with open(rtf2, 'r', encoding='latin1') as f:
            out.write(rtf_to_text(f.read()))
    except Exception as e:
        out.write(f"Error reading RTF2: {e}\n")

print("Extraction complete.")
