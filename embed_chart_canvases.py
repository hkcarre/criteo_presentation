"""
Create simplified chart embeddings for presentation
Step 1: Add Chart.js library and create chart canvases
"""

# Read the current HTML
with open('output/presentation/criteo_ceo_presentation.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Add Chart.js library before </head>
chartjs_cdn = """    <!-- Chart.js Library -->
    <script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>
</head>"""

html = html.replace('</head>', chartjs_cdn)

# Now let's add chart canvases to the relevant slides

# Chart 1: Add to Slide 3 (Threat Evolution) - After SO WHAT box
chart_1_canvas = """
                <div style="background: white; padding: 30px; margin: 40px 0; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.1);">
                    <canvas id="threatEvolutionChart" style="max-height: 350px;"></canvas>
                </div>
"""

# Find where to insert - after the "Key Findings:" h3 on slide 3
html = html.replace(
    '<h3>Key Findings:</h3>',
    chart_1_canvas + '\n                <h3>Key Findings:</h3>',
    1  # Only first occurrence
)

# Chart 2: Add to Slide 4 (Competitor Launches) - After metrics
chart_2_canvas = """
                <div style="background: white; padding: 30px; margin: 40px 0; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.1);">
                    <canvas id="launchesChart" style="max-height: 350px;"></canvas>
                </div>
"""

html = html.replace(
    '<h3>Strategic Implications:</h3>',
    chart_2_canvas + '\n                <h3>Strategic Implications:</h3>',
    1
)

# Chart 3: Add to Slide 5 (Market Landscape) - Before table
chart_3_canvas = """
                <div style="background: white; padding: 30px; margin: 40px 0; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.1);">
                    <canvas id="marketHeatmapChart" style="max-height: 300px;"></canvas>
                </div>
"""

# Find the table on slide 5 and add chart before it
# We'll add after the SO WHAT box
html = html.replace(
    '<table style="margin-top: 40px;">',
    chart_3_canvas + '\n                <h3 style="margin-top: 40px;">Detailed Market Analysis:</h3>\n                <table style="margin-top: 20px;">',
    1
)

# Chart 4: Add to Slide 6 (High-Risk Clients) - After metrics
chart_4_canvas = """
                <div style="background: white; padding: 30px; margin: 40px 0; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.1);">
                    <canvas id="clientRiskChart" style="max-height: 350px;"></canvas>
                </div>
"""

# Add after the table on slide 6, before slide-number
# This one will go at the end before the slide divider, but let's place it after the SO WHAT box for slide 6
# Actually, let's add it before the table
marker_slide_6 = '<table style="margin-top: 40px;">'
# Count occurrences to find the second one (slide 6)
first_occurrence = html.find(marker_slide_6)
second_occurrence = html.find(marker_slide_6, first_occurrence + 1)

if second_occurrence != -1:
    # Insert before the second table
    html = html[:second_occurrence] + chart_4_canvas + '\n                <h3 style="margin-top: 20px;">Sample High-Risk Clients:</h3>\n                ' + html[second_occurrence:]

# Save updated HTML with chart canvases
with open('output/presentation/criteo_ceo_presentation.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("✅ Chart.js library added")
print("✅ 4 chart canvases embedded in presentation")
print("\nCanvases added:")
print("  • Slide 3: Threat Evolution Chart")
print("  • Slide 4: Competitor Launches Chart")
print("  • Slide 5: Market Heatmap Chart")
print("  • Slide 6: Client Risk Chart")
