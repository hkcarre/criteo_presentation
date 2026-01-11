import pandas as pd
import numpy as np
from scipy import stats

print("="*80)
print("APPENDIX QA VALIDATION REPORT")
print("="*80)

# Load Data
df = pd.read_csv('CASE_STUDY_RAW.csv', low_memory=False)
df['month'] = pd.to_datetime(df['month'])
df['revenue_euro'] = pd.to_numeric(df['revenue_euro'], errors='coerce').fillna(0)
df['competitor_clicks'] = pd.to_numeric(df['competitor_clicks'], errors='coerce').fillna(0)
df['criteo_clicks'] = pd.to_numeric(df['criteo_clicks'], errors='coerce').fillna(0)
df['total_clicks'] = df['competitor_clicks'] + df['criteo_clicks']

# -------------------------------------------------------------------------
# APPENDIX A: DATA COVERAGE & DETECTION
# -------------------------------------------------------------------------
print("\n--- APPENDIX A: COVERAGE & DETECTION ---")
print(f"Total Records: {len(df)}")
print(f"Unique Clients: {df['client_id'].nunique()}")
print(f"Date Range: {df['month'].min().date()} to {df['month'].max().date()}")

# Detection Rate by Year
df['year'] = df['month'].dt.year
df['has_comp_data'] = df['competitor_clicks'] > 0

print("\nDetection Rate by Year:")
for year in [2022, 2023, 2024]:
    year_data = df[df['year'] == year]
    total_records = len(year_data)
    records_with_comp = year_data['has_comp_data'].sum()
    rate = (records_with_comp / total_records) * 100
    print(f"{year}: {records_with_comp} / {total_records} ({rate:.1f}%)")

# Data Quality Issues
zero_rev_count = (df['revenue_euro'] == 0).sum()
print(f"\nRevenue = 0 Records: {zero_rev_count} ({zero_rev_count/len(df)*100:.1f}%)")

no_comp_activity = (df['competitor_clicks'] == 0).sum()
print(f"No Competitor Activity: {no_comp_activity} ({no_comp_activity/len(df)*100:.1f}%)")

# -------------------------------------------------------------------------
# APPENDIX B: SEGMENT & MARKET DATA QUALITY
# -------------------------------------------------------------------------
print("\n--- APPENDIX B: SEGMENT & MARKET QUALITY ---")

# Segment Analysis
segments = ['Extra-Small', 'Small', 'Medium', 'Large']
print("\nSegment Quality (Inactive % & Avg Rev):")
for seg in segments:
    seg_data = df[df['segment'] == seg]
    if len(seg_data) > 0:
        inactive_pct = (seg_data['revenue_euro'] == 0).mean() * 100
        avg_rev = seg_data['revenue_euro'].mean()
        print(f"{seg}: Inactive {inactive_pct:.1f}%, Avg Rev €{avg_rev:.0f}")

# Market UTM Tracking (Detection Rate)
print("\nMarket Detection Rates:")
markets = ['EASTERN EUROPE', 'UK', 'DACH', 'NORDICS', 'IBERIA', 'FRANCE', 'RUSSIA']
for mkt in markets:
    mkt_data = df[df['market'] == mkt]
    detection_rate = (mkt_data['competitor_clicks'] > 0).mean() * 100
    print(f"{mkt}: {detection_rate:.1f}%")

# -------------------------------------------------------------------------
# APPENDIX C: STATISTICAL DEEP-DIVE
# -------------------------------------------------------------------------
print("\n--- APPENDIX C: STATISTICAL DEEP-DIVE ---")

# Monthly Aggregation for MoM/YoY
monthly_agg = df.groupby('month').agg({
    'competitor_clicks': 'sum',
    'total_clicks': 'sum',
    'revenue_euro': 'sum'
}).reset_index()
monthly_agg['comp_share'] = (monthly_agg['competitor_clicks'] / monthly_agg['total_clicks']) * 100

# MoM Analysis
monthly_agg['mom_change'] = monthly_agg['comp_share'].pct_change() * 100
monthly_agg['yoy_change'] = monthly_agg['comp_share'].pct_change(12) * 100

mom_avg = monthly_agg['mom_change'].mean()
mom_std = monthly_agg['mom_change'].std()
yoy_avg = monthly_agg['yoy_change'].mean()
yoy_std = monthly_agg['yoy_change'].std()

print(f"\nMoM Avg Change: {mom_avg:.2f}% (Std: {mom_std:.2f}%)")
print(f"YoY Avg Change: {yoy_avg:.2f}% (Std: {yoy_std:.2f}%)")
print(f"MoM Signal/Noise: {abs(mom_avg)/mom_std:.2f}")
print(f"YoY Signal/Noise: {abs(yoy_avg)/yoy_std:.2f}")

# Revenue Check
rev_2022 = monthly_agg[monthly_agg['month'].dt.year == 2022]['revenue_euro'].sum()
rev_2023 = monthly_agg[monthly_agg['month'].dt.year == 2023]['revenue_euro'].sum()
rev_2024_ytd = monthly_agg[monthly_agg['month'].dt.year == 2024]['revenue_euro'].sum()
# Annualize 2024 (10 months)
rev_2024_est = (rev_2024_ytd / 10) * 12

print(f"\n2022 Revenue: €{rev_2022/1e6:.1f}M")
print(f"2023 Revenue: €{rev_2023/1e6:.1f}M")
print(f"2024 Revenue (Est): €{rev_2024_est/1e6:.1f}M")

# Structural Break Check (Share %)
jan_23_share = monthly_agg[monthly_agg['month'] == '2023-01-01']['comp_share'].values[0]
apr_23_share = monthly_agg[monthly_agg['month'] == '2023-04-01']['comp_share'].values[0]
print(f"\nJan 2023 Share: {jan_23_share:.1f}%")
print(f"Apr 2023 Share: {apr_23_share:.1f}%")

# -------------------------------------------------------------------------
# APPENDIX D: CORRELATIONS
# -------------------------------------------------------------------------
print("\n--- APPENDIX D: CORRELATIONS ---")
# Correlation between Share % and Revenue
corr_pearson, p_pearson = stats.pearsonr(monthly_agg['comp_share'], monthly_agg['revenue_euro'])
corr_spearman, p_spearman = stats.spearmanr(monthly_agg['comp_share'], monthly_agg['revenue_euro'])

print(f"Pearson r: {corr_pearson:.2f} (p={p_pearson:.4f})")
print(f"Spearman rho: {corr_spearman:.2f}")

