#!/usr/bin/env python3
"""
FINAL CLEANUP SCRIPT
Removes duplicate SLIDE text and ensures Slide 6 has chart canvas
"""

import re

html_file = "output/presentation/criteo_ceo_presentation.html"

print("="*60)
print("🧹 FINAL CLEANUP")
print("="*60)

with open(html_file, 'r', encoding='utf-8') as f:
    html = f.read()

print(f"\n📄 Current size: {len(html)} bytes")

# ===== FIX 1: Remove duplicate "SLIDE SLIDE X" text =====
print("\n🔧 Removing duplicate SLIDE markers...")

# Pattern to match "SLIDE X" repeated multiple times
html = re.sub(r'(SLIDE\s+)+(SLIDE\s+\d+)', r'\2', html, flags=re.IGNORECASE)
html = re.sub(r'(APPENDIX\s+)+(APPENDIX\s+[A-Z])', r'\2', html, flags=re.IGNORECASE)

# More aggressive cleanup - remove standalone "SLIDE" without numbers
html = re.sub(r'\bSLIDE\s+SLIDE\s+', 'SLIDE ', html)

print("  ✅ Duplicate text removed")

# ===== FIX 2: Ensure Slide 6 has Client Risk Chart canvas =====
print("\n📊 Checking Slide 6 for Client Risk Chart...")

if 'id="clientRiskChart"' in html:
    print("  ✅ Client Risk Chart canvas already present")
else:
    print("  ⚠️  Adding Client Risk Chart canvas to Slide 6...")
    
    # Find SLIDE 6 content
    pattern = r'(<!-- SLIDE 6 -->.*?<div class="slide-content">)(.*?)(</div>\s*</div>\s*<!-- SLIDE 7)'
    
    def add_canvas_slide6(match):
        before = match.group(1)
        content = match.group(2)
        after = match.group(3)
        
        canvas_html = '''
                <div style="margin: 20px auto; max-width: 90%; height: 400px;">
                    <canvas id="clientRiskChart"></canvas>
                </div>
'''
        return before + content + canvas_html + after
    
    html = re.sub(pattern, add_canvas_slide6, html, flags=re.DOTALL)
    print("  ✅ Client Risk Chart canvas added to Slide 6")

# ===== SAVE =====
print("\n💾 Saving...")
with open(html_file, 'w', encoding='utf-8') as f:
    f.write(html)

print(f"✅ Saved: {len(html)} bytes")

print("\n" + "="*60)
print("✅ FINAL CLEANUP COMPLETE!")
print("="*60)
print("\n📋 What was fixed:")
print("  • Removed duplicate 'SLIDE SLIDE X' text")
print("  • Added Client Risk Chart canvas to Slide 6")
print("\n🔄 Refresh your browser (Ctrl+F5) to see the clean presentation!")
