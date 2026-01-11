#!/usr/bin/env python3
"""
ENABLE SCROLLING (FINAL FIX)
The backup was a slideshow (overflow:hidden). 
We must force it to be a vertical scrolling page.
"""

html_file = "output/presentation/criteo_ceo_presentation_scroll.html"

print("="*70)
print("ENABLING VERTICAL SCROLLING")
print("="*70)

with open(html_file, 'r', encoding='utf-8') as f:
    html = f.read()

# CSS to FORCE Scrolling
scroll_css = '''
<style>
    /* FORCE VERTICAL SCROLLING */
    html, body {
        overflow-y: auto !important;
        height: auto !important;
        min-height: 100vh;
        background-color: #f0f0f0;
    }
    
    .presentation {
        height: auto !important;
        overflow: visible !important;
        padding: 50px 0;
        display: block !important;
    }
    
    .slide {
        display: block !important;
        position: relative !important;
        top: auto !important;
        left: auto !important;
        transform: none !important;
        opacity: 1 !important;
        visibility: visible !important;
        
        width: 90% !important;
        max-width: 1200px !important;
        margin: 0 auto 50px auto !important;
        height: auto !important;
        min-height: 600px;
        background: white;
        border: 1px solid #ddd;
        box-shadow: 0 5px 15px rgba(0,0,0,0.1);
    }
    
    /* Hide Navigation UI */
    #presenter-hud, .navigation-controls, .progress-bar { display: none !important; }
</style>
'''

# Inject CSS at end of head
if '</head>' in html:
    html = html.replace('</head>', scroll_css + '</head>')
    print("✅ Injected Scroll CSS")
else:
    print("⚠️ Could not find </head>")

# Remove 'overflow: hidden' from original body style if present inline
html = html.replace('overflow: hidden;', 'overflow: auto;')
print("✅ Removed inline overflow:hidden")

# Save
with open(html_file, 'w', encoding='utf-8') as f:
    f.write(html)

print("\n✅ SCROLLING ENABLED")
print("   - CSS Forced to standard vertical scroll")
print("   - No JS slideshow logic will block it")
