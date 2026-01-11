import pandas as pd
import numpy as np

# Robust Load
try:
    df = pd.read_csv('c:/Dev/entrevista/CASE_STUDY_CLEAN.csv', sep= None, engine='python')
except:
    df = pd.read_csv('c:/Dev/entrevista/CASE_STUDY_CLEAN.csv', sep=',')

# Clean formatting
df.columns = [c.strip().lower().replace(' ', '_').replace('"', '') for c in df.columns]

# Helper to clean currency
def clean_num(x):
    if isinstance(x, str):
        return float(x.replace('€', '').replace(',', '').strip())
    return float(x) if x is not None else 0.0

# Map cols based on index if naming fails
# We saw earlier: 0:,month,client_id ... 7:estimated_revenue_lost_clicks 8:revenue_pe
# It seems "estimated_revenue_lost_clicks" is a merged header of "estimated_revenue_lost" and "clicks"?
# OR "clicks" is missing.
# Let's try to identify columns by content type in the first row of data?
# No, let's stick to the names we found.

# Identify Clicks
if 'criteo_clicks' not in df.columns:
    # Try finding any column with 'click'
    cols = [c for c in df.columns if 'click' in c and 'competitor' not in c and 'revenue' not in c]
    if cols:
        df.rename(columns={cols[0]: 'criteo_clicks'}, inplace=True)
    else:
        # Check for the weird merged header
        merged = [c for c in df.columns if 'clicks' in c and 'revenue' in c]
        print(f"DEBUG: Suspicious merged headers? {merged}")

# Identify Revenue
if 'revenue' not in df.columns:
     if 'revenue_in_euros' in df.columns: df.rename(columns={'revenue_in_euros': 'revenue'}, inplace=True)

# Force numeric
if 'revenue' in df.columns:
    df['revenue'] = df['revenue'].apply(clean_num)
if 'criteo_clicks' in df.columns:
    df['criteo_clicks'] = pd.to_numeric(df['criteo_clicks'], errors='coerce').fillna(0)

print("\n--- STATS ---")
if 'criteo_clicks' in df.columns and 'revenue' in df.columns:
    print(df[['criteo_clicks', 'revenue']].describe())
    
    print("\n--- LOWEST CLICKS WITH POSITIVE REVENUE ---")
    suspicious = df[df['revenue'] > 0].sort_values('criteo_clicks', ascending=True).head(10)
    print(suspicious[['client_id', 'criteo_clicks', 'revenue', 'segment'] if 'segment' in df.columns else ['client_id', 'criteo_clicks', 'revenue']])
else:
    print("Columns missing.")
    print(df.columns.tolist())
