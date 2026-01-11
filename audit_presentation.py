"""
Comprehensive Audit of Criteo CEO Presentation
No external dependencies required
"""
import re
import os

# Read the HTML file
with open('output/presentation/criteo_ceo_presentation.html', 'r', encoding='utf-8') as f:
    content = f.read()

print("=" * 80)
print("COMPREHENSIVE PRESENTATION AUDIT")
print("=" * 80)

# 1. Check for Lifeboat Navigation Script
print("\n1. NAVIGATION SCRIPT VERIFICATION")
if "EMERGENCY LIFEBOAT SCRIPT ACTIVATED" in content:
    print("   ✅ Lifeboat navigation script is PRESENT")
    if "document.addEventListener('keydown'" in content:
        print("   ✅ Keyboard event listener is PRESENT")
        print("   ✅ Arrow key navigation is configured")
    else:
        print("   ❌ Keyboard event listener is MISSING")
else:
    print("   ❌ Lifeboat navigation script is MISSING")

# 2. Count all slide div elements
slide_divs = content.count('<div class="slide')
slide_content_divs = content.count('<div class="slide-content"')
print(f"\n2. SLIDE STRUCTURE COUNT")
print(f"   Slide containers: {slide_divs}")
print(f"   Slide content divs: {slide_content_divs}")

# 3. List all slide markers (HTML comments)
print("\n3. SLIDE MARKER AUDIT (HTML Comments)")
slide_markers = re.findall(r'<!-- (Slide \d+|Appendix [A-Z]): ([^-]+) -->', content)
print(f"   Total slide markers: {len(slide_markers)}")
for i, (marker, title) in enumerate(slide_markers, 1):
    print(f"   {i:2d}. {marker}: {title.strip()}")

# 4. Check for Chart.js library
print("\n4. CHART.JS LIBRARY")
if "chart.js" in content.lower():
    print("   ✅ Chart.js library CDN is included")
else:
    print("   ❌ Chart.js library is MISSING")

# 5. Count canvas elements (for charts)
canvas_count = content.count('<canvas')
print(f"\n5. CHART CANVASES")
print(f"   Total canvas elements: {canvas_count}")
canvas_ids = re.findall(r'<canvas[^>]*id="([^"]+)"', content)
for i, canvas_id in enumerate(canvas_ids, 1):
    print(f"   {i}. Canvas ID: {canvas_id}")

# 6. Check for Chart data and configuration
print("\n6. CHART DATA & CONFIGURATION VERIFICATION")
chart_items = [
    ('new Chart', 'Chart.js initialization'),
    ('Chart.register', 'Chart.js plugins'),
    ('coverageChart', 'Coverage chart configuration'),
    ('penetrationChart', 'Penetration chart configuration'),
    ('labels:', 'Chart labels data'),
    ('datasets:', 'Chart datasets'),
]
for keyword, description in chart_items:
    count = content.count(keyword)
    if count > 0:
        print(f"   ✅ {description}: {count} occurrence(s)")
    else:
        print(f"   ❌ {description} MISSING")

# 7. Check for slide numbers
print("\n7. SLIDE NUMBER ELEMENTS")
slide_number_count = content.count('<div class="slide-number"')
print(f"   Total slide-number divs: {slide_number_count}")

# 8. Check orphan "SLIDE 1" text (the bug we fixed)
print("\n8. ORPHAN TEXT CHECK (Critical Bug)")
# Look for standalone SLIDE text not in proper div
lines = content.split('\n')
orphan_lines = [i+1 for i, line in enumerate(lines) if line.strip() == 'SLIDE 1' and '<div' not in line]
if orphan_lines:
    print(f"   ❌ WARNING: Found orphan 'SLIDE 1' at lines: {orphan_lines}")
else:
    print("   ✅ No orphan 'SLIDE 1' text nodes found")

# 9. File statistics
file_size = os.path.getsize('output/presentation/criteo_ceo_presentation.html')
line_count = len(lines)
print(f"\n9. FILE STATISTICS")
print(f"   Size: {file_size:,} bytes ({file_size/1024:.1f} KB)")
print(f"   Lines: {line_count:,}")

# 10. Critical CSS verification
print("\n10. CRITICAL CSS CLASSES")
css_classes = [
    ('class="slide"', 'Slide container'),
    ('class="slide-content"', 'Slide content'),
    ('class="slide-number"', 'Slide number'),
    ('class="presentation"', 'Presentation wrapper'),
    ('class="criteo-logo"', 'Criteo logo'),
    ('class="insight-box"', 'Insight boxes'),
]
for css_selector, description in css_classes:
    count = content.count(css_selector)
    status = "✅" if count > 0 else "❌"
    print(f"   {status} {description}: {count}")

# 11. Check for specific visualizations by slide
print("\n11. SLIDE-SPECIFIC CONTENT CHECK")
specific_content = [
    ('COMPETITIVE STRATEGY: DEFENDING MARKET', 'Title Slide'),
    ('We Face Accelerating Competitive Pressure', 'Slide 2: Executive Summary'),
    ('Granular Vertical Analysis', 'Slide 3'),
    ('Strong Brands Insulate Criteo', 'Slide 5'),
    ('Strategic Summary', 'Slide 11'),
    ('APPENDIX A', 'Appendix A'),
    ('APPENDIX B', 'Appendix B'),
    ('APPENDIX E', 'Appendix E'),
]
for text, label in specific_content:
    if text in content:
        print(f"   ✅ {label}")
    else:
        print(f"   ❌ {label} MISSING")

# 12. Browser cache warning
print("\n" + "=" * 80)
print("12. TROUBLESHOOTING RECOMMENDATION")
print("=" * 80)
print("\n   If navigation is NOT working in your browser:")
print("   1. Close ALL browser tabs showing this presentation")
print("   2. Press Ctrl+Shift+Delete (Windows) or Cmd+Shift+Delete (Mac)")
print("   3. Clear 'Cached images and files'")
print("   4. Re-open: file:///C:/Dev/entrevista/output/presentation/criteo_ceo_presentation.html")
print("   5. Try pressing ArrowRight to navigate")
print("\n   OR use a hard refresh: Ctrl+F5 (Windows) or Cmd+Shift+R (Mac)")

print("\n" + "=" * 80)
print("AUDIT COMPLETE")
print("=" * 80)
