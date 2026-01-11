"""
Elevate Design to Top Consultancy Standards
Senior Designer Implementation
"""

import os

# Define image filenames (based on what we triggered)
# Note: The timestamps in filenames are dynamic, so we'll search for the files
img_dir = 'output/presentation/images'
files = os.listdir(img_dir)

# Map loose filenames to our semantic names
images = {}
for f in files:
    if 'corporate_abstract_light' in f:
        images['bg_light'] = f"images/{f}"
    elif 'digital_strategy_dark' in f:
        images['bg_dark'] = f"images/{f}"
    elif 'business_defense_concept' in f:
        images['defense'] = f"images/{f}"
    elif 'market_map_europe' in f:
        images['map'] = f"images/{f}"

# Read the HTML
with open('output/presentation/criteo_ceo_presentation.html', 'r', encoding='utf-8') as f:
    html = f.read()

print("🎨 IMPLEMENTING PREMIUM DESIGN SYSTEM")
print("="*80)

# ============================================================================
# 1. Advanced CSS: Glassmorphism & Typography
# ============================================================================

premium_css = f"""
    /* ========== PREMIUM CONSULTANCY DESIGN SYSTEM ========== */
    
    :root {{
        --glass-bg: rgba(255, 255, 255, 0.92);
        --glass-border: rgba(255, 255, 255, 0.4);
        --glass-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.04);
        --primary-gradient: linear-gradient(135deg, #FF5722 0%, #FF8A65 100%);
    }}

    body {{
        background-color: #f4f4f4; /* Fallback */
        background-image: url('{images.get('bg_light', '')}');
        background-size: cover;
        background-attachment: fixed;
        background-blend-mode: overlay;
    }}

    /* Glassmorphism Cards */
    .metric-box, .insight-box, .recommendation, .alert-box, table {{
        background: var(--glass-bg) !important;
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border: 1px solid var(--glass-border) !important;
        box-shadow: var(--glass-shadow) !important;
    }}

    /* Typography Upgrades */
    h1, h2, h3 {{
        letter-spacing: -0.5px; /* Tighter, more modern */
    }}
    
    p, li {{
        letter-spacing: 0.2px; /* Better readability */
        line-height: 1.6;
    }}

    /* Hero Slide (Cover) */
    .title-slide {{
        background-image: 
            linear-gradient(rgba(0,0,0,0.7), rgba(0,0,0,0.6)),
            url('{images.get('bg_dark', '')}') !important;
        background-size: cover !important;
        background-position: center !important;
    }}
    
    .title-slide h1, .title-slide p, .title-slide .subtitle {{
        color: white !important;
        text-shadow: 0 2px 4px rgba(0,0,0,0.3);
    }}
    
    .title-slide .criteo-logo path {{
        fill: white !important; /* Make logo white on dark bg */
    }}
    
    /* Market Landscape Slide */
    .slide:nth-child(5) {{
         background-image: 
            linear-gradient(rgba(255,255,255,0.95), rgba(255,255,255,0.95)),
            url('{images.get('map', '')}');
         background-size: cover;
    }}

    /* Strategic Recommendations Slide */
    .slide:nth-child(7) {{
        position: relative;
        overflow: hidden;
    }}
    
    .slide:nth-child(7)::before {{
        content: '';
        position: absolute;
        top: 0; right: 0;
        width: 40%;
        height: 100%;
        background-image: url('{images.get('defense', '')}');
        background-size: cover;
        background-position: center;
        opacity: 0.1;
        mask-image: linear-gradient(to left, black, transparent);
        -webkit-mask-image: linear-gradient(to left, black, transparent);
        z-index: 0;
        pointer-events: none;
    }}

    /* Refined Metric Boxes */
    .metric-box {{
        border-radius: 4px; /* Sharper corners = more corporate */
        border-left: 4px solid var(--criteo-orange) !important;
        padding: 25px !important;
    }}

    /* "So What" Box Premium Look */
    .so-what-box {{
        background: linear-gradient(to right, #2a2a2a, #333) !important;
        border: none !important;
        border-left: 4px solid var(--criteo-orange) !important;
        box-shadow: 0 10px 30px rgba(0,0,0,0.15) !important;
        border-radius: 0 4px 4px 0;
    }}
    
    /* Chart Containers */
    canvas {{
        filter: drop-shadow(0 4px 6px rgba(0,0,0,0.05));
    }}

"""

# Inject CSS
html = html.replace('    </style>', premium_css + '\n    </style>')
print("  ✓ Injected premium Glassmorphism CSS")
print("  ✓ Integrated 4 high-res generated images")


# ============================================================================
# 2. HTML Structural Improvements for Design
# ============================================================================

# Improve Slide 1 (Cover) Structure for Dark Mode
# We need to make sure the logo is visible. The CSS handles the fill, but let's add a container class
if 'class="slide title-slide"' in html:
    pass # Already has class
else:
    # Find the title slide div (usually the first slide)
    # It's identified by "Criteo Executive Review" usually
    if '<!-- Slide 1: Title' in html:
        html = html.replace('<div class="slide"', '<div class="slide title-slide"', 1)
        print("  ✓ Upgraded Cover Slide to Dark Mode Hero")

# ============================================================================
# 3. Save
# ============================================================================

with open('output/presentation/criteo_ceo_presentation.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("\n✅ DESIGN ELEVATION COMPLETE")
print("  • Cover Slide: Dark, futuristic data abstract (Premium Tech)")
print("  • General Slides: Subtle 'white corporate' texture (No more flat white)")
print("  • Content: Glassmorphism capability added")
print("  • Typography: Tightened for executive polish")
print("  • Images: Strategically placed for visual depth")
