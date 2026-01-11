import pandas as pd

try:
    df = pd.read_csv('c:/Dev/entrevista/CASE_STUDY_CLEAN.csv')
    
    # Column mapping
    col_map = {c: c.lower() for c in df.columns}
    if 'revenue_in_euros' in col_map: df.rename(columns={'revenue_in_euros': 'revenue'}, inplace=True)
    elif 'revenue (in euros)' in col_map: df.rename(columns={'revenue (in euros)': 'revenue'}, inplace=True)
    for c in df.columns:
        if 'revenue' in c and 'lost' not in c and 'click' not in c: df.rename(columns={c: 'revenue'}, inplace=True); break

    print("\n=== PARETO SUMMARY ===")
    
    # 1. GLOBAL
    client_rev = df.groupby('client_id')['revenue'].sum().sort_values(ascending=False)
    total_rev = client_rev.sum()
    top_1_pct_count = int(len(client_rev) * 0.01)
    rev_top_1 = client_rev.head(top_1_pct_count).sum()
    print(f"1. GLOBAL: Top 1% clients = { (rev_top_1/total_rev)*100:.1f}% of Revenue")

    # 2. SEGMENT
    print("\n2. SEGMENT SKEW (Top 1% Share):")
    for seg in df['segment'].unique():
        s_df = df[df['segment'] == seg]
        s_rev = s_df.groupby('client_id')['revenue'].sum().sort_values(ascending=False)
        if len(s_rev) > 0:
            top_1 = s_rev.head(int(len(s_rev)*0.01)).sum()
            share = (top_1 / s_rev.sum()) * 100
            print(f"   - {seg}: {share:.1f}%")

    # 3. VERTICAL
    print("\n3. VERTICAL SKEW (Top 5 Most Concentrated):")
    vert_stats = []
    for v in df['vertical'].unique():
        v_df = df[df['vertical'] == v]
        v_rev = v_df.groupby('client_id')['revenue'].sum().sort_values(ascending=False)
        if len(v_rev) > 0 and v_rev.sum() > 0:
            top_1 = v_rev.head(int(len(v_rev)*0.01)).sum()
            share = (top_1 / v_rev.sum()) * 100
            vert_stats.append((v, share))
            
    vert_stats.sort(key=lambda x: x[1], reverse=True)
    for v, share in vert_stats[:5]:
        print(f"   - {v}: {share:.1f}%")

except Exception as e:
    print(e)
