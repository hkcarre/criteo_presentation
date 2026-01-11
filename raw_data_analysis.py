import pandas as pd
import numpy as np

print("Loading data...")
df = pd.read_csv('CASE_STUDY_RAW.csv', low_memory=False)

print(f"=== COMPREHENSIVE DATA PATTERN ANALYSIS ===")
print(f"Total records: {len(df):,}")
print(f"Columns: {df.columns.tolist()}")

# Convert numeric columns
rev = pd.to_numeric(df['revenue_euro'], errors='coerce')
comp = pd.to_numeric(df['competitor_clicks'], errors='coerce')
criteo = pd.to_numeric(df['criteo_clicks'], errors='coerce')
rpc = pd.to_numeric(df['revenue_per_click'], errors='coerce')
erl = pd.to_numeric(df['estimated_revenue_lost'], errors='coerce')

print("\n=== 1. ZERO VALUE BREAKDOWN ===")
print(f"revenue_euro = 0: {(rev==0).sum():,} ({(rev==0).sum()/len(df)*100:.1f}%)")
print(f"competitor_clicks = 0: {(comp==0).sum():,} ({(comp==0).sum()/len(df)*100:.1f}%)")
print(f"criteo_clicks = 0: {(criteo==0).sum():,} ({(criteo==0).sum()/len(df)*100:.1f}%)")
print(f"revenue_per_click = 0: {(rpc==0).sum():,} ({(rpc==0).sum()/len(df)*100:.1f}%)")

print("\n=== 2. ROOT CAUSE: Inactive Month Pattern ===")
zero_criteo = criteo == 0
zero_revenue = rev == 0
inactive = zero_criteo & zero_revenue
print(f"Records with zero Criteo clicks: {zero_criteo.sum():,} ({zero_criteo.sum()/len(df)*100:.1f}%)")
print(f"Of those, also zero revenue: {(zero_criteo & zero_revenue).sum():,} ({(zero_criteo & zero_revenue).sum()/zero_criteo.sum()*100:.1f}%)")
print(f"HYPOTHESIS: These are 'inactive months' - client in system but no transactions")

print("\n=== 3. SEGMENT PATTERN ===")
for seg in df['segment'].dropna().unique():
    seg_mask = df['segment'] == seg
    seg_zero = (rev[seg_mask] == 0).sum()
    seg_total = seg_mask.sum()
    seg_avg = rev[seg_mask].mean()
    print(f"{seg}: {seg_zero:,}/{seg_total:,} ({seg_zero/seg_total*100:.1f}%) zero-rev, avg=${seg_avg:.2f}")

print("\n=== 4. COMPETITOR DETECTION BY MARKET (UTM PATTERN) ===")
for mkt in df['market'].value_counts().head(10).index:
    mkt_mask = df['market'] == mkt
    mkt_has_comp = (comp[mkt_mask] > 0).sum()
    mkt_total = mkt_mask.sum()
    print(f"{mkt}: {mkt_has_comp:,}/{mkt_total:,} ({mkt_has_comp/mkt_total*100:.1f}%) have competitor activity")

print("\n=== 5. TEXT/NON-NUMERIC ANOMALIES ===")
for col in ['revenue_euro', 'competitor_clicks', 'criteo_clicks', 'revenue_per_click', 'estimated_revenue_lost']:
    numeric_conv = pd.to_numeric(df[col], errors='coerce')
    non_numeric = numeric_conv.isna() & df[col].notna()
    if non_numeric.sum() > 0:
        examples = df.loc[non_numeric, col].unique()[:5]
        print(f"{col}: {non_numeric.sum()} non-numeric values - Examples: {examples.tolist()}")
    else:
        print(f"{col}: No text anomalies detected")

print("\n=== 6. MISSING VALUES ===")
for col in df.columns:
    null_count = df[col].isna().sum()
    if null_count > 0:
        print(f"{col}: {null_count:,} ({null_count/len(df)*100:.2f}%) missing")

print("\n=== ANALYSIS COMPLETE ===")
