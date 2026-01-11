#!/usr/bin/env python3
"""
MANUAL FIX: Move Appendices Separator to Correct Position

Read file, extract separator, remove from beginning, insert before Appendix A
"""

html_file = "output/presentation/criteo_ceo_presentation_scroll.html"

print("="*70)
print("MANUALLY RELOCATING APPENDICES SEPARATOR")
print("="*70)

with open(html_file, 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Find the APPENDICES SEPARATOR block
separator_start = None
separator_end = None

for i, line in enumerate(lines):
    if '<!-- APPENDICES SEPARATOR SLIDE -->' in line:
        separator_start = i
    if separator_start is not None and separator_end is None:
        if '</div>' in line and i > separator_start + 5:  # Find the closing div of separator
            separator_end = i + 1
            break

if separator_start is not None and separator_end is not None:
    # Extract separator lines
    separator_lines = lines[separator_start:separator_end]
    print(f"✅ Found separator at lines {separator_start+1} to {separator_end}")
    
    # Remove separator from current position
    del lines[separator_start:separator_end]
    print(f"✅ Removed separator from lines {separator_start+1}-{separator_end}")
    
    # Find "APPENDIX A:" to insert before it
    appendix_a_line = None
    for i, line in enumerate(lines):
        if 'APPENDIX A:' in line:
            # Go backwards to find the opening <div class="slide"
            for j in range(i, max(0, i-20), -1):
                if '<div class="slide"' in lines[j]:
                    appendix_a_line = j
                    break
            break
    
    if appendix_a_line:
        print(f"✅ Found Appendix A slide start at line {appendix_a_line+1}")
        # Insert separator before Appendix A
        for line in reversed(separator_lines):
            lines.insert(appendix_a_line, line)
        print(f"✅ Inserted separator before Appendix A")
    else:
        print("❌ Could not find Appendix A")
        # Put it back at the end
        lines.extend(separator_lines)
    
    # Save
    with open(html_file, 'w', encoding='utf-8') as f:
        f.writelines(lines)
    
    print("\n✅ File saved - Appendices separator relocated!")
else:
    print("❌ Could not find separator to move")
