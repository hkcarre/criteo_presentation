import re

with open('output/presentation/criteo_ceo_presentation.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Pattern to find two consecutive criteo-logo divs
duplicate_pattern = r'(<div class="criteo-logo">.*?</div>)\s*<div class="criteo-logo">.*?</div>'

new_content = re.sub(duplicate_pattern, r'\1', content, flags=re.DOTALL)

if new_content != content:
    print("✅ Removed consecutive duplicate logos")
    content = new_content
else:
    print("⚠️  No consecutive duplicates found")

with open('output/presentation/criteo_ceo_presentation.html', 'w', encoding='utf-8') as f:
    f.write(content)
