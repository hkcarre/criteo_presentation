import re

file_path = r'c:\Dev\entrevista\output\presentation\criteo_ceo_presentation.html'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

print(f"File size: {len(content)} bytes")

# Find markers
markers = re.findall(r'<!-- (Slide \d+|APPENDIX [A-Z])', content)
print(f"Found {len(markers)} markers:")
for m in markers:
    print(m)
