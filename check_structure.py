#!/usr/bin/env python3
"""
Simplified diagnostic analysis - ASCII output only
"""

import re
from collections import defaultdict

html_file = "output/presentation/criteo_ceo_presentation.html"

print("="*70)
print("PRESENTATION STRUCTURE ANALYSIS")
print("="*70)

with open(html_file, 'r', encoding='utf-8') as f:
    content = f.read()
    lines = content.split('\n')

print(f"\nFile size: {len(content):,} bytes")
print(f"Total lines: {len(lines):,}")

# Find slide divs
slide_div_pattern = r'<div class="slide[^>]*>'
slide_divs = []
for i, line in enumerate(lines, 1):
    if re.search(slide_div_pattern, line):
        match = re.search(r'<div class="([^"]*)"', line)
        classes = match.group(1) if match else "unknown"
        slide_divs.append({'line': i, 'classes': classes})

print(f"\nTotal slide divs: {len(slide_divs)}")

# Find text markers
markers = []
marker_pattern = r'(?:SLIDE \d+|APPENDIX [A-E]|Questions\?)'
for i, line in enumerate(lines, 1):
    found = re.findall(marker_pattern, line)
    for marker in found:
        markers.append({'line': i, 'text': marker})

marker_counts = defaultdict(int)
for m in markers:
    marker_counts[m['text']] += 1

print(f"\nMarker frequency ({len(markers)} total):")
for marker in sorted(marker_counts.keys()):
    count = marker_counts[marker]
    status = "DUPLICATE!" if count > 1 else "OK"
    print(f"  {marker}: {count} x [{status}]")

# Appendix detection
appendix_pattern = r'<h[12][^>]*>\s*APPENDIX ([A-E])'
appendix_count = 0
for i, line in enumerate(lines, 1):
    if re.search(appendix_pattern, line):
        appendix_count += 1

print(f"\nAppendix headers found: {appendix_count} (expected: 5)")

# Summary
print("\n" + "="*70)
print("SUMMARY")
print("="*70)
print(f"Slide divs: {len(slide_divs)} (expected: ~17)")
print(f"Markers: {len(markers)}")
print(f"Appendix headers: {appendix_count} (expected: 5)")

# Issues
print("\nISSUES TO FIX:")
issues = []
for marker, count in marker_counts.items():
    if count > 1:
        issues.append(f"  - Remove {count - 1} duplicate(s) of '{marker}'")

if len(slide_divs) > 20:
    issues.append(f"  - Too many slide divs ({len(slide_divs)})")

if appendix_count < 5:
    issues.append(f"  - Missing Appendix slides (found {appendix_count}/5)")

if issues:
    for issue in issues:
        print(issue)
else:
    print("  No major issues detected!")

print("\n" + "="*70)
