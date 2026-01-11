import pandas as pd
import numpy as np

def parse_currency(x):
    if isinstance(x, str):
        return x.replace('€', '').replace(',', '').strip()
    return x

try:
    df = pd.read_csv('c:/Dev/entrevista/CASE_STUDY_CLEAN.csv', sep=',')
    
    # Standardize columns
    df.columns = [c.strip().lower().replace(' ', '_') for c in df.columns]
    
    # Clean numeric columns
    numeric_cols = ['revenue', 'competitor_clicks', 'estimated_revenue_lost']
    for col in numeric_cols:
        if col in df.columns:
            df[col] = df[col].apply(parse_currency).astype(float)
        
    print("--- DATA LOADED ---")
    
    # CHECK 1: CLIENT 2560
    client_2560 = df[df['client_id'] == 2560]
    if not client_2560.empty:
        total_rev_lost = client_2560['estimated_revenue_lost'].sum()
        max_rev_lost = client_2560['estimated_revenue_lost'].max()
        print(f"\n--- CLIENT 2560 ANALYSIS ---")
        print(f"Total 'Estimated Revenue Lost' (Original): €{total_rev_lost:,.2f}")
        print(f"Max Monthly 'Estimated Revenue Lost': €{max_rev_lost:,.2f}")
        
        # Calculate 'Corrected' Risk (Simple version: using max RPC observed)
        # Check if we can calculate RPC
        if 'revenue_per_click' in client_2560.columns:
             # Just checking if the consultant number matches the ORIGINAL sum
             pass
    else:
        print("\n--- CLIENT 2560 NOT FOUND ---")

    # CHECK 2: TOP 20 CLIENTS (Original Metric)
    top_20_original = df.groupby('client_id')['estimated_revenue_lost'].sum().sort_values(ascending=False).head(20)
    top_20_sum = top_20_original.sum()
    print(f"\n--- TOP 20 CLIENTS (Original Metric) ---")
    print(f"Sum of Top 20: €{top_20_sum:,.2f}")
    print("Top 5 IDs and Values:")
    print(top_20_original.head(5))

    # CHECK 3: GLOBAL TOTAL (Original Metric)
    total_original = df['estimated_revenue_lost'].sum()
    print(f"\n--- GLOBAL TOTAL (Original Metric) ---")
    print(f"Total Estimated Revenue Lost: €{total_original:,.2f}")
    
    # CHECK 4: DATASET DATE RANGE
    if 'month' in df.columns:
        print(f"\n--- DATE RANGE ---")
        print(f"Start: {df['month'].min()}")
        print(f"End: {df['month'].max()}")


    # CHECK 6: SEARCH FOR ~45M CLIENT
    print(f"\n--- SEARCH FOR ~€45M CLIENT ---")
    potential_whales = df[(df['estimated_revenue_lost'] > 40000000) & (df['estimated_revenue_lost'] < 50000000)]
    if not potential_whales.empty:
        print(potential_whales[['client_id', 'estimated_revenue_lost']].drop_duplicates())
    else:
        print("No clients found between €40M and €50M.")
        
    print(f"\n--- SEARCH FOR ~€45M (Corrected Risk) ---")
    # This would require repeating the 'Corrected' logic, skipping for now to keep it fast.
    
except Exception as e:
    print(f"Error: {e}")
