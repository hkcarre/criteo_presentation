#!/usr/bin/env python3
"""
STABILIZE & SIMPLIFY
1. Remove complex "Premium" animations
2. Verify Slide Order (Title -> Content -> Questions -> Separator -> Appendices)
3. Ensure simple, elegant scroll transitions
4. Verify Heatmap Data is preserved
"""

import re

html_file = "output/presentation/criteo_ceo_presentation_scroll.html"

print("="*70)
print("STABILIZING PRESENTATION")
print("="*70)

with open(html_file, 'r', encoding='utf-8') as f:
    html = f.read()

# 1. REMOVE COMPLEX ANIMATIONS
# Remove "McKinsey Premium Effects" style block
html = re.sub(r'<style>\s*/\* ========== MCKINSEY PREMIUM EFFECTS ========== \*/.*?</style>', '', html, flags=re.DOTALL)
print("✅ Removed complex CSS animations")

# Remove Chart.js animation overrides
html = re.sub(r'<script>\s*// CHART.JS ANIMATION ENHANCEMENTS.*?</script>', '', html, flags=re.DOTALL)
print("✅ Removed complex Chart JS animations")

# 2. ENSURE SIMPLE SCROLL TRANSITIONS
# We keep the simple .slide.is-visible CSS
simple_transition_css = '''
<style>
    /* SIMPLE ELEGANT TRANSITIONS */
    .slide {
        opacity: 0;
        transform: translateY(30px);
        transition: opacity 0.6s ease-out, transform 0.6s ease-out;
        will-change: opacity, transform;
    }
    
    .slide.is-visible {
        opacity: 1;
        transform: translateY(0);
    }
    
    /* Ensure first slide is visible immediately */
    .slide:nth-child(1) {
        opacity: 1;
        transform: translateY(0);
    }
</style>
'''

# Check if simple transition exists, if not add it
if 'SIMPLE ELEGANT TRANSITIONS' not in html:
    # Replace any existing "SCROLL ANIMATION STYLES" or just append to head
    if '/* SCROLL ANIMATION STYLES */' in html:
        html = re.sub(r'<style>\s*/\* SCROLL ANIMATION STYLES \*/.*?</style>', simple_transition_css, html, flags=re.DOTALL)
    else:
        html = html.replace('</head>', simple_transition_css + '</head>')
    print("✅ Enforced simple elegant transitions")

# 3. VERIFY & FIX SLIDE ORDER
# We need to ensure Title Slide is FIRST.
# Find Title Slide
title_slide_match = re.search(r'(<div class="slide title-slide.*?</div>\s*</div>)', html, re.DOTALL)
if title_slide_match:
    title_slide_html = title_slide_match.group(1)
    # Remove it from wherever it is
    html = html.replace(title_slide_html, '')
    
    # Find start of presentation container
    pres_start = html.find('<div class="presentation">')
    if pres_start != -1:
        insert_pos = pres_start + len('<div class="presentation">')
        html = html[:insert_pos] + '\n' + title_slide_html + html[insert_pos:]
        print("✅ Restored Title Slide to position #1")

# Ensure Separator is BEFORE Appendix A
separator_match = re.search(r'(<!-- APPENDICES SEPARATOR SLIDE -->.*?</div>\s*</div>)', html, re.DOTALL)
if separator_match:
    separator_html = separator_match.group(1)
    
    # Check if it's already in correct place (before Appendix A)
    appendix_a_pos = html.find('APPENDIX A:')
    separator_pos = html.find('<!-- APPENDICES SEPARATOR SLIDE -->')
    
    if appendix_a_pos != -1 and separator_pos > appendix_a_pos:
        # It's after! Move it before.
        print("⚠️ Separator found AFTER Appendix A. Moving it...")
        html = html.replace(separator_html, '')
        
        # Find start of Appendix A slide
        # Scan backwards from 'APPENDIX A:' to find <div class="slide"
        # Since we just modified html, indices changed. Let's do a targeted insert.
        
        # Split by slides is safest? No, regex is fine.
        appendix_marker = re.search(r'(<div class="slide[^>]*>.*?APPENDIX A)', html, re.DOTALL)
        if appendix_marker:
            insert_pos = appendix_marker.start(1)
            html = html[:insert_pos] + separator_html + '\n' + html[insert_pos:]
            print("✅ Moved Separator BEFORE Appendix A")

# 4. DATA CHECK
if "Revenue at Risk (€M)" in html and "9.2" in html:
    print("✅ Heatmap Data verified intact")
else:
    print("⚠️ Heatmap Data might be missing!")

# 5. REMOVE ANY "SCROLL MODE ENABLED" BANNER
html = re.sub(r'<div style="position: fixed; top: 0.*?SCROLL MODE ENABLED.*?</div>', '', html, flags=re.DOTALL)

with open(html_file, 'w', encoding='utf-8') as f:
    f.write(html)

print("\n✅ Presentation Stabilized & Simplified")
