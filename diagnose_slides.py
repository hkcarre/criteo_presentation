import re

file_path = r'c:\Dev\entrevista\output\presentation\criteo_ceo_presentation.html'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. List Slides
print("--- DETECTED SLIDES ---")
matches = re.finditer(r'<div class="slide.*?>(.*?)<div class="slide-number">(.*?)</div>', content, re.DOTALL)
count = 0
for m in matches:
    count += 1
    # Try to find a header
    slide_content = m.group(1)
    slide_num = m.group(2).strip()
    
    header = "No Header"
    h_match = re.search(r'<h[12][^>]*>(.*?)</h[12]>', slide_content)
    if h_match:
        header = h_match.group(1).strip()
        
    print(f"{count}. [{slide_num}] {header[:60]}...")

# 2. Check CSS for .slide
print("\n--- CSS CHECK ---")
css_match = re.search(r'\.slide\s*\{(.*?)\}', content, re.DOTALL)
if css_match:
    print(f".slide CSS: {css_match.group(1)}")
else:
    print("Could not find .slide CSS rule")

# 3. Check Active CSS
css_active = re.search(r'\.slide\.active\s*\{(.*?)\}', content, re.DOTALL)
if css_active:
    print(f".slide.active CSS: {css_active.group(1)}")
