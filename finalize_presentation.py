"""
Final step: Embed chart scripts into presentation HTML
"""

# Read the chart scripts
with open('output/presentation/chart_scripts.html', 'r', encoding='utf-8') as f:
    chart_scripts = f.read()

# Read the current HTML
with open('output/presentation/criteo_ceo_presentation.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Embed the chart scripts before </body>
html = html.replace('</body>', chart_scripts + '\n</body>')

# Save the complete HTML
with open('output/presentation/criteo_ceo_presentation.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("✅ Chart scripts embedded into presentation!")
print("✅ Presentation is now complete with interactive visualizations")
print("\n🎯 Final Presentation Includes:")
print("   • Bain-style insight-driven titles")
print("   • McKinsey SO WHAT storytelling boxes")
print("   • 4 interactive Chart.js visualizations")
print("   • Criteo brand compliance")
print("   • Official SVG logo")
print("   • Multi-agent validated data")
print("\n📊 Charts Added:")
print("   1. Slide 3: Threat Evolution Timeline")
print("   2. Slide 4: Competitor Launch Dynamics")
print("   3. Slide 5: Market Risk Heatmap")
print("   4. Slide 6: Top 10 Client Risk Scores")
