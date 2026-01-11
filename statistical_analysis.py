import pandas as pd
import numpy as np

df = pd.read_csv('CASE_STUDY_RAW.csv', low_memory=False)
rev = pd.to_numeric(df['revenue_euro'], errors='coerce')
comp = pd.to_numeric(df['competitor_clicks'], errors='coerce')
df['month_dt'] = pd.to_datetime(df['month'])

print("=" * 60)
print("STATISTICAL ANALYSIS: MISSING DATA PATTERNS & GROWTH METRICS")
print("=" * 60)

# 1. TEMPORAL PATTERN: Records per month
print("\n=== 1. DATA VOLUME BY MONTH ===")
monthly_counts = df.groupby('month').size()
print(f"Min records/month: {monthly_counts.min():,}")
print(f"Max records/month: {monthly_counts.max():,}")
print(f"Avg records/month: {monthly_counts.mean():,.0f}")
print(f"Std records/month: {monthly_counts.std():,.0f}")
print("\nRecords per month:")
print(monthly_counts.to_string())

# 2. Zero revenue by month
print("\n=== 2. ZERO REVENUE % BY MONTH ===")
monthly_zero = df.groupby('month').apply(
    lambda x: (pd.to_numeric(x['revenue_euro'], errors='coerce') == 0).sum() / len(x) * 100
).round(1)
print(monthly_zero.to_string())

# 3. Check if early months have less data
print("\n=== 3. YEAR-OVER-YEAR COMPARISON ===")
df['year'] = df['month_dt'].dt.year
yearly_stats = df.groupby('year').agg({
    'client_id': 'nunique',
    'revenue_euro': lambda x: pd.to_numeric(x, errors='coerce').sum() / 1e6
}).round(2)
yearly_stats.columns = ['unique_clients', 'total_revenue_M']
print(yearly_stats)

# 4. Competitor activity by month
print("\n=== 4. COMPETITOR ACTIVITY OVER TIME ===")
monthly_comp = df.groupby('month').apply(
    lambda x: (pd.to_numeric(x['competitor_clicks'], errors='coerce') > 0).sum() / len(x) * 100
).round(2)
print(monthly_comp.to_string())

# 5. Check growth rate calculation
print("\n=== 5. GROWTH METRIC ANALYSIS ===")
# Calculate market share by month
monthly_agg = df.groupby('month').agg({
    'competitor_clicks': lambda x: pd.to_numeric(x, errors='coerce').sum(),
    'criteo_clicks': lambda x: pd.to_numeric(x, errors='coerce').sum()
})
monthly_agg['total_clicks'] = monthly_agg['competitor_clicks'] + monthly_agg['criteo_clicks']
monthly_agg['comp_share'] = monthly_agg['competitor_clicks'] / monthly_agg['total_clicks'] * 100

print("Competitor market share by month:")
print(monthly_agg['comp_share'].round(2).to_string())

# Calculate MoM vs YoY
monthly_agg['mom_change'] = monthly_agg['comp_share'].diff()
monthly_agg = monthly_agg.reset_index()
monthly_agg['month_dt'] = pd.to_datetime(monthly_agg['month'])
monthly_agg['month_num'] = monthly_agg['month_dt'].dt.month

# YoY calculation
print("\n=== 6. MoM vs YoY GROWTH COMPARISON ===")
print(f"Average MoM change in market share: {monthly_agg['mom_change'].mean():.3f}%")
print(f"Std Dev of MoM change: {monthly_agg['mom_change'].std():.3f}%")

# Calculate YoY for comparable months
yoy_data = []
for month_num in range(1, 13):
    month_data = monthly_agg[monthly_agg['month_num'] == month_num].sort_values('month_dt')
    if len(month_data) >= 2:
        for i in range(1, len(month_data)):
            yoy_change = month_data.iloc[i]['comp_share'] - month_data.iloc[i-1]['comp_share']
            yoy_data.append({'month': month_data.iloc[i]['month'], 'yoy_change': yoy_change})

if yoy_data:
    yoy_df = pd.DataFrame(yoy_data)
    print(f"Average YoY change: {yoy_df['yoy_change'].mean():.3f}%")
    print(f"Std Dev of YoY change: {yoy_df['yoy_change'].std():.3f}%")

# 7. Seasonality
print("\n=== 7. SEASONALITY CHECK ===")
df['quarter'] = df['month_dt'].dt.quarter
quarterly_comp = df.groupby('quarter').apply(
    lambda x: (pd.to_numeric(x['competitor_clicks'], errors='coerce') > 0).sum() / len(x) * 100
).round(2)
print("Competitor activity % by quarter:")
print(quarterly_comp)

print("\n=== 8. DATA SUFFICIENCY CHECK ===")
# How many clients have data in multiple months?
client_months = df.groupby('client_id')['month'].nunique()
print(f"Clients with 1-3 months data: {(client_months <= 3).sum():,} ({(client_months <= 3).sum()/len(client_months)*100:.1f}%)")
print(f"Clients with 4-12 months data: {((client_months > 3) & (client_months <= 12)).sum():,}")
print(f"Clients with 12+ months data: {(client_months > 12).sum():,} ({(client_months > 12).sum()/len(client_months)*100:.1f}%)")

print("\n=== ANALYSIS COMPLETE ===")
