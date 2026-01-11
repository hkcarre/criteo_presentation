import re

# Read the HTML file
with open('output/presentation/criteo_ceo_presentation.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Pattern to find and fix malformed SVG logos
# Remove XML declaration inside SVG tags
pattern = r'(<div class="criteo-logo">)\s*<\?xml[^>]+\?>\s*(<svg[^>]*>)'

def fix_svg(match):
    """Remove XML declaration and simplify SVG"""
    return match.group(1) + '\n                ' + match.group(2)

content = re.sub(pattern, fix_svg, content)

# Also remove unnecessary SVG attributes for cleaner code
# Keep only essential attributes
content = re.sub(
    r'<svg width="118px" height="24px" viewBox="0 0 118 24" version="1\.1" xmlns="http://www\.w3\.org/2000/svg"\s+xmlns:xlink="http://www\.w3\.org/1999/xlink">',
    '<svg width="118px" height="24px" viewBox="0 0 118 24" xmlns="http://www.w3.org/2000/svg">',
    content
)

# Remove title tags (not needed)
content = re.sub(r'\s*<title>.*?</title>\s*', '', content, flags=re.DOTALL)

# Simplify nested g tags - remove unnecessary ID wrappers
content = re.sub(
    r'<g id="v5" stroke="none" stroke-width="1" fill="none" fill-rule="evenodd">\s*<g id="Homepage-Revamp-v5" transform="translate\(-165\.000000, -23\.000000\)" fill="#FE5000"\s+fill-rule="nonzero">\s*<g id="Criteo-Logo-Orange" transform="translate\(165\.000000, 23\.000000\)">',
    '<g fill="#FE5000">',
    content
)

# Write back
with open('output/presentation/criteo_ceo_presentation.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ Fixed all Criteo logos - removed XML declarations and simplified SVG structure")
