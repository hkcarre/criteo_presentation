import pandas as pd

try:
    df = pd.read_csv('c:/Dev/entrevista/CASE_STUDY_CLEAN.csv')
    col_map = {c: c.lower() for c in df.columns}
    if 'revenue_in_euros' in col_map: df.rename(columns={'revenue_in_euros': 'revenue'}, inplace=True)
    elif 'revenue (in euros)' in col_map: df.rename(columns={'revenue (in euros)': 'revenue'}, inplace=True)
    for c in df.columns:
        if 'revenue' in c and 'lost' not in c and 'click' not in c: df.rename(columns={c: 'revenue'}, inplace=True); break
    
    df['month'] = pd.to_datetime(df['month'])
    df['year'] = df['month'].dt.year
    
    travel_df = df[df['vertical'].isin(['TRAVEL AGENCIES', 'TRAVEL SERVICES'])].copy()
    
    print("\n=== FINAL TRAVEL NUMBERS ===")
    t23 = travel_df[travel_df['year'] == 2023]
    t24 = travel_df[travel_df['year'] == 2024]
    
    rpc_23 = t23['revenue'].sum() / t23['criteo_clicks'].sum()
    clicks_24 = t24['competitor_clicks'].sum()
    reported_24 = t24['estimated_revenue_lost'].sum()
    corrected_24 = clicks_24 * rpc_23
    
    print(f"2023 Stable RPC: €{rpc_23:.4f}")
    print(f"2024 Competitor Clicks: {clicks_24:,.0f}")
    print(f"2024 Reported Risk:   €{reported_24:,.0f}")
    print(f"2024 Corrected Risk:  €{corrected_24:,.0f}")
    print(f"Multiplier: {corrected_24 / reported_24:.1f}x")

except Exception as e:
    print(e)
