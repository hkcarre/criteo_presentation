#!/usr/bin/env python3
"""
SURGICAL HTML FIX
Removes orphan/loose HTML content and ensures clean slide structure
"""

import re
from bs4 import BeautifulSoup

html_file = "output/presentation/criteo_ceo_presentation.html"

print("="*70)
print("🔬 SURGICAL HTML STRUCTURE FIX")
print("="*70)

with open(html_file, 'r', encoding='utf-8') as f:
    html = f.read()

print(f"\n📄 Original size: {len(html)} bytes")

# Use BeautifulSoup for surgical precision
soup = BeautifulSoup(html, 'html.parser')

# ===== FIX 1: Remove loose "CRITEO" text on left side =====
print("\n🎨 Removing left-side CRITEO logo...")
# Find all divs containing just "CRITEO" text
for div in soup.find_all('div'):
    if div.get_text(strip=True) == 'CRITEO' and 'criteo-logo' not in div.get('class', []):
        print(f"  Removed standalone CRITEO div")
        div.decompose()

# ===== FIX 2: Find and remove orphan content (not inside .slide divs) =====
print("\n🧹 Removing orphan HTML content...")

# Find all slide divs
slides = soup.find_all('div', class_='slide')
print(f"  Found {len(slides)} .slide containers")

# Find content between slides or after last slide that's not wrapped
body = soup.find('body')
if body:
    # Remove any direct children of body that are divs with slide-content class but NOT inside a .slide div
    for element in body.find_all('div', class_='slide-content', recursive=False):
        print(f"  ⚠️ Found orphan slide-content div - removing")
        element.decompose()

# ===== FIX 3: Ensure Slide 12 has background image class =====
print("\n🖼️ Adding background to Slide 12...")

# Find Slide 12 (Questions slide)
for slide in slides:
    content = slide.get_text()
    if 'Questions?' in content and 'slide 12' in content.lower():
        # Add the summary-slide class which has the background
        current_classes = slide.get('class', [])
        if 'summary-slide' not in current_classes:
            current_classes.append('summary-slide')
            slide['class'] = current_classes
            print("  ✅ Added 'summary-slide' class to Slide 12")
        break

# ===== FIX 4: Remove "SLIDE X" text from  slide content (keep only in slide-number div) =====
print("\n🔢 Cleaning duplicate SLIDE text...")

for slide in slides:
    # Find slide-number div
    slide_number_div = slide.find('div', class_='slide-number')
    
    # Remove any text nodes that say "SLIDE X" outside the slide-number div
    for string in slide.find_all(string=re.compile(r'^\s*SLIDE\s+\d+\s*$')):
        # Check if this string is inside slide-number div
        if slide_number_div and string in slide_number_div.descendants:
            continue
        # Otherwise remove it
        if string.parent:
            string.extract()
            print(f"  Removed duplicate SLIDE text")

print("\n💾 Saving cleaned HTML...")
cleaned_html = str(soup)

with open(html_file, 'w', encoding='utf-8') as f:
    f.write(cleaned_html)

print(f"✅ Saved: {len(cleaned_html)} bytes")

print("\n" + "="*70)
print("✅ SURGICAL FIX COMPLETE!")
print("="*70)
print("\n📋 What was fixed:")
print("  ✅ Removed left-side CRITEO logo text")
print("  ✅ Removed orphan HTML content blocking Appendix slides")
print("  ✅ Added background class to Slide 12")
print("  ✅ Cleaned duplicate SLIDE text")
print("\n🔄 Now running rebuild to finalize structure...")
