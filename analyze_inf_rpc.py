import pandas as pd
import json

# Load dataset
df = pd.read_csv('c:/Dev/entrevista/CASE_STUDY_CLEAN.csv')
    
# Column standardization
col_map = {c: c.lower() for c in df.columns}
if 'revenue_in_euros' in col_map:
     df.rename(columns={'revenue_in_euros': 'revenue'}, inplace=True)
elif 'revenue (in euros)' in col_map:
     df.rename(columns={'revenue (in euros)': 'revenue'}, inplace=True)
if 'revenue' not in df.columns:
     for c in df.columns:
         if 'revenue' in c and 'lost' not in c and 'click' not in c:
             df.rename(columns={c: 'revenue'}, inplace=True)
             break

# 1. Filter: Clicks == 0 and Revenue > 0
inf_cases = df[(df['criteo_clicks'] == 0) & (df['revenue'] > 0)]

count = len(inf_cases)
total_revenue_affected = inf_cases['revenue'].sum()
total_global_revenue = df['revenue'].sum()
revenue_share = (total_revenue_affected / total_global_revenue) * 100 if total_global_revenue > 0 else 0

# 2. Lag Check
df['month'] = pd.to_datetime(df['month'])
df = df.sort_values(['client_id', 'month'])
df['prev_clicks'] = df.groupby('client_id')['criteo_clicks'].shift(1)
inf_with_history = df.loc[inf_cases.index]
lag_evidence = inf_with_history[inf_with_history['prev_clicks'] > 0]
lag_count = len(lag_evidence)
lag_pct = (lag_count / count * 100) if count > 0 else 0

result = {
    "count": int(count),
    "revenue_affected": float(total_revenue_affected),
    "revenue_share_pct": float(revenue_share),
    "attribution_lag_pct": float(lag_pct),
    "conclusion": "MATERIAL" if revenue_share >= 1.0 else "NEGLIGIBLE"
}

print(json.dumps(result))
