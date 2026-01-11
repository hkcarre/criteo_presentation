import pandas as pd

try:
    df = pd.read_csv('c:/Dev/entrevista/CASE_STUDY_CLEAN.csv')
    
    # Robust Column Mapping
    col_map = {c: c.lower() for c in df.columns}
    if 'revenue_in_euros' in col_map: df.rename(columns={'revenue_in_euros': 'revenue'}, inplace=True)
    elif 'revenue (in euros)' in col_map: df.rename(columns={'revenue (in euros)': 'revenue'}, inplace=True)
    for c in df.columns:
        if 'revenue' in c and 'lost' not in c and 'click' not in c: df.rename(columns={c: 'revenue'}, inplace=True); break
            
    df['month'] = pd.to_datetime(df['month'])
    
    t = df[df['vertical'].isin(['TRAVEL AGENCIES', 'TRAVEL SERVICES'])]
    t23 = t[t['month'].dt.year == 2023]
    
    rev = t23['revenue'].sum()
    clicks = t23['criteo_clicks'].sum()
    rpc = rev / clicks if clicks > 0 else 0
    
    print("\n=== RAW VERIFICATION 2023 ===")
    print(f"Revenue: €{rev:,.2f}")
    print(f"Clicks:  {clicks:,.0f}")
    print(f"RPC:     €{rpc:.4f}")

except Exception as e:
    print(e)
