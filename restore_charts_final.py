#!/usr/bin/env python3
"""
CHART RESTORATION SCRIPT
Properly injects chart canvas + Chart.js scripts into HTML
"""

import re

html_file = "output/presentation/criteo_ceo_presentation.html"
chart_scripts_file = "output/presentation/chart_scripts.html"

print("="*60)
print("📊 RESTORING CHARTS")
print("="*60)

# Read files
with open(html_file, 'r', encoding='utf-8') as f:
    html = f.read()

with open(chart_scripts_file, 'r', encoding='utf-8') as f:
    chart_scripts = f.read()

print(f"\n📄 HTML size: {len(html)} bytes")
print(f"📄 Chart scripts size: {len(chart_scripts)} bytes")

# ===== STEP 1: Remove duplicate "SLIDE X" text =====
print("\n🧹 Removing duplicate SLIDE X text...")
html = re.sub(r'(SLIDE \d+\s*){2,}', 'SLIDE \\1', html)
html = re.sub(r'(APPENDIX [A-Z]\s*){2,}', 'APPENDIX \\1', html)
print("  ✅ Cleaned duplicate markers")

# ===== STEP 2: Add chart canvas elements =====
print("\n📐 Adding chart canvas elements...")

canvas_definitions = {
    'SLIDE 3': ('threatEvolutionChart', 'Threat Evolution'),
    'SLIDE 4': ('launchesChart', 'Competitor Launches'),
    'SLIDE 5': ('marketHeatmapChart', 'Market Heatmap'),
    'SLIDE 6': ('clientRiskChart', 'Client Risk')
}

for slide_name, (canvas_id, label) in canvas_definitions.items():
    if f'id="{canvas_id}"' not in html:
        print(f"  Adding {label} canvas to {slide_name}...")
        
        # Find slide content section
        pattern = f'(<!-- {slide_name} -->.*?<div class="slide-content">)(.*?)(</div>\\s*</div>\\s*<!-- SLIDE)'
        
        def add_canvas(match):
            before = match.group(1)
            content = match.group(2)
            after = match.group(3)
            
            canvas_html = f'''
                <div style="margin: 20px auto; max-width: 90%; height: 400px;">
                    <canvas id="{canvas_id}"></canvas>
                </div>
'''
            return before + content + canvas_html + after
        
        html = re.sub(pattern, add_canvas, html, flags=re.DOTALL)
        print(f"    ✅ {label} canvas added")
    else:
        print(f"  ✅ {label} canvas already present")

# ===== STEP 3: Inject Chart.js scripts before </body> =====
print("\n🔧 Injecting Chart.js scripts...")

if 'new Chart(ctx1' in html:
    print("  ✅ Chart scripts already present")
else:
    # Find </body> tag
    marker = '</body>'
    pos = html.rfind(marker)
    
    if pos > 0:
        html = html[:pos] + '\n' + chart_scripts + '\n' + html[pos:]
        print("  ✅ Chart.js scripts injected before </body>")
    else:
        print("  ❌ Could not find </body> tag!")

# ===== STEP 4: Save =====
print("\n💾 Saving...")
with open(html_file, 'w', encoding='utf-8') as f:
    f.write(html)

print(f"✅ Saved: {len(html)} bytes")

print("\n" + "="*60)
print("✅ CHART RESTORATION COMPLETE!")
print("="*60)
print("\nRefresh your browser (Ctrl+F5) to see charts!")
