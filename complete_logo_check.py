import re

# Read the HTML file
with open('output/presentation/criteo_ceo_presentation.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Find ALL slides (including appendices)
all_slides = re.finditer(r'<div class="slide[^"]*"[^>]*>(.*?)<div class="slide-number[^>]*>(.*?)</div>', content, re.DOTALL)

slides_without_logo = []
slide_info = []

for i, match in enumerate(all_slides, 1):
    slide_content = match.group(1)
    slide_number = match.group(2).strip()
    has_logo = 'criteo-logo' in slide_content or 'criteo-logo' in slide_content[:1000]
    
    slide_info.append({
        'position': i,
        'label': slide_number,
        'has_logo': has_logo
    })
    
    if not has_logo:
        slides_without_logo.append((i, slide_number))
    
    status = '✅' if has_logo else '❌'
    print(f"{status} Position {i:2d}: {slide_number}")

if slides_without_logo:
    print(f"\n⚠️  Found {len(slides_without_logo)} slides WITHOUT logos:")
    for pos, label in slides_without_logo:
        print(f"   - Position {pos}: {label}")
else:
    print(f"\n✅ All {len(slide_info)} slides have Criteo logos!")
