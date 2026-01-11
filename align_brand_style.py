#!/usr/bin/env python3
"""
ALIGN BRAND GUIDELINES
1. Remove "Generic Card" styling (Gray BG, Borders)
2. Apply Criteo "Clean" Styling (White/Light Gray, No borders, Shadow only)
3. Ensure Typography is clean
"""

import re

html_file = "output/presentation/criteo_ceo_presentation_scroll.html"

print("="*70)
print("ALIGNING WITH CRITEO BRAND GUIDELINES")
print("="*70)

with open(html_file, 'r', encoding='utf-8') as f:
    html = f.read()

# 1. REPLACE GENERIC SCROLL CSS WITH BRANDED SCROLL CSS
# We want: 
# - Background: #F5F5F5 (Criteo Light Gray) or White
# - Slides: White, Subtle Shadow (Elevation 1), No Borders
# - Spacing: Clean

branded_css = '''
<style>
    /* CRITEO BRAND ALIGNED SCROLLING */
    
    /* Global Base */
    html, body {
        overflow-y: auto !important;
        height: auto !important;
        background-color: #F8F9FA !important; /* Premium Off-White */
        font-family: "Arial", "Helvetica Neue", sans-serif !important;
        color: #1A1A1A;
    }
    
    .presentation {
        height: auto !important;
        overflow: visible !important;
        padding: 60px 0;
        width: 100% !important;
        display: flex;
        flex-direction: column;
        align-items: center;
        background-color: transparent !important;
        box-shadow: none !important;
    }
    
    /* Slide Styling - "Paper" Look */
    .slide {
        display: block !important;
        position: relative !important;
        opacity: 1 !important;
        transform: none !important;
        top: auto !important;
        left: auto !important;
        
        /* Dimensions - 16:9 ish but flexible for content */
        width: 100% !important;
        max-width: 1100px !important; /* Optimal reading width */
        min-height: 620px;
        margin-bottom: 60px !important;
        
        /* Criteo Card Style */
        background-color: #FFFFFF !important;
        border: none !important;
        border-radius: 8px; /* Modern Soft Radius */
        box-shadow: 0 4px 24px rgba(0, 0, 0, 0.06) !important; /* Soft, Executive Shadow */
        
        padding: 0 !important; /* Let inner content handle padding */
        overflow: visible !important;
    }
    
    .slide-content {
        padding: 50px 60px !important;
    }
    
    /* Title Slide Override */
    .title-slide {
        background-color: #000 !important; /* Fallback */
        color: white !important;
        min-height: 600px;
        display: flex !important;
        flex-direction: column;
        justify-content: center;
    }
    
    /* Separator Slide Override */
    .slide[style*="linear-gradient"] {
        box-shadow: 0 10px 30px rgba(0,0,0,0.15) !important;
    }
    
    /* Hide Nav */
    .progress-bar, .back-to-top, #presenter-hud { display: none !important; }

    /* Typography Polish */
    h1 { font-weight: 800; letter-spacing: -0.5px; }
    h2 { font-weight: 600; color: #1A1A1A; }
    
    /* Fix Table Borders */
    td, th { border-bottom: 1px solid #EEEEEE !important; }
</style>
'''

# Replace the previous "STABLE SCROLL MODE CSS"
# We match the block we inserted in previous step
# It starts with <style>\n    /* STABLE SCROLL MODE CSS */
# We'll use regex to find and replace
scroll_css_pattern = r'<style>\s*/\* STABLE SCROLL MODE CSS \*/.*?</style>'
match = re.search(scroll_css_pattern, html, re.DOTALL)

if match:
    html = html.replace(match.group(0), branded_css)
    print("✅ Replaced Generic CSS with Criteo Branded CSS")
else:
    # If not found (maybe manual edits?), just append to Head
    html = html.replace('</head>', branded_css + '</head>')
    print("✅ Injected Criteo Branded CSS")

# 2. CHECK FOR HEATMAP DATA LOSS
# Just a safety check
if "9.2" not in html or "Revenue at Risk" not in html:
    print("⚠️ WARNING: Heatmap data might be missing. Please verify.")
else:
    print("✅ Heatmap Data confirmed present")

# Save
with open(html_file, 'w', encoding='utf-8') as f:
    f.write(html)

print("\n" + "="*70)
print("BRAND ALIGNMENT COMPLETE")
print("="*70)
print("✅ Background: Premium Off-White (#F8F9FA)")
print("✅ Slides: Clean White, Soft Shadow, No Borders")
print("✅ Typography: Clean Arial/Helvetica")
print("\nPresentation should now look clean and executive.")
