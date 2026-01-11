import pandas as pd

try:
    df = pd.read_csv('c:/Dev/entrevista/CASE_STUDY_CLEAN.csv')
    
    # Column map
    col_map = {c: c.lower() for c in df.columns}
    if 'revenue_in_euros' in col_map: df.rename(columns={'revenue_in_euros': 'revenue'}, inplace=True)
    elif 'revenue (in euros)' in col_map: df.rename(columns={'revenue (in euros)': 'revenue'}, inplace=True)
    for c in df.columns:
        if 'revenue' in c and 'lost' not in c and 'click' not in c: df.rename(columns={c: 'revenue'}, inplace=True); break

    df['month'] = pd.to_datetime(df['month'])

    print("\n=== FINAL ANSWERS ===")
    
    # 1. RUSSIA
    russia_df = df[df['market'].str.contains('Russia', case=False, na=False)]
    print(f"1. RUSSIA: {len(russia_df)} records. Total Revenue: €{russia_df['revenue'].sum():,.0f}. Comp Clicks: {russia_df['competitor_clicks'].sum():,.0f}")
    
    # 2. CHURN LAG (Client 31782)
    c_df = df[df['client_id'] == 31782].sort_values('month')
    first_spike = None; crash = None
    for idx, row in c_df.iterrows():
        if first_spike is None and row['competitor_clicks'] > 100000: first_spike = row['month']
        if crash is None and row['revenue'] < 10000 and row['month'].year >= 2024: crash = row['month']
    
    if first_spike and crash:
        lag = (crash.year - first_spike.year) * 12 + (crash.month - first_spike.month)
        print(f"2. CHURN LAG: Spike {first_spike.date()} -> Crash {crash.date()}. LAG = {lag} MONTHS.")
    else:
        print("2. CHURN LAG: Undetermined.")

    # 3. SEGMENTS (Top 3 Risk)
    print("\n3. SEGMENT RISK (Top 3 by Comp Intensity):")
    # Simplify risk metric: Comp Clicks per Client-Month
    seg_stats = df.groupby('segment').agg({'competitor_clicks': 'sum', 'client_id': 'count', 'revenue': 'sum'})
    seg_stats['intensity'] = seg_stats['competitor_clicks'] / seg_stats['client_id']
    print(seg_stats.sort_values('intensity', ascending=False).head(3))

except Exception as e:
    print(e)
