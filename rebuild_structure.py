import re

file_path = r'c:\Dev\entrevista\output\presentation\criteo_ceo_presentation.html'

with open(file_path, 'r', encoding='utf-8') as f:
    full_content = f.read()

# Split into Head/CSS and Body
header_end = full_content.find('<div class="presentation">') + len('<div class="presentation">')
header = full_content[:header_end]
body_and_footer = full_content[header_end:]

footer_start = body_and_footer.rfind('<script>')
footer = body_and_footer[footer_start:]
body = body_and_footer[:footer_start]

# Now, we extract each slide based on "<!-- Slide" or "<!-- APPENDIX"
# This is tricky because slides are nested now.
# We'll use a regex to find all comment markers that represent a new slide.

# We'll use a more flexible way to find markers.
import re

# Look for patterns like <!-- Slide X: ... --> or <!-- APPENDIX ... -->
markers_regex = r'<!-- (Slide \d+|Executive Summary|APPENDIX.*?)[:\ -]'
matches = list(re.finditer(markers_regex, body, re.IGNORECASE))

slice_points = [m.start() for m in matches]
slice_points.sort()
slice_points.append(len(body))

raw_slides = []
for i in range(len(slice_points)-1):
    raw_slides.append(body[slice_points[i]:slice_points[i+1]])

print(f"Detected {len(raw_slides)} slides.")

# Standardize each slide structure
fixed_slides = []
for i, rs in enumerate(raw_slides):
    # Extract the actual content inside the slide - we'll be aggressive
    # We look for the first <h1> or <div class="slide-content"> and take everything 
    # until we hit the next slide's comment or a slide-number.
    
    # Actually, a safer way:
    # 1. Keep the comment.
    # 2. Re-wrap everything in a clean div.slide and div.slide-content.
    
    # Extract Title (optional) for the slide number if missing
    slide_id = f"SLIDE {i+1}"
    if "APPENDIX" in rs:
        # Try to find which appendix
        app_match = re.search(r'APPENDIX ([A-E])', rs)
        if app_match:
            slide_id = f"APPENDIX {app_match.group(1)}"
    
    # Strip existing slide wrappers and numbers
    # We remove blocks of code that look like slide wrappers or numbers
    to_remove = [
        r'<div class="slide.*?>',
        r'<div class="slide-content.*?>',
        r'<div class="slide-number".*?</div>',
        r'</div>\s+<div class="slide-number".*?</div>\s+</div>',
        r'</div>\s+APPENDIX [A-E]', # Specific stray text I saw
    ]
    clean_rs = rs
    for r_pat in to_remove:
        clean_rs = re.sub(r_pat, '', clean_rs, flags=re.IGNORECASE | re.DOTALL)
    
    # DATA RESCUE: Smart Balancing of Divs
    # The content often contains extra </div> tags that close our wrapper.
    # We must remove exactly enough trailing </div>s to make the content neutral.
    open_divs = len(re.findall(r'<div\b', clean_rs, re.IGNORECASE))
    close_divs = len(re.findall(r'</div>', clean_rs, re.IGNORECASE))
    
    balance = open_divs - close_divs
    
    # If we have more closing than opening, strip the excess from the end
    if balance < 0:
        excess = abs(balance)
        print(f"  [Fix] Slide {slide_id}: Balancing {excess} excess closing divs.")
        # Remove the last 'excess' occurrences of </div>
        # We do this by reversing, replacing first N, then reversing back.
        rs_reversed = clean_rs[::-1]
        rs_reversed = re.sub(r'>vid/<', '', rs_reversed, count=excess, flags=re.IGNORECASE)
        clean_rs = rs_reversed[::-1]
    
    # Special Fix: Slide classes
    slide_class = "slide"
    bg_style = ""
    if "Slide 1: Title" in rs: slide_class = "slide title-slide"
    if "Slide 10: Strategic Summary" in rs: slide_class = "slide summary-slide"
    if "Slide 12: Questions" in rs: slide_class = "slide questions-slide"
    if "APPENDIX" in rs: bg_style = ' style="background: #FAFAFA;"'
    
    # Build clean slide
    fixed_s = f"""
    <div class="{slide_class}"{bg_style}>
        <div class="slide-content" style="width: 95%; max-width: 1200px; margin: 0 auto; padding: 40px 0;">
            {clean_rs.strip()}
        </div>
        <div class="slide-number" style="color: #888;">{slide_id}</div>
    </div>"""
    
    fixed_slides.append(fixed_s)

# Combine everything
new_body = "\n".join(fixed_slides)

# CONSTRUCT FINAL FILE
final_output = header + "\n" + new_body + "\n    </div>\n" + footer

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(final_output)

print("Full structural rebuild complete. 16:9 container restored.")
