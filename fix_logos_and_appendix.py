import re

# Read the HTML
with open('output/presentation/criteo_ceo_presentation.html', 'r', encoding='utf-8') as f:
    content = f.read()

# ISSUE 1: Fix logos - they're rendering as single-line compressed SVG
# The problem is the SVG paths are all on one line making them hard to render
# Let's find and fix the logo structure

print("🔧 Fixing logo rendering issues...")

# Current broken pattern: <svg ...><g fill="#FE5000"><path d="..."/><path d="..."/>...
# We need to ensure SVG has proper structure

# Fix: Add explicit width/height to SVG and ensure it's not compressed to single line
logo_pattern = r'(<div class="criteo-logo">)\s*(<svg[^>]+>)<g fill="#FE5000">'

def fix_logo_structure(match):
    div_start = match.group(1)
    svg_tag = match.group(2)
    
    # Ensure SVG has explicit dimensions
    if 'width=' not in svg_tag or 'height=' not in svg_tag:
        svg_tag = '<svg width="118" height="24" viewBox="0 0 118 24" xmlns="http://www.w3.org/2000/svg">'
    
    return f'''{div_start}
                {svg_tag}
                    <g fill="#FE5000">'''

content = re.sub(logo_pattern, fix_logo_structure, content)

print("✅ Fixed logo SVG structure")

# ISSUE 2: Reverse Appendix C compression - make it readable and centered
print("\n🔧 Reversing Appendix C compression...")

# Find Appendix C section
appendix_c_start = content.find('APPENDIX C: Statistical Deep-Dive')
appendix_c_end = content.find('APPENDIX D:', appendix_c_start)

if appendix_c_start > 0 and appendix_c_end > 0:
    # Extract the section
    before = content[:appendix_c_start-200]  # Include some buffer
    appendix_section = content[appendix_c_start-200:appendix_c_end]
    after = content[appendix_c_end:]
    
    # Restore reasonable formatting
    appendix_section = appendix_section.replace('font-size: 17px', 'font-size: 24px')
    appendix_section = appendix_section.replace('font-size: 12px', 'font-size: 16px')
    appendix_section = appendix_section.replace('font-size: 11px', 'font-size: 14px')
    appendix_section = appendix_section.replace('font-size: 10px', 'font-size: 13px')
    appendix_section = appendix_section.replace('font-size: 9px', 'font-size: 12px')
    appendix_section = appendix_section.replace('padding: 2px', 'padding: 8px')
    appendix_section = appendix_section.replace('padding: 3px', 'padding: 8px')
    appendix_section = appendix_section.replace('padding: 4px', 'padding: 8px')
    appendix_section = appendix_section.replace('padding: 6px', 'padding: 10px')
    appendix_section = appendix_section.replace('margin-top: 6px', 'margin-top: 15px')
    appendix_section = appendix_section.replace('margin-top: 8px', 'margin-top: 15px')
    appendix_section = appendix_section.replace('margin-bottom: 4px', 'margin-bottom: 12px')
    appendix_section = appendix_section.replace('margin-bottom: 6px', 'margin-bottom: 12px')
    
    content = before + appendix_section + after
    print("✅ Restored Appendix C to readable formatting")
else:
    print("⚠️  Could not find Appendix C section")

# Write back
with open('output/presentation/criteo_ceo_presentation.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("\n✅ All fixes applied!")
