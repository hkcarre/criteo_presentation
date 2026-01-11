#!/usr/bin/env python3
"""
Generate detailed manual cleanup guide
Maps all slide divs and identifies exact duplicates to remove
"""

import re

html_file = "output/presentation/criteo_ceo_presentation.html"

print("="*80)
print("GENERATING DETAILED MANUAL CLEANUP GUIDE")
print("="*80)

with open(html_file, 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Find all slide div lines with context
slide_divs = []
for i, line in enumerate(lines, 1):
    if '<div class="slide' in line:
        # Get surrounding context
        prev_line = lines[i-2].strip() if i > 1 else ""
        next_line = lines[i].strip() if i < len(lines) else ""
        
        slide_divs.append({
            'line': i,
            'content': line.strip(),
            'prev': prev_line[:80],
            'next': next_line[:80]
        })

print(f"\nTotal slide divs found: {len(slide_divs)}")
print("\nDetailed mapping:")
print("-" * 80)

# Group consecutive duplicates
groups = []
current_group = [slide_divs[0]] if slide_divs else []

for i in range(1, len(slide_divs)):
    if slide_divs[i]['line'] - slide_divs[i-1]['line'] <= 5:  # Within 5 lines = likely duplicate
        current_group.append(slide_divs[i])
    else:
        if current_group:
            groups.append(current_group)
        current_group = [slide_divs[i]]

if current_group:
    groups.append(current_group)

print(f"\nFound {len(groups)} slide groups")
print("\nGROUPS WITH POTENTIAL DUPLICATES:")
print("=" * 80)

cleanup_steps = []
for idx, group in enumerate(groups, 1):
    if len(group) > 1:
        print(f"\n📍 GROUP {idx}: Lines {group[0]['line']}-{group[-1]['line']} ({len(group)} divs)")
        print(f"   ACTION: Likely has {len(group)-1} duplicate(s) to remove")
        
        for div in group:
            print(f"   Line {div['line']:4d}: {div['content'][:70]}")
        
        cleanup_steps.append({
            'group': idx,
            'start_line': group[0]['line'],
            'end_line': group[-1]['line'],
            'div_count': len(group),
            'duplicates': len(group) - 1
        })
    else:
        print(f"\n✅ GROUP {idx}: Line {group[0]['line']} (single div - OK)")

# Generate cleanup guide
print("\n" + "=" * 80)
print("MANUAL CLEANUP STEPS")
print("=" * 80)

print("\n1. Open file: output/presentation/criteo_ceo_presentation.html")
print("2. Go to line number (Ctrl+G in most editors)")
print("3. Remove duplicate <div class=\"slide\"> tags as follows:")
print()

for step in cleanup_steps:
    print(f"\n📝 Step {cleanup_steps.index(step) + 1}:")
    print(f"   Go to lines {step['start_line']}-{step['end_line']}")
    print(f"   Found {step['div_count']} divs, remove {step['duplicates']} duplicate(s)")
    print(f"   Keep ONLY the FIRST <div class=\"slide\"> at line {step['start_line']}")
    print(f"   Delete lines with duplicate divs")

print(f"\n\nTotal cleanup actions: {len(cleanup_steps)}")
print("\n4. After cleanup, save file")
print("5. Refresh browser and test navigation")

# Save detailed report
report_file = "cleanup_guide.txt"
with open(report_file, 'w', encoding='utf-8') as f:
    f.write("MANUAL CLEANUP GUIDE FOR criteo_ceo_presentation.html\n")
    f.write("=" * 80 + "\n\n")
    
    f.write(f"Total slide divs found: {len(slide_divs)}\n")
    f.write(f"Expected: ~17\n")
    f.write(f"Duplicates to remove: ~{len(slide_divs) - 17}\n\n")
    
    f.write("CLEANUP STEPS:\n")
    f.write("-" * 80 + "\n\n")
    
    for step in cleanup_steps:
        f.write(f"Step {cleanup_steps.index(step) + 1}:\n")
        f.write(f"  Lines {step['start_line']}-{step['end_line']}\n")
        f.write(f"  Action: Keep line {step['start_line']}, remove {step['duplicates']} duplicate(s)\n\n")

print(f"\n✅ Detailed report saved to: {report_file}")
print("=" * 80)
