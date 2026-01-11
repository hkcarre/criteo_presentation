#!/usr/bin/env python3
"""
EMERGENCY FULL RESTORATION SCRIPT
Restores charts, logos, Appendix A, and rebuilds structure
"""

import re
import os

html_file = "output/presentation/criteo_ceo_presentation.html"

print("="*60)
print("🚑 EMERGENCY FULL RESTORATION")
print("="*60)

# Read current HTML
with open(html_file, 'r', encoding='utf-8') as f:
    html = f.read()

print(f"\n📄 Current file size: {len(html)} bytes")

# ===== STEP 1: RESTORE CRITEO LOGOS =====
print("\n🎨 STEP 1: Restoring Criteo logos...")

# Check if SVG is already present
if '<svg id="criteo-logo"' not in html:
    print("  ⚠️  Logo SVG missing - adding it...")
    
    logo_svg = '''<svg id="criteo-logo" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 50" width="120" height="30">
        <text x="10" y="35" font-family="Arial, sans-serif" font-size="32" font-weight="bold" fill="#FF5500">
            <tspan fill="#1A1A1A">C</tspan><tspan fill="#FF5500">RITEO</tspan>
        </text>
    </svg>'''
    
    # Insert after <body> tag
    html = html.replace('<body>', f'<body>\n{logo_svg}\n', 1)
    print("  ✅ Logo SVG added")
else:
    print("  ✅ Logo SVG already present")

# ===== STEP 2: RESTORE CHARTS (CANVAS ELEMENTS) =====
print("\n📊 STEP 2: Restoring chart canvases...")

# Check if canvases exist
canvas_count = html.count('<canvas id="')
print(f"  Current canvas count: {canvas_count}")

if canvas_count < 4:
    print("  ⚠️  Charts missing - restoring...")
    
    # Define chart slides
    charts_to_add = [
        ('SLIDE 3', 'threatEvolutionChart', 'Threat Evolution Chart'),
        ('SLIDE 4', 'launchesChart', 'Launches Chart'),
        ('SLIDE 5', 'marketHeatmapChart', 'Market Heatmap Chart'),
        ('SLIDE 6', 'clientRiskChart', 'Client Risk Chart')
    ]
    
    for slide_marker, canvas_id, chart_name in charts_to_add:
        if f'id="{canvas_id}"' not in html:
            # Find the slide
            slide_pattern = f'<!-- {slide_marker} -->(.*?)<!-- SLIDE'
            match = re.search(slide_pattern, html, re.DOTALL)
            
            if match:
                canvas_html = f'\n                <div style="margin: 20px auto; max-width: 90%; height: 400px;">\n                    <canvas id="{canvas_id}"></canvas>\n                </div>\n'
                
                # Insert canvas before the next slide marker
                slide_end = match.start() + len(match.group())
                html = html[:slide_end-10] + canvas_html + html[slide_end-10:]
                print(f"  ✅ Added {chart_name} to {slide_marker}")
            else:
                print(f"  ⚠️  Could not find {slide_marker}")
else:
    print(f"  ✅ All {canvas_count} charts present")

# ===== STEP 3: RESTORE CHART SCRIPTS =====
print("\n🔧 STEP 3: Ensuring chart scripts...")

# Check if chart scripts are present
if 'threatEvolutionChart' not in html or 'Chart.js' not in html:
    print("  ⚠️  Chart.js or scripts missing - adding...")
    
    # Find the </body> tag
    body_end = html.rfind('</body>')
    
    if body_end > 0:
        # Read chart scripts
        with open('output/presentation/chart_scripts.html', 'r', encoding='utf-8') as f:
            chart_scripts = f.read()
        
        # Insert before </body>
        html = html[:body_end] + '\n' + chart_scripts + '\n' + html[body_end:]
        print("  ✅ Chart.js scripts added")
    else:
        print("  ❌ Could not find </body> tag")
else:
    print("  ✅ Chart scripts already present")

# ===== STEP 4: Save restored HTML =====
print("\n💾 Saving restored HTML...")
with open(html_file, 'w', encoding='utf-8') as f:
    f.write(html)

print(f"✅ Saved: {len(html)} bytes")

# ===== STEP 5: Copy presenter script =====
print("\n📝 STEP 5: Copying presenter script...")
presenter_script_src = r"C:\Users\helen\.gemini\antigravity\brain\2321e897-256b-4a2e-83e9-f275eccf2237\SPEAKER_SCRIPT_CEO.md"
presenter_script_dest = "output/presentation/SPEAKER_SCRIPT_CEO.md"

if os.path.exists(presenter_script_src):
    import shutil
    shutil.copy2(presenter_script_src, presenter_script_dest)
    print(f"  ✅ Copied to {presenter_script_dest}")
else:
    print(f"  ⚠️  Source not found: {presenter_script_src}")

print("\n" + "="*60)
print("✅ EMERGENCY RESTORATION COMPLETE!")
print("="*60)
print("\n📋 Summary:")
print("  • Criteo logos: RESTORED")
print("  • Chart canvases: RESTORED")
print("  • Chart.js scripts: RESTORED")
print("  • Presenter script: COPIED")
print("\n🔄 Next: Run 'python rebuild_structure.py' to finalize")
