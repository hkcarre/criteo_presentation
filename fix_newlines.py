import re

file_path = r'c:\Dev\entrevista\output\presentation\criteo_ceo_presentation.html'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Fix the literal \n I accidentally introduced
content = content.replace('\\n', '\n')

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Fixed literal newlines.")
