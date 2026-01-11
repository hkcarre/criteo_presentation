#!/usr/bin/env python3
"""Detailed slide analysis of restored presentation"""
import re

html_file = "output/presentation/criteo_ceo_presentation.html"

with open(html_file, 'r', encoding='utf-8') as f:
    content = f.read()

# Find all slide divs
slide_divs = re.findall(r'<div class="slide[^>]*>', content)
print(f"Total <div class=\"slide\"> elements: {len(slide_divs)}")

# Find markers
markers = re.findall(r'(?:SLIDE \d+|APPENDIX [A-E]|Questions\?)', content)
print(f"\nFound {len(markers)} text markers:")
for i, m in enumerate(markers, 1):
    print(f"  {i}. {m}")

# Check for specific key slides
key_slides = [
    "Competitive Defense Strategy",
    "Questions?",
    "APPENDIX A",
    "APPENDIX B", 
    "APPENDIX C",
    "APPENDIX D",
    "APPENDIX E"
]

print("\n🔍 Key Slide Verification:")
for slide_title in key_slides:
    exists = slide_title in content
    print(f"  {'✅' if exists else '❌'} {slide_title}")

# Check for duplicate content
print("\n⚠️ Duplicates Check:")
slide_5_count = content.count("SLIDE 5")
print(f"  'SLIDE 5' appears: {slide_5_count} times")
