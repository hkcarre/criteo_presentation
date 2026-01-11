"""
Fix Design Integration - Robust Injection
"""

import os

# Define image filenames based on actual directory listing
images = {
    'bg_light': 'images/corporate_abstract_light_1767893409482.png',
    'bg_dark': 'images/digital_strategy_dark_1767893425772.png', 
    'defense': 'images/business_defense_concept_1767893440693.png',
    'map': 'images/market_map_europe_1767893456079.png'
}

print("🔧 FIXING AND ELEVATING DESIGN")
print("="*80)

# Read the HTML
with open('output/presentation/criteo_ceo_presentation.html', 'r', encoding='utf-8') as f:
    html = f.read()

# ============================================================================
# 1. PREMIUM CSS - ROBUST INJECTION
# ============================================================================

premium_css = f"""
        /* ========== PREMIUM CONSULTANCY DESIGN SYSTEM (REPAIRED) ========== */
        
        :root {{
            --glass-bg: rgba(255, 255, 255, 0.92);
            --glass-border: rgba(255, 255, 255, 0.4);
            --glass-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.04);
            --primary-gradient: linear-gradient(135deg, #FF5722 0%, #FF8A65 100%);
        }}

        body {{
            background-color: #f4f4f4;
            background-image: url('{images['bg_light']}');
            background-size: cover;
            background-attachment: fixed;
            background-blend-mode: overlay;
        }}

        /* Glassmorphism Cards */
        .metric-box, .insight-box, .recommendation, .alert-box, table, .summary-highlight {{
            background: var(--glass-bg) !important;
            backdrop-filter: blur(12px);
            -webkit-backdrop-filter: blur(12px);
            border: 1px solid var(--glass-border) !important;
            box-shadow: var(--glass-shadow) !important;
        }}

        /* Typography Upgrades */
        h1, h2, h3 {{
            letter-spacing: -0.5px;
        }}
        
        body {{
            font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif !important;
        }}

        /* Hero Slide (Cover) */
        .title-slide {{
            background-image: 
                linear-gradient(rgba(0,0,0,0.7), rgba(0,0,0,0.6)),
                url('{images['bg_dark']}') !important;
            background-size: cover !important;
            background-position: center !important;
            border: none !important; /* Remove top border */
        }}
        
        .title-slide::before {{ display: none !important; }} /* Remove gradient bar */
        
        .title-slide h1, .title-slide h2, .title-slide p, .title-slide .subtitle, .title-slide div {{
            color: white !important;
            text-shadow: 0 4px 12px rgba(0,0,0,0.5);
        }}
        
        .title-slide h1 {{
            font-weight: 800;
            letter-spacing: -2px;
        }}
        
        .title-slide .criteo-logo path {{
            fill: white !important;
        }}
        
        /* Remove artifacts from cover */
        .title-slide .footer, .title-slide .slide-number, .title-slide ::after {{
            display: none !important;
        }}
        
        /* Market Landscape Slide */
        .slide:nth-child(5) {{
             background-image: 
                linear-gradient(rgba(255,255,255,0.96), rgba(255,255,255,0.96)),
                url('{images['map']}');
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
            background-image: url('{images['defense']}');
            background-size: cover;
            background-position: center;
            opacity: 0.15;
            mask-image: linear-gradient(to left, black, transparent);
            -webkit-mask-image: linear-gradient(to left, black, transparent);
            z-index: 0;
            pointer-events: none;
        }}

        /* Refined Metric Boxes */
        .metric-box {{
            border-radius: 4px;
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
        
        .so-what-label {{
            color: rgba(255,255,255,0.7) !important;
        }}
        
        /* Chart Containers */
        canvas {{
            filter: drop-shadow(0 4px 6px rgba(0,0,0,0.05));
            background: rgba(255,255,255,0.7);
            border-radius: 8px;
            padding: 15px;
            margin: 20px 0;
        }}
"""

# Append CSS to the end of the existing styles
# This is safer than replacing
if '</style>' in html:
    html = html.replace('</style>', premium_css + '\n</style>')
    print("  ✓ Injected Premium CSS with correct image paths")
else:
    print("  ❌ CRITICAL: Could not find </style> tag")

# ============================================================================
# 2. STRUCTURAL FIXES
# ============================================================================

# Apply title-slide class to the first slide
# First slide is usually identifiable by the logo or title
if 'class="slide title-slide"' not in html:
    # Just look for the first occurrence of class="slide"
    html = html.replace('class="slide"', 'class="slide title-slide"', 1)
    print("  ✓ Applied 'title-slide' class to Cover Slide")

# ============================================================================
# 3. SAVE
# ============================================================================

with open('output/presentation/criteo_ceo_presentation.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("\n✅ REPAIR COMPLETE")
print(f"  • Used Light Abstract BG: {images['bg_light']}")
print(f"  • Used Dark Hero BG: {images['bg_dark']}")
print(f"  • Used Map Overlay: {images['map']}")
print(f"  • Used Defense Overlay: {images['defense']}")
