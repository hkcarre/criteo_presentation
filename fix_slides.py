import re

file_path = r'c:\Dev\entrevista\output\presentation\criteo_ceo_presentation.html'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Remove stray "SLIDE X" text that appears outside of HTML tags
# These are causing the browser to render them as text
patterns_to_remove = [
    r'\n\s*SLIDE \d+\s*\n',  # Stray "SLIDE 1", "SLIDE 2", etc.
    r'\n\s*SLIDE \d+[a-z]?\s*\n',  # Stray "SLIDE 5b", etc.
]

for pattern in patterns_to_remove:
    content = re.sub(pattern, '\n', content, flags=re.IGNORECASE)

# 2. Remove duplicate </div> tags that appear after slide-number
# Pattern: </div>\s*<div class="slide-number"...>SLIDE X</div>\s*</div>
# Should be: <div class="slide-number"...>SLIDE X</div>\s*</div>

# Actually, the issue is more complex. Let me just clean up the stray SLIDE X text first
# and see if that helps.

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Cleaned up stray SLIDE text. Please refresh your browser.")
