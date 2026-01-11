#!/usr/bin/env python3
"""
SCROLL MODE GENERATOR
Converts the rebuilt presentation into a simple scrolling webpage.
Removes all 'slide' hiding logic. Use CSS to just show everything.
"""

html_file = "output/presentation/criteo_ceo_presentation.html" # Using the rebuilt one
output_file = "output/presentation/criteo_ceo_presentation_scroll.html"

print("="*70)
print("GENERATING SCROLLING VERSION")
print("="*70)

with open(html_file, 'r', encoding='utf-8') as f:
    html = f.read()

# 1. CSS Override
# We need to ensure .slide is visible and has margin
css_fix = '''
<style>
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
    
</style>
'''

# Remove the old script that hides slides
html = html.replace('<script>', '<!-- script removed --> <script type="skip">')

# Inject CSS styles before </head>
html = html.replace('</head>', css_fix + '</head>')

# Add a "Scrolling Mode" header badge
ui_header = '''
<div style="position: fixed; top: 0; left: 0; width: 100%; background: #333; color: white; padding: 10px; text-align: center; z-index: 99999;">
    <strong>SCROLL MODE ENABLED</strong> - Scroll down to see all slides
</div>
<div style="height: 50px;"></div>
'''
html = html.replace('<body>', '<body>' + ui_header)

with open(output_file, 'w', encoding='utf-8') as f:
    f.write(html)

print(f"✅ Created: {output_file}")
print("Mode: Vertical Scrolling (All slides visible)")
