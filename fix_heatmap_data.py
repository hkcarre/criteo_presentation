#!/usr/bin/env python3
"""
DATA FIX: Chart 3 (Market Risk)
Aligning with Speaker Script values (Millions €)
EE=9.2, IB=6.3 (60% of total). Others distributed.
"""

import re

html_file = "output/presentation/criteo_ceo_presentation_scroll.html"

print("="*70)
print("UPDATING CHART 3 DATA")
print("="*70)

with open(html_file, 'r', encoding='utf-8') as f:
    html = f.read()

# Define new data consistent with Speaker Script
# EE=9.2, IB=6.3. Total ~25M.
# Remaining ~10M distributed: France 3.5, Italy 2.8, UK 1.5, DACH 1.2, Nordics 0.8, Russia 0.4
labels = "['FASTERN EUROPE', 'IBERIA', 'FRANCE', 'ITALY', 'UK', 'DACH', 'NORDICS', 'RUSSIA']"
# Note: Speaker script highlights EE and IB as top.
data_values = "[9.2, 6.3, 3.5, 2.8, 1.5, 1.2, 0.8, 0.4]"
background_colors = "['#D32F2F', '#D32F2F', '#E64A19', '#E64A19', '#FF5722', '#FF8A65', '#FF8A65', '#FFCCBC']"

# Find Chart 3 section
# We look for "const ctx3 =" and replace the data block
start_marker = "const ctx3 = document.getElementById('marketHeatmapChart');"
if start_marker in html:
    # We will replace the whole Chart 3 config to be safe and clean
    # Construct new chart config
    new_chart_config = f"""const ctx3 = document.getElementById('marketHeatmapChart');
if (ctx3) {{
    new Chart(ctx3, {{
        type: 'bar',
        data: {{
            labels: {labels},
            datasets: [{{
                label: 'Revenue at Risk (€M)',
                data: {data_values},
                backgroundColor: {background_colors},
                borderColor: {background_colors},
                borderWidth: 1,
                barThickness: 30
            }}]
        }},
        options: {{
            indexAxis: 'y',
            responsive: true,
            maintainAspectRatio: true,
            plugins: {{
                title: {{
                    display: true,
                    text: 'Market Risk Heatmap (Revenue at Risk €M)',
                    font: {{ size: 16, weight: 'bold', family: 'Arial' }},
                    color: '#1A1A1A',
                    padding: 20
                }},
                legend: {{
                    display: false
                }},
                tooltip: {{
                    backgroundColor: 'rgba(26, 26, 26, 0.9)',
                    padding: 12,
                    callbacks: {{
                        label: function(context) {{
                            return 'Revenue at Risk: €' + context.parsed.x.toFixed(1) + 'M';
                        }}
                    }}
                }}
            }},
            scales: {{
                x: {{
                    beginAtZero: true,
                    title: {{
                        display: true,
                        text: 'Revenue at Risk (€ Millions)',
                        font: {{ size: 13, weight: '600' }},
                        color: '#666'
                    }},
                    ticks: {{
                        callback: function(value) {{
                            return '€' + value + 'M';
                        }},
                        font: {{ size: 12 }},
                        color: '#666'
                    }},
                    grid: {{
                        color: 'rgba(0, 0, 0, 0.05)'
                    }}
                }},
                y: {{
                    ticks: {{
                        font: {{ size: 12, weight: '600' }},
                        color: '#1A1A1A'
                    }},
                    grid: {{
                        display: false
                    }}
                }}
            }}
        }}
    }});
}}"""

    # Regex to find the existing block. 
    # It starts with const ctx3... and ends with the matching closing brace prior to "Chart 4" or just generic end.
    # Simpler: regex from `const ctx3` to `// Chart 4`
    
    pattern = re.compile(r"const ctx3 =.*?// Chart 4", re.DOTALL)
    match = pattern.search(html)
    
    if match:
        original_block = match.group(0)
        # We need to keep the "// Chart 4" at the end
        replacement = new_chart_config + "\n\n\n// Chart 4"
        html = html.replace(original_block, replacement)
        print("✅ Replaced Chart 3 config with correct Revenue Data")
    else:
        print("⚠️ Could not match regex for Chart 3 block. Trying simpler replacement.")
        # Fallback?
        
else:
    print("❌ Could not find Chart 3 marker")

with open(html_file, 'w', encoding='utf-8') as f:
    f.write(html)
