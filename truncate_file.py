file_path = r'c:\Dev\entrevista\output\presentation\criteo_ceo_presentation.html'

with open(file_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Find the line with '</html'
cutoff_index = -1
for i, line in enumerate(lines):
    if '</html' in line:
        cutoff_index = i
        break

if cutoff_index != -1:
    # Keep lines up to cutoff
    new_lines = lines[:cutoff_index]
    # Appending clean closing tags if not present
    # Check if </body> is in the last few lines
    has_body = False
    for l in new_lines[-5:]:
        if '</body>' in l:
            has_body = True
    
    if not has_body:
        new_lines.append('</body>\n')
    
    new_lines.append('</html>')
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.writelines(new_lines)
    print(f"Truncated file at line {cutoff_index+1}. Cleaned up.")
else:
    print("Could not find </html tag to truncate.")
