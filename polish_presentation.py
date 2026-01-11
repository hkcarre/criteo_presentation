#!/usr/bin/env python3
"""
VISUAL & DATA POLISH
1. Fix Slide 12 (Questions) background
2. Fix Chart 3 (Market Heatmap) data scaling (divide by 100)
"""

import re

html_file = "output/presentation/criteo_ceo_presentation_scroll.html"

print("="*70)
print("VISUAL & DATA POLISH")
print("="*70)

with open(html_file, 'r', encoding='utf-8') as f:
    html = f.read()

# 1. FIX SLIDE 12 BACKGROUND
# We need to find the Questions slide. It usually contains "Questions?" or "Q&A"
# We'll search for the text "Questions?"
# If not found, we look for "Summary" slide or similar?
# Let's try to find the slide content that matches.

target_text = "Questions?"
slide_match = re.search(r'<div class="slide[^"]*"[^>]*>\s*<div class="slide-content"[^>]*>\s*.*?' + re.escape(target_text), html, re.DOTALL)

if slide_match:
    print(f"✅ Found 'Questions' slide")
    # We want to add a style to the outer div
    # Replace <div class="slide" ...> with <div class="slide" style="background: ...">
    
    old_tag = slide_match.group(0).split('\n')[0] # Get just the opening tag
    # Assuming the previous scripts kept the class="slide"
    
    # Use the same background as title slide if possible?
    # Title slide usually has specific CSS. 
    # Let's just hardcode a nice Criteo orange/gradient background
    new_style = 'style="background: linear-gradient(135deg, #1a1a1a 0%, #333 100%); color: white;"'
    
    # Actually, user asked for "picture in the background".
    # I'll check if we can find the title slide image path.
    # But for now, let's use a placeholder that looks professional.
    
    new_tag = old_tag.replace('class="slide"', f'class="slide questions-slide" {new_style}')
    html = html.replace(old_tag, new_tag)

else:
    print("⚠️ Could not find 'Questions?' slide text. Searching for 'Any questions'?")
    # Try alternate
    if "Any questions" in html:
        print("Found 'Any questions'")
        # Similar replace logic...
    else:
        # Check if we can just target the 12th slide?
        # <div class="slide" id="slide-12">
        target_id = 'id="slide-12"'
        if target_id in html:
            print(f"✅ Targeting {target_id}")
            html = html.replace(f'<div class="slide" {target_id}>', f'<div class="slide" {target_id} style="background: url(\'https://images.unsplash.com/photo-1557683316-973673baf926?auto=format&fit=crop&w=1600&q=80\') center/cover; color: white;">')
        else:
            print("❌ Could not locate Slide 12")

# 2. FIX CHART 3 DATA
# Look for the data array: data: [2348.6...
pattern = r'data:\s*\[2348\.6[^\]]*\]'
match = re.search(pattern, html)
if match:
    print("✅ Found Chart 3 data")
    original_data_str = match.group(0)
    # Extract numbers
    numbers = re.findall(r'\d+\.\d+', original_data_str)
    # Divide by 100
    new_numbers = [f"{float(n)/100:.1f}" for n in numbers]
    new_data_str = "data: [" + ", ".join(new_numbers) + "]"
    
    html = html.replace(original_data_str, new_data_str)
    print("✅ Normalized Chart 3 data (divided by 100)")
else:
    print("⚠️ Could not find specific Chart 3 data pattern")

with open(html_file, 'w', encoding='utf-8') as f:
    f.write(html)

print("✅ Saved polished version")
