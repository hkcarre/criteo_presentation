import re

with open('output/presentation/criteo_ceo_presentation.html', 'r', encoding='utf-8') as f:
    content = f.read()

# SPLIT BY SLIDES
# We'll split by <div class="slide" (checking for potential style attributes)
# But splitting is risky with regex. Better to use sub with a function that checks content.

def process_slide(match):
    full_slide = match.group(0)
    
    # Check if it is an Appendix Slide
    # Look for "APPENDIX" in comments or h1 tags or slide-numbers
    is_appendix = (
        "APPENDIX" in full_slide.upper() 
        and ("<h1" in full_slide or "slide-number" in full_slide)
        and "slide-number" not in full_slide # Wait, slide-number usually says "APPENDIX A"
    )
    
    # Actually, simpler: check if "APPENDIX" is in the slide content (headers/footer)
    # The comments might be unreliable.
    # Let's check the Title <h1>...APPENDIX...</h1> OR <div class="slide-number">APPENDIX...</div>
    
    has_appendix_header = re.search(r'<h1[^>]*>.*?APPENDIX.*?</h1>', full_slide, re.IGNORECASE | re.DOTALL)
    has_appendix_footer = re.search(r'<div class="slide-number"[^>]*>.*?APPENDIX.*?</div>', full_slide, re.IGNORECASE | re.DOTALL)
    
    if has_appendix_header or has_appendix_footer:
        # It's an appendix. Remove the logo.
        # Remove <div class="criteo-logo">...</div>
        # Use simple string replacement or regex
        clean_slide = re.sub(r'<div class="criteo-logo">.*?</div>', '', full_slide, flags=re.DOTALL)
        print("Removed logo from Appendix Slide")
        return clean_slide
    
    return full_slide

# Apply to all slides
# Pattern matches <div class="slide" ... > ... </div>
# We need to capture the whole slide div. Inner divs might make this hard with regex.
# Since we know the structure is flat (slides are siblings), we can split by <div class="slide"
# But we must be careful.
# Let's try to match the logo specifically inside appendix-looking contexts.

# 1. Remove logos from any block that looks like an Appendix
# We will iterate through all logos and check their context window

logo_iter = re.finditer(r'(<div class="slide"[^>]*>)\s*<div class="criteo-logo">', content)

# This is tricky to replace in place.
# Let's go with a simpler approach: 
# Find the specific Appendix chunks we know exist based on comments.

appendix_comments = [
    "APPENDIX: Data Quality", 
    "APPENDIX B", 
    "APPENDIX C", 
    "APPENDIX D", 
    "APPENDIX E"
]

for section in appendix_comments:
    # Find the section start
    # Then find the first <div class="criteo-logo">...</div> after it and remove it
    # We assume the logo is somewhat close to the comment
    pattern = rf'(<!--\s*{section}.*?-->\s*<div class="slide"[^>]*>)\s*<div class="criteo-logo">.*?</div>'
    
    content = re.sub(pattern, r'\1', content, flags=re.DOTALL | re.IGNORECASE)

print("✅ Removed logos from Appendices based on comments")

with open('output/presentation/criteo_ceo_presentation.html', 'w', encoding='utf-8') as f:
    f.write(content)
