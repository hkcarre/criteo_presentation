import re

file_path = r'c:\Dev\entrevista\output\presentation\criteo_ceo_presentation.html'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Standardizing ALL Appendix Slides (A, B, C, D, E)
print("Standardizing all Appendix slides...")

def standardize_appendix(match):
    name = match.group(1) # e.g. "A: Data Quality & Methodology Caveats"
    body = match.group(2) # The content inside slide-content
    
    # Clean the body from any previous inner slide-content or grid-2 overrides
    # We want a fresh slide-content div
    
    # Remove any existing slide-content wrappers if nested (shouldn't be, but just in case)
    # Actually, we replace the whole slide body.
    
    # We use a 1100px max-width centered container.
    new_html = f"""
    <div class="slide" style="background: #FAFAFA;">
        <div class="slide-content" style="width: 100%; max-width: 1100px; margin: 0 auto; padding: 50px 20px;">
            <h1 style="font-size: 26px; margin-bottom: 25px; text-align: left;">APPENDIX {name}</h1>
            <div class="grid-2" style="width: 100%; gap: 60px; display: grid; grid-template-columns: 1fr 1fr;">
                {body}
            </div>
        </div>
        <div class="slide-number" style="color: #888;">APPENDIX {name[0]}</div>
    </div>"""
    return new_html

# We'll do this more carefully.
# Appendix A
content = re.sub(r'<!-- APPENDIX: Data Quality & Methodology -->.*?<div class="slide".*?><div class="slide-content">.*?<h1.*?>APPENDIX A: (.*?)</h1>.*?<div class="grid-2".*?>(.*?)</div>.*?</div>.*?<div class="slide-number".*?>APPENDIX A</div>.*?</div>', 
                 lambda m: standardize_appendix(m), content, flags=re.DOTALL)

# Appendix B
content = re.sub(r'<!-- APPENDIX B: Root Cause Analysis & Data Patterns -->.*?<div class="slide".*?><div class="slide-content">.*?<h1.*?>APPENDIX B: (.*?)</h1>.*?<div class="grid-2".*?>(.*?)</div>.*?</div>.*?<div class="slide-number".*?>APPENDIX B</div>.*?</div>', 
                 lambda m: standardize_appendix(m), content, flags=re.DOTALL)

# Appendix C (The one with the problem)
# Note: I added style to slide-content manually in previous turn, so regex might fail if too specific.
content = re.sub(r'<!-- APPENDIX C: Statistical Deep-Dive -->.*?<div class="slide".*?><div class="slide-content".*?>.*?<h1.*?>APPENDIX C: (.*?)</h1>.*?<div class="grid-2".*?>(.*?)</div>.*?</div>.*?<div class="slide-number".*?>APPENDIX C</div>.*?</div>', 
                 lambda m: standardize_appendix(m), content, flags=re.DOTALL)

# Appendix D
content = re.sub(r'<!-- APPENDIX D: Methodology Transparency & Confidence Levels -->.*?<div class="slide".*?><div class="slide-content">.*?<h1.*?>APPENDIX D: (.*?)</h1>.*?<div class="grid-2".*?>(.*?)</div>.*?</div>.*?<div class="slide-number".*?>APPENDIX D</div>.*?</div>', 
                 lambda m: standardize_appendix(m), content, flags=re.DOTALL)

# Appendix E
content = re.sub(r'<!-- APPENDIX E: Circular Logic Warning - What NOT to Use -->.*?<div class="slide".*?><div class="slide-content">.*?<h1.*?>APPENDIX E: (.*?)</h1>.*?<div class="grid-2".*?>(.*?)</div>.*?</div>.*?<div class="slide-number".*?>APPENDIX E</div>.*?</div>', 
                 lambda m: standardize_appendix(m), content, flags=re.DOTALL)

# 2. Add explicit white color to dark slide logos
print("Ensuring white logo on dark slides...")
content = content.replace(
    '<div class="criteo-logo">',
    '<div class="criteo-logo" style="color: inherit;">'
)

# And specifically for Slide 12 which is summary-slide
# The currentColor should work, but I'll make sure .summary-slide logo is white font.
# Actually, the user wants "White font" -> white wordmark and orange dots.
# My SVG template has fill="currentColor" for letters and #FE5000 for dots.
# So if color is White, font will be white.

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Done!")
