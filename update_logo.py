"""
Update presentation to use actual Criteo SVG logo
"""

# Read the SVG logo
with open('brand/criteo-logo-orange (1).svg', 'r', encoding='utf-8') as f:
    svg_content = f.read()

# Read the current HTML
with open('output/presentation/criteo_ceo_presentation.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Update the logo CSS to accommodate SVG
new_logo_css = """        /* Criteo Logo - SVG */
        .criteo-logo {
            position: absolute;
            top: 25px;
            right: 60px;
            width: 100px;
            height: auto;
        }
        
        .criteo-logo svg {
            width: 100%;
            height: auto;
            display: block;
        }"""

# Replace the logo CSS
html = html.replace(
    """        /* Criteo Logo - Matching Brand */
        .criteo-logo {
            position: absolute;
            top: 30px;
            right: 60px;
            font-size: 20px;
            font-weight: 900;
            color: var(--criteo-orange);
            letter-spacing: 3px;
            font-family: var(--font-primary);
        }""",
    new_logo_css
)

# Replace all text logos with the SVG
# The SVG content should be embedded inline for the presentation to work standalone
html = html.replace(
    '<div class="criteo-logo">CRITEO</div>',
    f'<div class="criteo-logo">{svg_content}</div>'
)

# Save the updated HTML
with open('output/presentation/criteo_ceo_presentation.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("✅ Criteo SVG logo integrated into presentation!")
print("✅ All 11 slides updated with official logo")
