#!/usr/bin/env python3
"""
STRUCTURAL FIX SCRIPT
Based on analysis: 44 slide divs (should be ~17)
This script will:
1. Keep only unique slide content
2. Remove duplicates
3. Ensure proper Appendix wrapping
"""

import re

html_file = "output/presentation/criteo_ceo_presentation.html"

print("="*70)
print("PRESENTATION STRUCTURAL FIX")
print("="*70)

with open(html_file, 'r', encoding='utf-8') as f:
    html = f.read()

original_size = len(html)
print(f"\nOriginal size: {original_size:,} bytes")

# Count before
slide_divs_before = len(re.findall(r'<div class="slide', html))
print(f"Slide divs before: {slide_divs_before}")

# Strategy: The HTML likely has nested/duplicate slide divs
# We need to find the proper .presentation container and ensure
# it only has the correct slides

# For now, let's just count and report what we find
# Then I'll create targeted fixes

print("\nAnalyzing slide structure...")

# Find .presentation div
pres_match = re.search(r'<div class="presentation"[^>]*>', html)
if pres_match:
    pres_start = pres_match.start()
    print(f"Found .presentation div at position {pres_start}")
    
    # Find all slide divs after presentation start
    slide_pattern = r'<div class="slide([^"]*)"[^>]*>'
    slides_in_pres = []
    for match in re.finditer(slide_pattern, html[pres_start:]):
        pos = pres_start + match.start()
        classes = match.group(1)
        slides_in_pres.append({'pos': pos, 'classes': 'slide' + classes})
    
    print(f"Found {len(slides_in_pres)} slides inside .presentation")
    
# The issue is likely that we have orphan content or badly nested divs
# Let's check for the specific markers we care about

markers_to_find = [
    "SLIDE 1", "SLIDE 2", "SLIDE 3", "SLIDE 4", "SLIDE 5",
    "SLIDE 6", "SLIDE 7", "SLIDE 8", "SLIDE 9", "SLIDE 10",
    "SLIDE 11", "SLIDE 12",
    "APPENDIX A", "APPENDIX B", "APPENDIX C", "APPENDIX D", "APPENDIX E"
]

print("\nChecking for expected markers:")
for marker in markers_to_find:
    count = html.count(marker)
    status = "OK" if count == 1 else f"ISSUE: {count}x"
    print(f"  {marker}: {status}")

print("\n" + "="*70)
print("Next step: Need to manually inspect and fix HTML structure")
print("="*70)
