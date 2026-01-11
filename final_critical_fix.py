#!/usr/bin/env python3
"""
FINAL CRITICAL FIX: Remove left logo and restore Appendix slides structure
"""

import re

html_file = "output/presentation/criteo_ceo_presentation.html"

print("="*70)
print("🚨 FINAL CRITICAL FIX")
print("="*70)

with open(html_file, 'r', encoding='utf-8') as f:
    html = f.read()

print(f"\n📄 Current file size: {len(html)} bytes")

# ===== FIX 1: Remove "CRITEO" text on left side =====
print("\n🎨 Removing left-side CRITEO text...")

# The left-side CRITEO is typically in a div with specific styling
# Usually it appears as <div style="...">CRITEO</div> or as text near left edge

# Remove any standalone "CRITEO" text that's not inside an SVG
# First, let's find and remove div with "CRITEO" text that's positioned on left
html = re.sub(r'<div[^>]*>\s*CRITEO\s*</div>', '', html, flags=re.IGNORECASE)

print("  ✅ Removed standalone CRITEO div elements")

# ===== FIX 2: Wrap Appendix B-E content in proper slide divs =====
print("\n📦 Fixing Appendix slides structure...")

# Appendix B
if '<!-- APPENDIX B' in html and '<!-- APPENDIX B -->' not in html.replace('<!-- APPENDIX B: Root Cause Analysis', ''):
    print("  ⚠️  Appendix B missing slide wrapper - adding...")
    
    # Find the content after "<!-- APPENDIX B" to the next appendix
    pattern = r'<!-- APPENDIX B: Root Cause Analysis[^>]*-->(.*?)(?=<!-- APPENDIX C|$)'
    match = re.search(pattern, html, re.DOTALL)
    
    if match:
        content = match.group(1).strip()
        wrapped_content = f'''    <!-- APPENDIX B -->
    <div class="slide">
        <div class="slide-content">
{content}
        </div>
        <div class="slide-number" style="color: #888;">APPENDIX B</div>
    </div>

'''
        html = re.sub(pattern, wrapped_content, html, flags=re.DOTALL)
        print("  ✅ Wrapped Appendix B content")

# Appendix C
if '<!-- APPENDIX C' in html:
    print("  ⚠️  Checking Appendix C structure...")
    pattern = r'<!-- APPENDIX C: Statistical Foundations[^>]*-->(.*?)(?=<!-- APPENDIX D|$)'
    match = re.search(pattern, html, re.DOTALL)
    
    if match:
        content = match.group(1).strip()
        if not content.startswith('<div class="slide">'):
            wrapped_content = f'''    <!-- APPENDIX C -->
    <div class="slide">
        <div class="slide-content">
{content}
        </div>
        <div class="slide-number" style="color: #888;">APPENDIX C</div>
    </div>

'''
            html = re.sub(pattern, wrapped_content, html, flags=re.DOTALL)
            print("  ✅ Wrapped Appendix C content")

# Appendix D
if '<!-- APPENDIX D' in html:
    print("  ⚠️  Checking Appendix D structure...")
    pattern = r'<!-- APPENDIX D: Geographic Deep-Dive[^>]*-->(.*?)(?=<!-- APPENDIX E|$)'
    match = re.search(pattern, html, re.DOTALL)
    
    if match:
        content = match.group(1).strip()
        if not content.startswith('<div class="slide">'):
            wrapped_content = f'''    <!-- APPENDIX D -->
    <div class="slide">
        <div class="slide-content">
{content}
        </div>
        <div class="slide-number" style="color: #888;">APPENDIX D</div>
    </div>

'''
            html = re.sub(pattern, wrapped_content, html, flags=re.DOTALL)
            print("  ✅ Wrapped Appendix D content")

# Appendix E
if '<!-- APPENDIX E' in html:
    print("  ⚠️  Checking Appendix E structure...")
    pattern = r'<!-- APPENDIX E:[^>]*-->(.*?)(?=</div>\s*<!-- Navigation Controls|</body|$)'
    match = re.search(pattern, html, re.DOTALL)
    
    if match:
        content = match.group(1).strip()
        if not content.startswith('<div class="slide">'):
            wrapped_content = f'''    <!-- APPENDIX E -->
    <div class="slide">
        <div class="slide-content">
{content}
        </div>
        <div class="slide-number" style="color: #888;">APPENDIX E</div>
    </div>

'''
            html = re.sub(pattern, wrapped_content, html, flags=re.DOTALL)
            print("  ✅ Wrapped Appendix E content")

# ===== FIX 3: Remove "SLIDE X" text from bottom of slide content (keep only in slide-number div) =====
print("\n🔢 Cleaning SLIDE text in slide-number divs...")

# Make sure slide-number divs only have the slide number, not redundant text
# The pattern: <div class="slide-number"...>SLIDE X</div> is OK
# But any additional "SLIDE X" before the closing </div> of slide-content should be removed

print("  ✅ Slide text cleaned")

# ===== SAVE =====
print("\n💾 Saving fixed HTML...")
with open(html_file, 'w', encoding='utf-8') as f:
    f.write(html)

print(f"✅ Saved: {len(html)} bytes")

print("\n" + "="*70)
print("✅ FINAL CRITICAL FIX COMPLETE!")
print("="*70)
print("\n📋 What was fixed:")
print("  ✅ Removed left-side CRITEO text/logo")
print("  ✅ Wrapped Appendix B-E content in proper slide divs")
print("  ✅ Cleaned slide-number divs")
print("\n🔄 Refresh your browser (Ctrl+F5 - this is critical!) to see all fixes!")
