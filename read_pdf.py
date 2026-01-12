
import PyPDF2

def extract_pdf_pypdf():
    try:
        with open(r"C:\Dev\entrevista\Waterfall Chart Tutorial & Prompt Template.pdf", 'rb') as f:
            reader = PyPDF2.PdfReader(f)
            text = ""
            for page in reader.pages:
                text += page.extract_text() + "\n"
        
        print("--- EXTRACTED TEXT ---")
        print(text[:2000]) # Print first 2000 chars
        
        # Save to file for full inspection if needed
        with open(r"C:\Dev\entrevista\pdf_content.txt", "w", encoding="utf-8") as f:
            f.write(text)
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    extract_pdf_pypdf()
