import pandas as pd
import json

# BRUTE FORCE PARSING
# ROBUST PARSING
try:
    # Try reading with python engine which is more forgiving
    df = pd.read_csv('c:/Dev/entrevista/CASE_STUDY_RAW.csv', sep=None, engine='python')
    print("Read with python engine auto-sep")
except:
    try:
        df = pd.read_csv('c:/Dev/entrevista/CASE_STUDY_RAW.csv', sep=',')
        print("Read with comma")
    except:
        df = pd.read_csv('c:/Dev/entrevista/CASE_STUDY_RAW.csv', sep=';')
        print("Read with semicolon")

# Standardize columns
df.columns = [c.strip().lower().replace(' ', '_').replace('"', '') for c in df.columns]
print(f"DEBUG FINAL COLS: {df.columns.tolist()}")

# Map Clicks
if 'criteo_clicks' not in df.columns:
     # Look for anything with 'clicks' that isn't competitor
     for c in df.columns:
         if 'clicks' in c and 'competitor' not in c and 'lost' not in c:
             df.rename(columns={c: 'criteo_clicks'}, inplace=True)
             break

def clean_curr(x):
    if isinstance(x, str): 
        return float(x.replace('€', '').replace(',', '').strip())
    return float(x)
    
# Map Revenue
if 'revenue' not in df.columns:
    if 'revenue_in_euros' in df.columns: 
        df.rename(columns={'revenue_in_euros': 'revenue'}, inplace=True)
    elif 'revenue_per_click' in df.columns:
        # Fallback
        # Ensure numeric columns
        df['criteo_clicks'] = pd.to_numeric(df['criteo_clicks'], errors='coerce').fillna(0)
        df['revenue_per_click'] = df['revenue_per_click'].apply(clean_curr)
        df['revenue'] = df['criteo_clicks'] * df['revenue_per_click']

# Ensure numeric Revenue
if 'revenue' in df.columns:
    df['revenue'] = df['revenue'].apply(clean_curr)

inf_cases = df[(df['criteo_clicks'] == 0) & (df['revenue'] > 0)]

count = len(inf_cases)
total_revenue_affected = inf_cases['revenue'].sum()
total_global_revenue = df['revenue'].sum()

print(f"Total Infinite RPC Count: {count}")
print(f"Total Revenue Affected: €{total_revenue_affected:,.2f}")

# 2. SEGMENT BREAKDOWN
print("\n--- BY SEGMENT ---")
if 'segment' in df.columns:
    seg_stats = inf_cases.groupby('segment')['revenue'].agg(['count', 'sum'])
    seg_stats['share_of_issue'] = (seg_stats['sum'] / total_revenue_affected) * 100
    print(seg_stats.sort_values('sum', ascending=False))
else:
    print("Segment column not found.")
