import re

# Read the HTML file
with open('output/presentation/criteo_ceo_presentation.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Find all slide numbers
slide_numbers = re.findall(r'<div class="slide-number">(.*?)</div>', content)

print("All slide numbers found:")
for i, num in enumerate(slide_numbers, 1):
    print(f"  Position {i}: {num}")

# Now find slides WITHOUT logos
slides_div = re.finditer(r'<div class="slide"(?:[^>]*)>(.*?)</div>\s*<div class="slide-number', content, re.DOTALL)

print("\nSlides analysis:")
for i, match in enumerate(slides_div, 1):
    slide_content = match.group(1)[:500]  # First 500 chars
    has_logo = 'criteo-logo' in slide_content
    print(f"  Slide position {i}: {'✅ HAS LOGO' if has_logo else '❌ NO LOGO'}")
