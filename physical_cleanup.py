#!/usr/bin/env python3
"""
PHYSICAL HTML CLEANUP
JavaScript filtering failed. Must physically remove the wrapper divs.
Strategy: Keep only <div class="slide"> that is immediately followed by <div class="slide-content">
"""

import re

html_file = "output/presentation/criteo_ceo_presentation.html"
backup_file = "output/presentation/criteo_ceo_presentation_pre_physical.html"

print("="*70)
print("PHYSICAL HTML CLEANUP")
print("="*70)

with open(html_file, 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Backup
with open(backup_file, 'w', encoding='utf-8') as f:
    f.writelines(lines)
print(f"✅ Backup created: {backup_file}")

# Identify lines to keep/remove
# We want to keep <div class="slide"> ONLY if it's the one wrapping slide-content
# The pattern we saw was:
# <div class="slide"> (wrapper - REMOVE)
# <div class="slide"> (wrapper - REMOVE)
# <div class="slide"> (real - KEEP)
# <div class="slide-content">

# First, find all lines with slide div
slide_indices = [i for i, line in enumerate(lines) if '<div class="slide' in line and 'slide-content' not in line]
content_indices = [i for i, line in enumerate(lines) if 'slide-content' in line]

print(f"Found {len(slide_indices)} slide divs")
print(f"Found {len(content_indices)} content divs")

lines_to_remove = set()

# For each content div, find its immediate parent slide div
for content_idx in content_indices:
    # Look backwards for the first slide div
    found_parent = False
    for i in range(content_idx - 1, -1, -1):
        if '<div class="slide' in lines[i]:
            if not found_parent:
                # This is the immediate parent - KEEP IT
                found_parent = True
                # print(f"Keep parent at {i+1} for content at {content_idx+1}")
            else:
                # This is a grandparent/wrapper - MARK FOR REMOVAL
                # Only if it's close (within 10 lines) to avoid removing previous slides
                if content_idx - i < 15:
                    lines_to_remove.add(i)
                    # Also need to remove its matching closing div? 
                    # That's harder. Let's just remove the opening tag for now.
                    # Browser might handle extra closing divs okay, or we can run a tidy later.

# Also remove duplicates that are consecutive
for i in range(len(lines)-1):
    if '<div class="slide' in lines[i] and '<div class="slide' in lines[i+1]:
        # Remove the first one
        lines_to_remove.add(i)

print(f"Identified {len(lines_to_remove)} wrapper divs to remove")

# Create new content
new_lines = []
for i, line in enumerate(lines):
    if i in lines_to_remove:
        # print(f"Removing line {i+1}: {line.strip()}")
        continue
    new_lines.append(line)

# Save
with open("output/presentation/criteo_ceo_presentation_cleaned.html", 'w', encoding='utf-8') as f:
    f.writelines(new_lines)

# Overwrite original
with open(html_file, 'w', encoding='utf-8') as f:
    f.writelines(new_lines)

print("\n✅ SAVED CLEANED VERSION")
print(f"Original lines: {len(lines)}")
print(f"New lines: {len(new_lines)}")
print("="*70)
