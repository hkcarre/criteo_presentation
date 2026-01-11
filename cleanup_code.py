file_path = r'c:\Dev\entrevista\output\presentation\criteo_ceo_presentation.html'

with open(file_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

start_index = -1
end_index = -1

# Find start of corruption (script> or the end of HUD)
# We know HUD ends with <div id="hud-next-preview">...</div></div></div></div>
# Let's look for the line "hud-next-preview" and go down a few lines
for i, line in enumerate(lines):
    if 'id="hud-next-preview"' in line:
        # The corruption starts a few lines after this
        # Let's find the specific "script>" or "<script>" line after this
        for j in range(i, len(lines)):
            if 'script>' in lines[j] or '<script>' in lines[j] or '<!-- script neutralized -->' in lines[j]:
                start_index = j
                break
        break

# Find end of corruption (Lifeboat script)
for i, line in enumerate(lines):
    if "EMERGENCY LIFEBOAT SCRIPT" in line:
        end_index = i - 1 # Keep the <script> tag of lifeboat
        break

if start_index != -1 and end_index != -1:
    print(f"Removing corruption from line {start_index+1} to {end_index+1}")
    new_lines = lines[:start_index] + lines[end_index:]
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.writelines(new_lines)
    print("Cleanup complete.")
else:
    print(f"Could not find boundaries. Start: {start_index}, End: {end_index}")
