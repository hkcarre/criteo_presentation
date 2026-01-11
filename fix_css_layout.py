import re

# Read the HTML file
with open('output/presentation/criteo_ceo_presentation.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. ADD CSS FOR GRID AND FIX LOGO SIZE
# ---------------------------------------------------------
css_updates = """
        /* GRID SYSTEM - WAS MISSING */
        .grid-2 {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 40px;
            width: 100%;
            align-items: start;
        }

        /* LOGO FIX - Increase size and ensure visibility */
        .criteo-logo {
            position: absolute;
            top: 25px;
            right: 60px;
            width: 140px; /* Increased from 100px */
            height: auto;
            z-index: 1000; /* Ensure on top */
        }
"""

# Insert CSS before the closing </style> tag if grid-2 doesn't exist
if '.grid-2 {' not in content:
    content = content.replace('</style>', css_updates + '\n    </style>')
else:
    # Just update logo width if grid exists (though grep said it didn't)
    content = content.replace('width: 100px;', 'width: 140px;')

print("✅ Added .grid-2 CSS and increased logo size to 140px")

# 2. FIX LOGO SVG (Use a simpler viewbox approach if needed)
# The previous fix removed xml tags but maybe the paths are still weird.
# We will trust the paths are basically correct but ensure the SVG tag is robust.
# Force width/height on the SVG itself to match aspect ratio
content = re.sub(
    r'<svg width="118px" height="24px" viewBox="0 0 118 24"',
    '<svg width="100%" height="100%" viewBox="0 0 118 24" preserveAspectRatio="xMidYMid meet"',
    content
)

# 3. FIX APPENDIX C LAYOUT (Centralize)
# ---------------------------------------------------------
# User wants it "centralized". 
# We'll make sure the container for Appendix C is centered and the grid works.

# Find Appendix C Grid
# It currently has: <div class="grid-2" style="margin-top: 15px; gap: 20px; max-width: 1400px; margin-left: auto; margin-right: auto;">
# We will ensure the styling is perfect for centering.

app_c_pattern = r'(APPENDIX C: Statistical Deep-Dive.*?<div class="grid-2"[^>]*>)'

def fix_app_c_layout(match):
    # Retrieve the header part
    header_part = match.group(1).split('<div')[0]
    
    # New grid definition for Appendix C specifically
    # logical alignment: center the grid container, but keep 2 columns inside.
    # remove max-width constraint if it's compressing too much, or increase it.
    new_grid_tag = '<div class="grid-2" style="margin-top: 30px; gap: 50px; width: 90%; margin-left: auto; margin-right: auto;">'
    
    return header_part + new_grid_tag

content = re.sub(app_c_pattern, fix_app_c_layout, content, flags=re.DOTALL)
print("✅ Centered Appendix C grid (90% width, auto margins)")

# Write back
with open('output/presentation/criteo_ceo_presentation.html', 'w', encoding='utf-8') as f:
    f.write(content)
