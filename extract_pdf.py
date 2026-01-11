import pdfplumber

# Open and extract all text from the PDF
with pdfplumber.open('Case_Study_AXSI_082025.pdf') as pdf:
    full_text = ""
    for i, page in enumerate(pdf.pages):
        full_text += f"\n{'='*80}\nPAGE {i+1}\n{'='*80}\n"
        full_text += page.extract_text()
        full_text += "\n"
    
    # Save to a text file for easier reading
    with open('case_study_extracted.txt', 'w', encoding='utf-8') as f:
        f.write(full_text)
    
    print(full_text)
