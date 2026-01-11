import pdfplumber
from PIL import Image
import os

# Create output directory for images
os.makedirs('brand/extracted', exist_ok=True)

# Open the PDF
pdf_path = 'C:/Dev/entrevista/brand/criteo-strategic-deck (1).pdf'
pdf = pdfplumber.open(pdf_path)

print(f"Total pages: {len(pdf.pages)}\n")

# Try to extract images and analyze each page
for i, page in enumerate(pdf.pages):
    print(f"\n{'='*80}")
    print(f"PAGE {i+1}")
    print(f"{'='*80}")
    
    # Try text extraction
    text = page.extract_text()
    if text:
        print(f"Text: {text[:500]}")
    else:
        print("No text extracted - likely image-based")
    
    # Get page dimensions
    print(f"\nPage dimensions: {page.width} x {page.height}")
    
    # Try to get images
    try:
        # Convert page to image
        im = page.to_image(resolution=150)
        im.save(f'brand/extracted/page_{i+1}.png')
        print(f"✓ Saved screenshot: brand/extracted/page_{i+1}.png")
    except Exception as e:
        print(f"Could not save image: {e}")
    
    # Extract colors if possible
    try:
        # Get page objects
        if hasattr(page, 'objects'):
            print(f"\nPage objects found: {len(page.objects)}")
    except:
        pass

print("\n" + "="*80)
print("BRAND ANALYSIS COMPLETE")
print("="*80)
print("\nCheck brand/extracted/ folder for page screenshots")
print("We'll analyze these visually to extract brand guidelines")
