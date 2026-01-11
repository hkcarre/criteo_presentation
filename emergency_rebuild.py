#!/usr/bin/env python3
"""
EMERGENCY REBUILD SCRIPT
Extracts pure slide content and rebuilds a fresh, clean HTML file.
Ignores all broken structure/wrappers.
"""

import re

html_file = "output/presentation/criteo_ceo_presentation.html"
output_file = "output/presentation/criteo_ceo_presentation_rebuilt.html"

print("="*70)
print("🚑 EMERGENCY PRESENTATION REBUILD")
print("="*70)

with open(html_file, 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Extract HEAD (CSS/Styles)
head_match = re.search(r'<head>.*?</head>', html, re.DOTALL)
if not head_match:
    print("❌ Critical: Could not find <head> section")
    exit(1)
head_content = head_match.group(0)
print("✅ Extracted CSS/Head")

# 2. Extract Slide Content Blocks
# We look for <div class="slide-content"...> ... </div>
# We need to handle nested divs inside content
content_blocks = []

def find_balanced_div(text, start_pos):
    # Find the end of the opening tag
    tag_end = text.find('>', start_pos)
    if tag_end == -1: return None
    
    count = 1
    pos = tag_end + 1
    
    while count > 0 and pos < len(text):
        next_open = text.find('<div', pos)
        next_close = text.find('</div>', pos)
        
        if next_close == -1: return None # Error
        
        if next_open != -1 and next_open < next_close:
            count += 1
            pos = next_open + 1
        else:
            count -= 1
            pos = next_close + 6 # len('</div>')
            
    return text[start_pos:pos]

# Find all starts
start_indices = [m.start() for m in re.finditer(r'<div class="slide-content"', html)]
print(f"🔍 Found {len(start_indices)} potential content blocks")

# Extract balanced blocks
unique_blocks = []
seen_content = set()

for start in start_indices:
    block = find_balanced_div(html, start)
    if block:
        # Simple hash to detect exact duplicates (often created by copy-paste errors)
        content_hash = hash(block)
        if content_hash not in seen_content:
            unique_blocks.append(block)
            seen_content.add(content_hash)

print(f"✅ Extracted {len(unique_blocks)} UNIQUE slide content blocks")

if len(unique_blocks) < 10:
    print("⚠️ Warning: Low slide count. check extraction logic.")
if len(unique_blocks) > 20:
    print("⚠️ Warning: High slide count. Still duplicates?")

# 3. Construct New HTML
print("🔨 Rebuilding file...")

new_html = [
    '<!DOCTYPE html>',
    '<html lang="en">',
    head_content,
    '<body>',
    '<div class="presentation">'
]

# Add slides
for i, block in enumerate(unique_blocks):
    # Determine classes
    classes = "slide"
    if i == 0: classes += " title-slide active" # First slide is title, active
    
    slide_html = f'    <div class="{classes}" id="slide-{i+1}">\n    {block}\n    </div>'
    new_html.append(slide_html)

new_html.append('</div>') # Close presentation

# Add Navigation Script
nav_script = '''
<script>
console.log("🚀 REBUILT NAVIGATION ACTIVE");
document.addEventListener('DOMContentLoaded', () => {
    const slides = document.querySelectorAll('.slide');
    let currentIndex = 0;

    function showSlide(index) {
        if (index < 0) index = 0;
        if (index >= slides.length) index = slides.length - 1;

        slides.forEach((s, i) => {
            s.style.display = (i === index) ? 'block' : 'none';
            s.classList.toggle('active', i === index);
        });
        currentIndex = index;
    }

    document.addEventListener('keydown', (e) => {
        if (e.key === 'ArrowRight' || e.key === ' ') showSlide(currentIndex + 1);
        if (e.key === 'ArrowLeft') showSlide(currentIndex - 1);
    });

    // Init
    showSlide(0);
});
</script>
'''
new_html.append(nav_script)
new_html.append('</body></html>')

# Write Result
with open(output_file, 'w', encoding='utf-8') as f:
    f.write('\n'.join(new_html))

print(f"✅ Created: {output_file}")
print(f"🎉 Total Slides: {len(unique_blocks)}")
