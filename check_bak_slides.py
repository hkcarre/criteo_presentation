#!/usr/bin/env python3
"""Check slide count in the .bak file"""
import re

bak_file = "output/presentation/criteo_ceo_presentation.bak"

with open(bak_file, 'r', encoding='utf-8') as f:
    content = f.read()

# Find slide markers
markers = re.findall(r'(?:SLIDE \d+|APPENDIX [A-E])', content)

print(f"File size: {len(content)} bytes")
print(f"Found {len(markers)} markers:")
for m in markers:
    print(m)
