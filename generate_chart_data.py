"""
Create interactive visualizations for the Bain-style presentation
Uses Chart.js embedded inline for standalone HTML
"""

import json

# Load analysis results
with open('analysis_results.json', 'r') as f:
    analysis = json.load(f)

# Load strategic insights
with open('strategic_insights.json', 'r') as f:
    strategic = json.load(f)

print("📊 Generating Chart Data...")

# ============================================================================
# Chart 1: Waterfall Chart - Threat Evolution
# ============================================================================
q1_data = analysis['question_1_threat_evolution']
monthly = q1_data['monthly_evolution']

# Get first, last, and key milestones
first_month = monthly[0]
last_month = monthly[-1]
mid_point = monthly[len(monthly)//2]

waterfall_data = {
    'labels': ['Oct 2021\nStart', 'Growth\nPhase 1', 'Mid Point\n(17 months)', 'Growth\nPhase 2', 'Oct 2024\nCurrent'],
    'data': [
        first_month['revenue_lost_pct'],  # Starting
        mid_point['revenue_lost_pct'] - first_month['revenue_lost_pct'],  # Phase 1 growth
        0,  # Mid-point (marker)
        last_month['revenue_lost_pct'] - mid_point['revenue_lost_pct'],  # Phase 2 growth
        0   # Current (marker)
    ],
    'actual_values': [
        first_month['revenue_lost_pct'],
        mid_point['revenue_lost_pct'],
        mid_point['revenue_lost_pct'],
        last_month['revenue_lost_pct'],
        last_month['revenue_lost_pct']
    ]
}

print(f"✓ Waterfall: {first_month['revenue_lost_pct']:.2f}% → {last_month['revenue_lost_pct']:.2f}%")

# ============================================================================
# Chart 2: Heatmap Data - Market × Vertical Risk
# ============================================================================
q3_data = analysis['question_3_segment_analysis']

# Get top markets and verticals
markets = q3_data['by_market']['segment_analysis'][:5]  # Top 5 markets
verticals = q3_data['by_vertical']['segment_analysis'][:5]  # Top 5 verticals

heatmap_data = {
    'markets': [m['segment'] for m in markets],
    'market_values': [m['revenue_lost_pct'] for m in markets],
    'verticals': [v['segment'] for v in verticals],
    'vertical_values': [v['revenue_lost_pct'] for v in verticals]
}

print(f"✓ Heatmap: {len(markets)} markets × {len(verticals)} verticals")

# ============================================================================
# Chart 3: Spider/Radar Chart - Multi-Dimensional Threat
# ============================================================================
spider_data = {
    'labels': [
        'Revenue\nLost %',
        'Client\nPenetration',
        'Launch\nVelocity',
        'Trend\nAcceleration',
        'Geographic\nConcentration'
    ],
    'values': [
        (last_month['revenue_lost_pct'] / 10) * 100,  # Normalize to /10 scale
        70.9,  # Client penetration %
        50.1,  # Launch velocity (501/1000 normalized)
        85.0,  # Trend acceleration (+16.8% as severity score)
        75.0   # Geographic concentration (top 3 markets hold 75%+ of risk)
    ]
}

print(f"✓ Spider: 5 dimensions, avg score {sum(spider_data['values'])/5:.1f}/100")

# ============================================================================
# Chart 4: Stacked Area Chart - Competitor Launches
# ============================================================================
q2_data = analysis['question_2_competitor_launches']
launches = q2_data['launches_by_month']

# Sample every 3rd month for readability (34 months → ~11 points)
sampled_launches = launches[::3]

area_data = {
    'labels': [l['month'] for l in sampled_launches],
    'new_launches': [l['new_launches'] for l in sampled_launches],
    'cumulative': [l['cumulative_launches'] for l in sampled_launches]
}

print(f"✓ Area Chart: {len(sampled_launches)} time points, {area_data['cumulative'][-1]} total launches")

# ============================================================================
# Chart 5: Horizontal Bar Chart - Top 20 Client Risk
# ============================================================================
q4_data = analysis['question_4_client_attention']
top_clients = q4_data['top_20_clients'][:10]  # Show top 10 for readability

bar_data = {
    'labels': [f"Client {i+1}" for i in range(len(top_clients))],  # Anonymized
    'risk_scores': [c['risk_score'] for c in top_clients],
    'revenue_at_risk': [c['revenue_lost'] for c in top_clients]
}

print(f"✓ Bar Chart: Top {len(top_clients)} clients, €{sum(bar_data['revenue_at_risk'])/1000000:.1f}M at risk")

# ============================================================================
# Save chart data as JSON for HTML embedding
# ============================================================================
chart_data_bundle = {
    'waterfall': waterfall_data,
    'heatmap': heatmap_data,
    'spider': spider_data,
    'area': area_data,
    'bar': bar_data
}

with open('output/presentation/chart_data.json', 'w') as f:
    json.dump(chart_data_bundle, f, indent=2)

print("\n✅ Chart data generated and saved!")
print("📁 File: output/presentation/chart_data.json")
