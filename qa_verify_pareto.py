import pandas as pd
import numpy as np

pd.set_option('display.max_rows', None)
pd.set_option('display.float_format', '{:.4f}'.format)

try:
    df = pd.read_csv('c:/Dev/entrevista/CASE_STUDY_CLEAN.csv')
    
    # Column mapping (Standardization)
    col_map = {c: c.lower() for c in df.columns}
    if 'revenue_in_euros' in col_map: df.rename(columns={'revenue_in_euros': 'revenue'}, inplace=True)
    elif 'revenue (in euros)' in col_map: df.rename(columns={'revenue (in euros)': 'revenue'}, inplace=True)
    for c in df.columns:
        if 'revenue' in c and 'lost' not in c and 'click' not in c: df.rename(columns={c: 'revenue'}, inplace=True); break

    print("\n=== QA AUDIT: PARETO FIGURES ===")
    
    # helper for verification
    def verify_group(label, data):
        client_rev = data.groupby('client_id')['revenue'].sum().sort_values(ascending=False)
        total_rev = client_rev.sum()
        total_clients = len(client_rev)
        
        # Strict 1% definition: int(total_clients * 0.01)
        # Note: if < 100 clients, this might be 0. Let's check logic.
        top_1_count = int(total_clients * 0.01)
        if top_1_count == 0 and total_clients > 0: top_1_count = 1 # Edge case adjustment for small groups? 
        # Actually, let's stick to the previous logic to see if it matches, then critique if loop-hole found.
        # The previous script used: top_1_pct_count = int(len(client_rev) * 0.01)
        
        top_1_count_strict = int(total_clients * 0.01)
        
        rev_top_1 = client_rev.head(top_1_count_strict).sum()
        share = (rev_top_1 / total_rev * 100) if total_rev > 0 else 0
        
        print(f"\n[{label}]")
        print(f"   Total Clients: {total_clients}")
        print(f"   Total Revenue: €{total_rev:,.2f}")
        print(f"   Top 1% Count (Strict Int): {top_1_count_strict}")
        print(f"   Top 1% Revenue: €{rev_top_1:,.2f}")
        print(f"   Share: {share:.4f}%")
        return share

    # 1. GLOBAL VERIFY
    verify_group("GLOBAL", df)

    # 2. SEGMENT VERIFY (Large vs Small)
    verify_group("SEGMENT: Large", df[df['segment'] == 'Large'])
    verify_group("SEGMENT: Small", df[df['segment'] == 'Small'])

    # 3. VERTICAL VERIFY (Classifieds/Career vs Travel Agencies)
    verify_group("VERTICAL: CLASSIFIEDS/CAREER", df[df['vertical'] == 'CLASSIFIEDS/CAREER'])
    verify_group("VERTICAL: TRAVEL AGENCIES", df[df['vertical'] == 'TRAVEL AGENCIES'])

except Exception as e:
    print(e)
