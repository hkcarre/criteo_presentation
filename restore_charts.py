#!/usr/bin/env python3
"""
RESTORE CHARTS SCRIPT
Injects the missing Chart.js initialization code into the scrolling presentation.
"""

presentation_file = "output/presentation/criteo_ceo_presentation_scroll.html"
chart_script_file = "output/presentation/chart_scripts.html"

print("="*70)
print("RESTORING CHARTS")
print("="*70)

# Read presentation
with open(presentation_file, 'r', encoding='utf-8') as f:
    presentation = f.read()

# Read chart scripts
with open(chart_script_file, 'r', encoding='utf-8') as f:
    chart_scripts = f.read()

# Verify Chart.js library is present
if "chart.umd.min.js" not in presentation and "chart.js" not in presentation:
    print("⚠️ Chart.js library missing! Injecting it...")
    presentation = presentation.replace('</head>', '<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>\n</head>')

# Append scripts before body end
if "</body>" in presentation:
    presentation = presentation.replace("</body>", f"\n{chart_scripts}\n</body>")
else:
    presentation += f"\n{chart_scripts}"

# Save
with open(presentation_file, 'w', encoding='utf-8') as f:
    f.write(presentation)

print(f"✅ Injected chart scripts from {chart_script_file}")
print("Charts should now render!")
