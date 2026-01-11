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
    
    print(f"Total Revenue 2024 sum: {df[df['year']==2024]['revenue'].sum():,.0f}")
    
    # Uppercase Markets
    df['market'] = df['market'].str.upper()
    
    res_list = []
    for m in df['market'].unique():
        sub = df[df['market'] == m]
        rev_23 = sub[sub['year'] == 2023]['revenue'].mean() * 12
        rev_24 = sub[sub['year'] == 2024]['revenue'].mean() * 12
        
        # Handle missing years
        if pd.isna(rev_23): rev_23 = 0
        if pd.isna(rev_24): rev_24 = 0
        
        delta = rev_24 - rev_23
        est_loss = sub[sub['year'] == 2024]['estimated_revenue_lost'].sum()
        
        res_list.append({'Market': m, 'Actual_Delta': delta, 'Est_Risk': est_loss})
    
    res = pd.DataFrame(res_list).set_index('Market').sort_values('Est_Risk', ascending=False)
    
    print("\nMARKET | EST_RISK | ACTUAL_DELTA")
    for m, row in res.head(5).iterrows():
        print(f"{m} | €{row['Est_Risk']:,.0f} | €{row['Actual_Delta']:,.0f}")
        
    print(f"RUSSIA | €{res.loc['RUSSIA']['Est_Risk']:,.0f} | €{res.loc['RUSSIA']['Actual_Delta']:,.0f}")
    
    print(f"\nCorrelation: {res['Actual_Delta'].corr(res['Est_Risk']):.4f}")

except Exception as e:
    print(e)
