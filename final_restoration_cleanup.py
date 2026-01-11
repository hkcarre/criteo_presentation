#!/usr/bin/env python3
"""
FINAL RESTORATION CLEANUP
Remove the orphan "Market Perception" HTML that blocks Appendix slides
"""

import re

html_file = "output/presentation/criteo_ceo_presentation.html"

print("="*70)
print("🔧 FINAL RESTORATION CLEANUP")
print("="*70)

with open(html_file, 'r', encoding='utf-8') as f:
    html = f.read()

print(f"\n📄 Size before cleanup: {len(html)} bytes")

# Count slides before
slide_divs_before = len(re.findall(r'<div class="slide', html))
print(f"Slide divs before: {slide_divs_before}")

# CRITICAL FIX: Remove the orphan "Market Perception" content
# This is loose HTML sitting between closing </div> tags
# Pattern: Find "Market Perception" heading and remove everything until the next <div class="slide"
orphan_pattern = r'</div>\s*<h2[^>]*>Market Perception.*?(?=<div class="slide"|<script>|</body>)'

matches = re.findall(orphan_pattern, html, re.DOTALL)
if matches:
    print(f"\n🎯 Found {len(matches)} orphan HTML blocks to remove")
    html = re.sub(orphan_pattern, '</div>\n', html, flags=re.DOTALL)
    print("✅ Removed orphan 'Market Perception' HTML")
else:
    print("ℹ️ No orphan HTML found (might be inside .presentation div)")
    # Try alternative: Find it inside .presentation div but outside any .slide
    alt_pattern = r'(<div class="presentation"[^>]*>.*?)<h2[^>]*>Market Perception.*?(?=<div class="slide")'
    if re.search(alt_pattern, html, re.DOTALL):
        html = re.sub(alt_pattern, r'\1\n', html, flags=re.DOTALL)
        print("✅ Removed orphan from inside .presentation div")

# Count slides after
slide_divs_after = len(re.findall(r'<div class="slide', html))
print(f"Slide divs after: {slide_divs_after}")

print(f"\n💾 Saving cleaned HTML...")
with open(html_file, 'w', encoding='utf-8') as f:
    f.write(html)

print(f"✅ Saved: {len(html)} bytes")

print("\n" + "="*70)
print("✅ RESTORATION CLEANUP COMPLETE!")
print("="*70)
print("\n📋 Changes:")
print(f"  • Removed orphan 'Market Perception' HTML")
print(f"  • Slide divs: {slide_divs_before} → {slide_divs_after}")
print("\n🔄 Refresh browser to verify all Appendix slides are visible!")
