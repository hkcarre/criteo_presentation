"""
Recalculate Analysis with Competitor Market Share % Metric
Chief Data Science Officer Approved Adjustment
"""

import json
import pandas as pd
import numpy as np

print("🔄 METRIC RECALCULATION - COMPETITOR MARKET SHARE %")
print("="*80)

# Load cleaned data
df = pd.read_csv('CASE_STUDY_CLEAN.csv')

# ============================================================================
# Q1: Recalculate with Market Share Metric
# ============================================================================
print("\n📊 Q1: Threat Evolution - NEW METRIC")
print("-"*80)

# Group by month
monthly = df.groupby('month').agg({
    'revenue_euro': 'sum',
    'competitor_clicks': 'sum',
    'criteo_clicks': 'sum',
    'client_id': 'nunique'
}).reset_index()

# Calculate Competitor Market Share %
monthly['competitor_market_share'] = (
    monthly['competitor_clicks'] / 
    (monthly['competitor_clicks'] + monthly['criteo_clicks'])
) * 100

# Calculate trend (3-month moving average)
monthly['trend_ma3'] = monthly['competitor_market_share'].rolling(window=3, min_periods=1).mean()

# Key statistics
first_month = monthly.iloc[0]
last_month = monthly.iloc[-1]
avg_share = monthly['competitor_market_share'].mean()

print(f"\n✅ NEW METRIC: Competitor Market Share %")
print(f"  • First Month ({first_month['month'][:10]}): {first_month['competitor_market_share']:.2f}%")
print(f"  • Last Month ({last_month['month'][:10]}): {last_month['competitor_market_share']:.2f}%")
print(f"  • Average: {avg_share:.2f}%")
print(f"  • Total Change: +{last_month['competitor_market_share'] - first_month['competitor_market_share']:.2f}pp")

# Calculate monthly growth rate
months_count = len(monthly)
total_change = last_month['competitor_market_share'] - first_month['competitor_market_share']
monthly_growth = total_change / months_count

print(f"  • Monthly Growth Rate: +{monthly_growth:.3f}%")
print(f"  • Peak: {monthly['competitor_market_share'].max():.2f}%")

# ============================================================================
# Update Analysis Results
# ============================================================================
print("\n🔄 Updating analysis_results.json...")

# Load existing results
with open('analysis_results.json', 'r') as f:
    analysis = json.load(f)

# Update Q1 with new metric
analysis['q1']['monthly_data'] = []
for _, row in monthly.iterrows():
    analysis['q1']['monthly_data'].append({
        'month': row['month'],
        'revenue_euro': float(row['revenue_euro']),
        'competitor_clicks': int(row['competitor_clicks']),
        'criteo_clicks': int(row['criteo_clicks']),
        'client_id': int(row['client_id']),
        'competitor_market_share': float(row['competitor_market_share']),
        'trend_ma3': float(row['trend_ma3']) if not pd.isna(row['trend_ma3']) else None
    })

# Update key findings
analysis['q1']['metrics_comparison'] = {
    'Competitor Market Share (%)': {
        'first_month': float(first_month['competitor_market_share']),
        'last_month': float(last_month['competitor_market_share']),
        'change': float(total_change),
        'avg': float(avg_share),
        'peak': float(monthly['competitor_market_share'].max()),
        'pros': [
            'Always between 0-100%',
            'Directly shows competitive pressure',
            'Easy for executives to understand',
            'Comparable across time periods'
        ]
    }
}

analysis['q1']['key_findings'] = {
    'monthly_growth_rate': float(monthly_growth),
    'total_increase_pp': float(total_change),
    'peak_threat_pct': float(monthly['competitor_market_share'].max()),
    'current_threat_pct': float(last_month['competitor_market_share'])
}

analysis['q1']['recommended_metric'] = 'Competitor Market Share (%)'

# Save updated analysis
with open('analysis_results.json', 'w') as f:
    json.dump(analysis, f, indent=2)

print("✅ analysis_results.json updated with new metric")

# ============================================================================
# Generate Updated Chart Data
# ============================================================================
print("\n📊 Generating updated chart data...")

# Sample every 3 months for chart
sampled = monthly.iloc[::3]

chart1_labels = [m[:7] for m in sampled['month'].tolist()]
chart1_values = sampled['competitor_market_share'].tolist()

chart_data = {
    'labels': chart1_labels,
    'values': chart1_values,
    'first_value': float(first_month['competitor_market_share']),
    'last_value': float(last_month['competitor_market_share']),
    'peak_value': float(monthly['competitor_market_share'].max()),
    'growth_rate': float(monthly_growth)
}

with open('output/presentation/updated_chart_data.json', 'w') as f:
    json.dump(chart_data, f, indent=2)

print("✅ Chart data generated: output/presentation/updated_chart_data.json")

# ============================================================================
# Summary
# ============================================================================
print("\n" + "="*80)
print("✅ RECALCULATION COMPLETE")
print("="*80)

print(f"\n📈 NEW KEY METRICS:")
print(f"   Current Threat: {last_month['competitor_market_share']:.2f}% (was N/A with old metric)")
print(f"   Monthly Growth: +{monthly_growth:.3f}% (was +1.77%)")
print(f"   Total Change: +{total_change:.2f}pp (from {first_month['competitor_market_share']:.2f}% to {last_month['competitor_market_share']:.2f}%)")
print(f"   Peak Threat: {monthly['competitor_market_share'].max():.2f}%")

print(f"\n🎯 NARRATIVE UPDATES NEEDED:")
print(f"   • Slide 3: 'Competitors Now Capture {last_month['competitor_market_share']:.1f}% of Market Clicks'")
print(f"   • SO WHAT: 'Up from {first_month['competitor_market_share']:.1f}% in 34 months'")
print(f"   • Chart Title: 'Competitor Market Share Growth ({first_month['competitor_market_share']:.1f}% → {last_month['competitor_market_share']:.1f}%)'")

print("\n🎨 Next: Update presentation HTML with new metric")
