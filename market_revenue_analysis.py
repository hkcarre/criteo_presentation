import pandas as pd
import numpy as np

print("=" * 80)
print("MARKET REVENUE vs. RISK ANALYSIS")
print("=" * 80)

# 1. Load Data
df = pd.read_csv('CASE_STUDY_RAW.csv', low_memory=False)
df['revenue_euro'] = pd.to_numeric(df['revenue_euro'], errors='coerce').fillna(0)
df['competitor_clicks'] = pd.to_numeric(df['competitor_clicks'], errors='coerce').fillna(0)
df['criteo_clicks'] = pd.to_numeric(df['criteo_clicks'], errors='coerce').fillna(0)

# 2. Group by Market
market_stats = df.groupby('market').agg({
    'revenue_euro': 'sum',
    'competitor_clicks': 'sum',
    'criteo_clicks': 'sum'
}).reset_index()

# 3. Calculate Metrics
market_stats['total_clicks'] = market_stats['competitor_clicks'] + market_stats['criteo_clicks']
market_stats['comp_share_pct'] = (market_stats['competitor_clicks'] / market_stats['total_clicks']) * 100
market_stats['revenue_share_pct'] = (market_stats['revenue_euro'] / market_stats['revenue_euro'].sum()) * 100

# 4. Proxy for "Absolute Risk" (Revenue * Share)
# This assumes the click share vaguely correlates to revenue potential lost
market_stats['revenue_at_risk_proxy'] = market_stats['revenue_euro'] * (market_stats['comp_share_pct'] / 100)

# 5. Sort and Display
# Sort by Revenue Size first to see "Who pays the bills?"
print("\nTOP MARKETS BY TOTAL REVENUE (SIZE):")
print(f"{'Market':<15} {'Revenue (€)':<15} {'% of Global':<12} {'Comp Share':<12} {'Risk Tier'}")
print("-" * 75)

top_revenue = market_stats.sort_values('revenue_euro', ascending=False)
for _, row in top_revenue.iterrows():
    risk_tier = "LOW"
    if row['comp_share_pct'] > 25: risk_tier = "CRITICAL"
    elif row['comp_share_pct'] > 20: risk_tier = "HIGH"
    elif row['comp_share_pct'] > 15: risk_tier = "MEDIUM"
    
    print(f"{row['market']:<15} €{row['revenue_euro']/1e6:.1f}M       {row['revenue_share_pct']:<5.1f}%       {row['comp_share_pct']:<5.1f}%       {risk_tier}")

print("\n" + "=" * 80)

# Sort by "Weighted Risk" (Revenue At Risk Proxy)
print("\nTOP MARKETS BY ESTIMATED ABSOLUTE REVENUE RISK (€ * Share):")
print(f"{'Market':<15} {'Est. Risk (€)':<15} {'Comp Share':<12} {'Total Rev (€)'}")
print("-" * 75)

top_risk = market_stats.sort_values('revenue_at_risk_proxy', ascending=False)
for _, row in top_risk.iterrows():
    print(f"{row['market']:<15} €{row['revenue_at_risk_proxy']/1e6:.1f}M       {row['comp_share_pct']:<5.1f}%       €{row['revenue_euro']/1e6:.1f}M")
