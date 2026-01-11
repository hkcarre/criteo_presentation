#!/usr/bin/env python3
"""Compare current HTML vs .bak backup to find best version"""
import re

current_file = "output/presentation/criteo_ceo_presentation.html"
backup_file = "output/presentation/criteo_ceo_presentation.bak"

def analyze_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    return {
        'size': len(content),
        'slide_divs': len(re.findall(r'<div class="slide', content)),
        'has_title_slide': 'COMPETITIVE STRATEGY: DEFENDING MARKET' in content,
        'has_questions_slide': 'Questions?' in content,
        'appendix_a': content.count('APPENDIX A'),
        'appendix_b': content.count('APPENDIX B'),
        'appendix_c': content.count('APPENDIX C'),
        'appendix_d': content.count('APPENDIX D'),
        'appendix_e': content.count('APPENDIX E'),
        'slide_5_count': content.count('SLIDE 5'),
    }

print("="*70)
print("📊 FILE COMPARISON ANALYSIS")
print("="*70)

print("\n🔍 Current HTML:")
current = analyze_file(current_file)
for key, value in current.items():
    print(f"  {key}: {value}")

print("\n🔍 Backup (.bak):")
backup = analyze_file(backup_file)
for key, value in backup.items():
    print(f"  {key}: {value}")

print("\n" + "="*70)
print("📋 RECOMMENDATION")
print("="*70)

if current['has_title_slide'] and not backup['has_title_slide']:
    print("✅ CURRENT HTML is BETTER - has title slide")
    print("   Recommendation: Keep current file, do NOT restore from .bak")
elif backup['has_title_slide'] and not current['has_title_slide']:
    print("✅ BACKUP is BETTER - has title slide")
    print("   Recommendation: Restore from .bak")
else:
    if current['slide_divs'] > backup['slide_divs']:
        print("✅ CURRENT HTML likely better - more slides")
    else:
        print("⚠️ Files seem similar, manual inspection needed")
