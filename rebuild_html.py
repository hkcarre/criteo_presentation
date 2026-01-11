import re

file_path = r'c:\Dev\entrevista\output\presentation\criteo_ceo_presentation.html'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Split the file into parts
# 1. Head section (everything before <body>)
# 2. Slides section (all slides)
# 3. Script section (the lifeboat script)
# 4. Footer (</body></html>)

# Find the head section
head_match = re.search(r'(<!DOCTYPE html>.*?</head>)', content, re.DOTALL | re.IGNORECASE)
head_section = head_match.group(1) if head_match else ''

# Find the lifeboat script
script_match = re.search(r'(<script>\s*console\.log\("🚀 EMERGENCY LIFEBOAT.*?</script>)', content, re.DOTALL)
lifeboat_script = script_match.group(1) if script_match else ''

# Find all slide divs - match from <div class="slide to the next <div class="slide or the script
# This is complex because slides are malformed. Let's use a different approach.

# Extract the body content between <body> and the lifeboat script
body_start = content.find('<body>')
script_start = content.find('<script>\r\n                                    console.log("🚀')
if script_start == -1:
    script_start = content.find('<script>\n                                    console.log("🚀')

body_content = content[body_start+6:script_start] if body_start != -1 and script_start != -1 else ''

# Find all slide content using regex - match <!-- Slide X --> comments
slide_pattern = r'<div class="slide[^"]*"[^>]*>.*?(?=<div class="slide|$)'

# Alternative: Find all slide openings and try to match content
# Let's just clean up the stray text and extra </div> tags

# Remove stray SLIDE X text
body_content = re.sub(r'\n\s*SLIDE \d+[a-z]?\s*\n', '\n', body_content, flags=re.IGNORECASE)
body_content = re.sub(r'>\s*SLIDE \d+[a-z]?\s*<', '><', body_content, flags=re.IGNORECASE)

# Remove orphaned </div> tags that appear after slide-number
# Pattern: </div>\s*<div class="slide-number">SLIDE X</div>\s*</div>\s*</div>
# Should be just the slide-number inside the slide

# Count div opens vs closes
open_divs = len(re.findall(r'<div', body_content))
close_divs = len(re.findall(r'</div>', body_content))
print(f"Open divs: {open_divs}, Close divs: {close_divs}")

# The problem is too many close divs. Let's rebuild the structure properly.

# Actually let's take a simpler approach: 
# 1. Find all .slide elements content
# 2. Rebuild the HTML with proper structure

# Find all slide comment markers
slide_markers = list(re.finditer(r'<!-- Slide (\d+[a-z]?):.*?-->', content, re.IGNORECASE))
print(f"Found {len(slide_markers)} slide markers")

# For now, let's just fix the presentation container
# Find <div class="presentation"> and ensure all content until </body> is inside it

# Write a new clean structure
new_content = f'''{head_section}

<body>
    <div class="presentation">
'''

# Extract each slide's content
current_pos = body_content.find('<div class="slide')
while current_pos != -1:
    # Find the next slide start or end of content
    next_slide = body_content.find('<div class="slide', current_pos + 1)
    
    if next_slide == -1:
        # This is the last slide - get content until end
        slide_content = body_content[current_pos:]
    else:
        slide_content = body_content[current_pos:next_slide]
    
    # Clean up the slide content - remove stray text and extra divs
    slide_content = re.sub(r'\n\s*SLIDE \d+[a-z]?\s*\n', '\n', slide_content, flags=re.IGNORECASE)
    slide_content = re.sub(r'>\s*SLIDE \d+[a-z]?\s*<', '><', slide_content, flags=re.IGNORECASE)
    
    # Count divs in this slide
    opens = len(re.findall(r'<div', slide_content))
    closes = len(re.findall(r'</div>', slide_content))
    
    # If there are too many closes, remove the extras
    if closes > opens:
        extra = closes - opens
        # Remove extra </div> from the end
        for _ in range(extra):
            last_close = slide_content.rfind('</div>')
            if last_close != -1:
                slide_content = slide_content[:last_close] + slide_content[last_close+6:]
    elif opens > closes:
        # Add missing closes
        slide_content += '</div>' * (opens - closes)
    
    new_content += slide_content + '\n\n'
    current_pos = next_slide

# Close the presentation container and add the script
new_content += f'''
    </div>
    
{lifeboat_script}
</body>
</html>'''

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(new_content)

print("HTML structure rebuilt successfully!")
print(f"Total length: {len(new_content)} characters")
