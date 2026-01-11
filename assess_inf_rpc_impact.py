import pandas as pd
import numpy as np

def load_and_analyze():
    print("Loading Data...")
    try:
        df = pd.read_csv('c:/Dev/entrevista/CASE_STUDY_CLEAN.csv', sep=',')
    except:
        df = pd.read_csv('c:/Dev/entrevista/CASE_STUDY_CLEAN.csv', sep=';')

    # Standardize columns
    df.columns = [c.strip().lower().replace(' ', '_').replace('.', '') for c in df.columns]
    print(f"Columns: {df.columns.tolist()}")

    # RAW INDEX MAPPING (CLEAN CSV)
    # Index 5: segment
    # Index 6: revenue (in euros?)
    # Index 8: criteo_clicks
    
    try:
        df.rename(columns={
            df.columns[5]: 'segment',
            df.columns[6]: 'revenue',
            df.columns[8]: 'criteo_clicks'
        }, inplace=True)
        print("Mapped columns by index (5=Seg, 6=Rev, 8=Clicks)")
    except Exception as e:
        print(f"Index mapping failed: {e}")
        # Fallback to string search if index fails (unlikely)
    
    revenue_col = 'revenue'
    clicks_col = 'criteo_clicks'
    segment_col = 'segment'

    if not revenue_col or not clicks_col or not segment_col:
        print("CRITICAL: Could not map necessary columns.")
        return

    # Ensure numeric
    def clean_num(x):
        if isinstance(x, str):
            return float(x.replace('€', '').replace(',', '').strip())
        return float(x)
        
    df[revenue_col] = df[revenue_col].apply(clean_num)
    df[clicks_col] = pd.to_numeric(df[clicks_col], errors='coerce').fillna(0)

    # Filter for Small / Extra-Small
    target_segments = ['Small', 'Extra-Small', 'Medium'] # Added Medium for context
    
    print("\n--- INFINITE RPC ANALYSIS (Rev > 0, Clicks = 0) ---")
    
    for seg in target_segments:
        seg_df = df[df[segment_col] == seg]
        total_rev = seg_df[revenue_col].sum()
        
        # Infinite RPC Rows
        inf_rows = seg_df[(seg_df[clicks_col] == 0) & (seg_df[revenue_col] > 0)]
        inf_rev = inf_rows[revenue_col].sum()
        inf_count = len(inf_rows)
        total_count = len(seg_df)
        
        if total_rev > 0:
            share = (inf_rev / total_rev) * 100
        else:
            share = 0.0
            
        print(f"\nSegment: {seg}")
        print(f"  Total Rows: {total_count}")
        print(f"  Inf RPC Rows: {inf_count} ({inf_count/total_count*100:.2f}%)")
        print(f"  Total Revenue: €{total_rev:,.2f}")
        print(f"  Inf RPC Revenue: €{inf_rev:,.2f}")
        print(f"  **Impact Share: {share:.2f}%**")

    # Strategy Simulation (Global)
    print("\n--- STRATEGY SIMULATION (Global) ---")
    global_inf = df[(df[clicks_col] == 0) & (df[revenue_col] > 0)]
    print(f"Total Ghost Revenue: €{global_inf[revenue_col].sum():,.2f}")
    
    # Strategy 1: Imputation
    # Estimate clicks needed to justify revenue based on global Avg RPC (Simple proxy)
    global_rev = df[revenue_col].sum()
    global_clicks = df[clicks_col].sum()
    avg_rpc = global_rev / global_clicks if global_clicks > 0 else 0.50 # fallback
    
    imputed_clicks = global_inf[revenue_col] / avg_rpc
    print(f"Strategy 1 (Imputation): Would add ~{int(imputed_clicks.sum())} clicks to dataset.")
    print("  Result: 0 'Inf RPC' rows remain. ZERO data loss.")

    # Strategy 2: Min Clicks (Set to 1)
    # This adds exactly 1 click per row.
    min_clicks_added = len(global_inf)
    print(f"Strategy 2 (Min Flow): Would add {min_clicks_added} clicks to dataset.")
    print("  Pros: Simple. Cons: Underestimates traffic if revenue is high (e.g. €100 rev with 1 click = €100 RPC outlier).")

if __name__ == "__main__":
    load_and_analyze()
