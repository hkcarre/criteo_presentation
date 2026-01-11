import re

file_path = r'c:\Dev\entrevista\output\presentation\criteo_ceo_presentation.html'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# The problem pattern is:
# <div class="slide...">
#     </div>          <-- This should NOT be here
# <div class="slide-content"...>   <-- This should be INSIDE the slide
#     ...content...
# </div>

# Fix 1: Remove empty </div> tags right after slide opening
# Pattern: <div class="slide...">whitespace</div>
pattern1 = r'(<div class="slide[^"]*"[^>]*>)\s*</div>\s*\n\s*(<div class="slide-)'
replacement1 = r'\1\n\2'
content, count1 = re.subn(pattern1, replacement1, content)
print(f"Fix 1: Removed {count1} empty closing divs after slide openings")

# Fix 2: Similar pattern but with slide-content
pattern2 = r'(<div class="slide[^"]*"[^>]*>)\s*</div>\s*\n\s*(<div class="slide-content")'
replacement2 = r'\1\n    \2'
content, count2 = re.subn(pattern2, replacement2, content)
print(f"Fix 2: Removed {count2} empty closing divs before slide-content")

# Fix 3: Find slide-content that's NOT inside a slide and wrap it
# This is harder - we need to find orphaned slide-content divs

# For now, let's try a different approach: rebuild ALL slides properly
# using the slide comment markers

# First, let's check what we have after the basic fixes
print("\nAnalyzing structure after basic fixes...")
open_divs = len(re.findall(r'<div', content))
close_divs = len(re.findall(r'</div>', content))
print(f"Open divs: {open_divs}, Close divs: {close_divs}")

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("\nBasic fixes applied. If slides still overlap, a full rebuild is needed.")
