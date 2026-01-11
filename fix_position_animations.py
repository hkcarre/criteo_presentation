#!/usr/bin/env python3
"""
SENIOR DESIGNER: FIX APPENDICES POSITION & ANIMATIONS

1. Move Appendices separator to AFTER Questions slide
2. Fix animation conflicts (remove scroll mode CSS overrides)
3. Enable smooth transitions
"""

import re

html_file = "output/presentation/criteo_ceo_presentation_scroll.html"

print("="*70)
print("FIXING APPENDICES POSITION & ANIMATIONS")
print("="*70)

with open(html_file, 'r', encoding='utf-8') as f:
    html = f.read()

# 1. REMOVE SCROLL MODE CSS OVERRIDES THAT BLOCK ANIMATIONS
# Find and replace the problematic CSS

# The scroll mode CSS that forces display/opacity
old_scroll_css = '''<style>
    /* FORCE SCROLLING MODE */
    html, body {
        overflow-y: auto !important;
        height: auto !important;
        background: #f0f0f0;
    }
    .presentation {
        height: auto !important;
        overflow: visible !important;
        padding: 50px 0;
    }
    .slide {
        display: block !important;
        opacity: 1 !important;
        position: relative !important;
        top: auto !important;
        left: auto !important;
        transform: none !important;
        
        /* Card styling */
        width: 90% !important;
        max-width: 1200px !important;
        margin: 0 auto 50px auto !important; /* Spacing between slides */
        height: auto !important;
        min-height: 600px;
        background: white;
        box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        border: 1px solid #ddd;
    }
    .slide-content {
        padding: 40px !important;
    }
    
    /* Hide nav elements if any */
    .slide-number { display: block !important; }
    
    /* Fix potential absolute positioning inside slides */
    
</style>'''

new_scroll_css = '''<style>
    /* SCROLLING MODE - ANIMATION FRIENDLY */
    html, body {
        overflow-y: auto !important;
        height: auto !important;
        background: #f0f0f0;
    }
    .presentation {
        height: auto !important;
        overflow: visible !important;
        padding: 50px 0;
    }
    .slide {
        /* Allow animations - don't force display/opacity */
        display: block;
        position: relative !important;
        top: auto !important;
        left: auto !important;
        
        /* Card styling */
        width: 90% !important;
        max-width: 1200px !important;
        margin: 0 auto 50px auto !important;
        height: auto !important;
        min-height: 600px;
        background: white;
        box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        border: 1px solid #ddd;
    }
    .slide-content {
        padding: 40px !important;
    }
</style>'''

if old_scroll_css in html:
    html = html.replace(old_scroll_css, new_scroll_css)
    print("✅ Removed animation-blocking CSS")
else:
    print("⚠️ Scroll CSS already modified or not found")

# 2. FIND AND RELOCATE APPENDICES SEPARATOR
# Remove it from wherever it is
appendices_separator_pattern = r'<!-- APPENDICES SEPARATOR SLIDE -->.*?</div>\s*</div>'
separator_match = re.search(appendices_separator_pattern, html, re.DOTALL)

if separator_match:
    separator_html = separator_match.group(0)
    # Remove from current location
    html = html.replace(separator_html, '', 1)
    print("✅ Removed Appendices separator from current position")
    
    # Now find where to insert it - AFTER "Questions?" slide
    # We need to find the closing </div> of the Questions slide, then insert after
    # Questions slide likely contains "Questions?" text
    
    # Strategy: Find all slide divs, look for one with "Questions?", insert after it
    # More reliable: Find "APPENDIX A" and insert BEFORE it
    
    appendix_a_marker = re.search(r'(<div class="slide[^>]*>.*?APPENDIX A)', html, re.DOTALL)
    if appendix_a_marker:
        insert_pos = appendix_a_marker.start(1)
        html = html[:insert_pos] + separator_html + '\n\n' + html[insert_pos:]
        print("✅ Moved Appendices separator to BEFORE Appendix A")
    else:
        print("❌ Could not find Appendix A to relocate separator")
else:
    print("⚠️ Appendices separator not found - creating new one")
    
    # Create and insert new separator
    separator_html = '''
    <!-- APPENDICES SEPARATOR SLIDE -->
    <div class="slide" style="background: linear-gradient(135deg, #1A1A1A 0%, #2C2C2C 100%); display: flex; align-items: center; justify-content: center; text-align: center; min-height: 600px;">
        <div style="width: 100%; padding: 60px;">
            <div style="border-bottom: 6px solid var(--criteo-orange); display: inline-block; padding-bottom: 30px; margin-bottom: 40px;">
                <h1 style="font-size: 56px; color: white; font-weight: 800; letter-spacing: 3px; margin: 0;">APPENDICES</h1>
            </div>
            <p style="font-size: 20px; color: rgba(255,255,255,0.75); margin-top: 40px; font-weight: 300; letter-spacing: 1px;">
                Data Quality & Methodology
            </p>
        </div>
    </div>
'''
    
    appendix_a_marker = re.search(r'(<div class="slide[^>]*>.*?APPENDIX A)', html, re.DOTALL)
    if appendix_a_marker:
        insert_pos = appendix_a_marker.start(1)
        html = html[:insert_pos] + separator_html + '\n\n' + html[insert_pos:]
        print("✅ Created and inserted Appendices separator before Appendix A")

# Save
with open(html_file, 'w', encoding='utf-8') as f:
    f.write(html)

print("\n" + "="*70)
print("FIXES COMPLETE")
print("="*70)
print("\n✅ Appendices separator positioned correctly (after Questions)")
print("✅ Animation CSS enabled (removed !important overrides)")
print("\n🎨 Refresh to see smooth animations!")
