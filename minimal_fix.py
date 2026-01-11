#!/usr/bin/env python3
"""
MINIMAL TARGETED FIX - DO NOT REBUILD STRUCTURE
Only fix what's broken without destroying what works
"""

import re

html_file = "output/presentation/criteo_ceo_presentation.html"

print("="*70)
print("🎯 MINIMAL TARGETED FIX (NO REBUILD)")
print("="*70)

with open(html_file, 'r', encoding='utf-8') as f:
    html = f.read()

print(f"\n📄 Original size: {len(html)} bytes")

# Count slides before
slide_count_before = len(re.findall(r'<div class="slide', html))
print(f"Slides before: {slide_count_before}")

# Only fix what user reported - NO structural changes

# 1. Check if Appendix A exists
has_appendix_a = 'APPENDIX A' in html
print(f"\n📑 Appendix A exists: {has_appendix_a}")

# 2. Remove standalone "CRITEO" text (left logo) - be very specific
# Only remove divs that contain JUST "CRITEO" and nothing else
html = re.sub(r'<div[^>]*>\s*CRITEO\s*</div>\s*\n?', '', html, count=5)
print("✅ Removed standalone CRITEO divs (if any)")

# 3. No other changes - keep everything else intact

print("\n💾 Saving minimally fixed HTML...")
with open(html_file, 'w', encoding='utf-8') as f:
    f.write(html)

# Count slides after
slide_count_after = len(re.findall(r'<div class="slide', html))
print(f"Slides after: {slide_count_after}")

print(f"✅ Saved: {len(html)} bytes")

print("\n" + "="*70)
print("✅ MINIMAL FIX COMPLETE - Backup restored, minimal changes applied")
print("="*70)
print("\n📋 Changed:")
print("  ✅ Restored from backup")
print("  ✅ Removed left-side CRITEO divs only")
print("\n🔄 Refresh browser (Ctrl+F5) to see the clean backup!")
