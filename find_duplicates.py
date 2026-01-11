#!/usr/bin/env python3
"""Find consecutive duplicate slide divs"""
import re

html_file = "output/presentation/criteo_ceo_presentation.html"

with open(html_file, 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Find consecutive duplicates
duplicates = []
for i in range(len(lines) - 1):
    if '<div class="slide"' in lines[i] and '<div class="slide"' in lines[i+1]:
        duplicates.append((i+1, i+2))

print(f"Found {len(duplicates)} consecutive duplicate pairs:")
print()
for pair in duplicates[:15]:
    print(f"Lines {pair[0]}-{pair[1]}: Both have <div class='slide'>")
    print(f"  Line {pair[0]}: {lines[pair[0]-1].strip()[:70]}")
    print(f"  Line {pair[1]}: {lines[pair[1]-1].strip()[:70]}")
    print(f"  ACTION: Delete line {pair[1]}")
    print()
