#!/usr/bin/env python3
"""
Comprehensive diagnostic analysis of presentation structure
Maps all slide divs, identifies duplicates, orphans, and nesting issues
"""

import re
from collections import defaultdict

html_file = "output/presentation/criteo_ceo_presentation.html"

print("="*80)
print("📊 COMPREHENSIVE PRESENTATION STRUCTURE ANALYSIS")
print("="*80)

with open(html_file, 'r', encoding='utf-8') as f:
    content = f.read()
    lines = content.split('\n')

print(f"\n📄 File size: {len(content):,} bytes")
print(f"📄 Total lines: {len(lines):,}")

# 1. Find all <div class="slide"> tags with their line numbers
print("\n" + "="*80)
print("1️⃣  SLIDE DIV ANALYSIS")
print("="*80)

slide_div_pattern = r'<div class="slide[^>]*>'
slide_divs = []
for i, line in enumerate(lines, 1):
    if re.search(slide_div_pattern, line):
        # Extract class names
        match = re.search(r'<div class="([^"]*)"', line)
        classes = match.group(1) if match else "unknown"
        slide_divs.append({'line': i, 'classes': classes})

print(f"Total <div class=\"slide\"> elements found: {len(slide_divs)}")
print(f"\nFirst 20 slide divs:")
for idx, div in enumerate(slide_divs[:20], 1):
    print(f"  {idx:2d}. Line {div['line']:4d}: <div class=\"{div['classes']}\">")

# 2. Find all text markers (SLIDE X, APPENDIX X, Questions?)
print("\n" + "="*80)
print("2️⃣  TEXT MARKER ANALYSIS")
print("="*80)

markers = []
marker_pattern = r'(?:SLIDE \d+|APPENDIX [A-E]|Questions\?)'
for i, line in enumerate(lines, 1):
    found = re.findall(marker_pattern, line)
    for marker in found:
        markers.append({'line': i, 'text': marker})

# Count occurrences
marker_counts = defaultdict(int)
for m in markers:
    marker_counts[m['text']] += 1

print(f"Total markers found: {len(markers)}")
print(f"\nMarker frequency:")
for marker, count in sorted(marker_counts.items()):
    status = "⚠️ DUPLICATE" if count > 1 else "✅"
    print(f"  {status} {marker}: {count} occurrence(s)")

print(f"\nAll marker locations:")
for idx, m in enumerate(markers, 1):
    print(f"  {idx:2d}. Line {m['line']:4d}: {m['text']}")

# 3. Find Appendix slides
print("\n" + "="*80)
print("3️⃣  APPENDIX SLIDE DETECTION")
print("="*80)

appendix_headers = []
appendix_pattern = r'<h[12][^>]*>\s*APPENDIX ([A-E])'
for i, line in enumerate(lines, 1):
    match = re.search(appendix_pattern, line)
    if match:
        letter = match.group(1)
        appendix_headers.append({'line': i, 'letter': letter, 'content': line.strip()[:100]})

print(f"Appendix headers found: {len(appendix_headers)}")
for app in appendix_headers:
    print(f"  Appendix {app['letter']} at line {app['line']}")

# 4. Check for orphan HTML (content between closing </div> and next <div class="slide">)
print("\n" + "="*80)
print("4️⃣  ORPHAN HTML DETECTION")
print("="*80)

orphan_sections = []
in_orphan = False
orphan_start = None
orphan_content = []

for i, line in enumerate(lines, 1):
    if '</div>' in line and not re.search(slide_div_pattern, line):
        in_orphan = True
        orphan_start = i
        orphan_content = [line.strip()]
    elif in_orphan:
        if re.search(slide_div_pattern, line):
            # Found next slide, record orphan
            if len(orphan_content) > 1:  # More than just the closing div
                orphan_sections.append({
                    'start': orphan_start,
                    'end': i - 1,
                    'lines': len(orphan_content),
                    'preview': ' '.join(orphan_content[:3])[:100]
                })
            in_orphan = False
            orphan_content = []
        else:
            orphan_content.append(line.strip())

print(f"Orphan HTML sections found: {len(orphan_sections)}")
for idx, orphan in enumerate(orphan_sections, 1):
    print(f"  {idx}. Lines {orphan['start']}-{orphan['end']} ({orphan['lines']} lines)")
    print(f"     Preview: {orphan['preview']}")

# 5. Expected slide structure
print("\n" + "="*80)
print("5️⃣  EXPECTED vs ACTUAL STRUCTURE")
print("="*80)

expected_slides = [
    "Slide 1: Title Slide",
    "Slide 2-11: Main Content",
    "Slide 12: Questions?",
    "Slide 13: Appendix A",
    "Slide 14: Appendix B",
    "Slide 15: Appendix C",
    "Slide 16: Appendix D",
    "Slide 17: Appendix E"
]

print("Expected structure (17 slides total):")
for slide in expected_slides:
    print(f"  {slide}")

print(f"\nActual numbers:")
print(f"  Total slide divs: {len(slide_divs)} (should be ~17)")
print(f"  Total markers: {len(markers)}")
print(f"  Appendix headers: {len(appendix_headers)} (should be 5)")

# 6. Recommendations
print("\n" + "="*80)
print("6️⃣  RECOMMENDED FIXES")
print("="*80)

fixes = []

# Check for duplicates
for marker, count in marker_counts.items():
    if count > 1:
        fixes.append(f"❌ Remove {count - 1} duplicate(s) of '{marker}'")

# Check orphans
if orphan_sections:
    fixes.append(f"❌ Remove {len(orphan_sections)} orphan HTML section(s)")

# Check slide count
if len(slide_divs) > 20:
    fixes.append(f"❌ Too many slide divs ({len(slide_divs)}), should be ~17")

# Check Appendix
if len(appendix_headers) < 5:
    fixes.append(f"❌ Missing Appendix slides: expected 5, found {len(appendix_headers)}")

if fixes:
    print("Issues to fix:")
    for fix in fixes:
        print(f"  {fix}")
else:
    print("✅ No major structural issues detected!")

print("\n" + "="*80)
print("✅ ANALYSIS COMPLETE")
print("="*80)
