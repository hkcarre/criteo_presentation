import re

# Read the HTML file
with open('output/presentation/criteo_ceo_presentation.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. REMOVE LOGOS FROM APPENDICES
# ---------------------------------------------------------
# Find all appendix slides and remove their logos
# Strategy: Find slides containing "APPENDIX" and remove the logo div

appendix_pattern = r'(<!-- APPENDIX [A-Z]:.*?-->\s*<div class="slide">)\s*<div class="criteo-logo">.*?</div>'

def remove_logo(match):
    return match.group(1) # Return the slide start without the logo

new_content = re.sub(appendix_pattern, remove_logo, content, flags=re.DOTALL)

if new_content != content:
    print("✅ Removed logos from Appendix slides")
    content = new_content
else:
    print("⚠️  No Appendix logos found to remove (or pattern mismatch)")


# 2. ENSURE GRID CSS IS PRESENT
# ---------------------------------------------------------
# Check if .grid-2 is actually in the file
if '.grid-2 {' not in content:
    print("⚠️  .grid-2 CSS was missing! Adding it now.")
    css_block = """
        .grid-2 {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 40px;
            width: 100%;
            align-items: start;
        }
    """
    content = content.replace('</style>', css_block + '\n    </style>')
else:
    print("✅ .grid-2 CSS is present")

# 3. VERIFY LOGO CSS
# ---------------------------------------------------------
if 'width: 140px;' in content:
    print("✅ Logo width is 140px")
else:
    print("⚠️  Logo width not 140px, fixing...")
    content = content.replace('.criteo-logo {\n            position: absolute;', 
                            '.criteo-logo {\n            position: absolute;\n            width: 140px;')

# 4. APPENDIX C CENTERING CHECK
# ---------------------------------------------------------
# Ensure Appendix C grid has margin auto
if 'margin-left: auto; margin-right: auto;' in content:
     print("✅ Appendix C grid has auto margins")
else:
     print("⚠️  Appendix C grid missing auto margins")

# Write back
with open('output/presentation/criteo_ceo_presentation.html', 'w', encoding='utf-8') as f:
    f.write(content)
