
import pandas as pd
import numpy as np

def analyze_correlations():
    print("Loading data...")
    # Force comma separator per verification
    try:
        df = pd.read_csv('c:/Dev/entrevista/CASE_STUDY_CLEAN.csv', sep=',')
        print(f"Loaded {len(df)} rows.")
        print(f"Columns: {list(df.columns)}")
    except Exception as e:
        print(f"Error: {e}")
        return

    # Dynamic Column Mapping
    # We look for specific keywords if exact names vary
    cols = df.columns
    
    # 1. Revenue
    rev_col = [c for c in cols if 'revenue' in c.lower() and 'estimated' not in c.lower()][0] # Avoid 'estimated_revenue_lost'
    # Actually, let's be safe. In previous scripts, we saw 'revenue' might be unnamed or hard to find.
    # Looking at the raw output: "Unnamed: 0,month,client_id,market,vertical,segme..."
    # Let's map by index 3,4,5,6,7,8 as a fallback if names fail
    
    market_col = 'market' if 'market' in cols else cols[3]
    vertical_col = 'vertical' if 'vertical' in cols else cols[4]
    segment_col = 'segment' if 'segment' in cols else cols[5]
    
    # Revenue is usually index 6
    if 'criteo_revenue' in cols: rev_col = 'criteo_revenue'
    elif 'revenue' in cols: rev_col = 'revenue'
    else: rev_col = cols[6]

    # Competitor Clicks usually index 7
    if 'competitor_clicks' in cols: comp_col = 'competitor_clicks'
    else: comp_col = cols[7]

    print(f"Using columns: Market='{market_col}', Vertical='{vertical_col}', Seg='{segment_col}', Rev='{rev_col}', Comp='{comp_col}'")

    # Ensure numeric
    df[rev_col] = pd.to_numeric(df[rev_col], errors='coerce').fillna(0)
    df[comp_col] = pd.to_numeric(df[comp_col], errors='coerce').fillna(0)


    # ... (Loading code remains same until data prep) ...
    # Ensure numeric
    df[rev_col] = pd.to_numeric(df[rev_col], errors='coerce').fillna(0)
    df[comp_col] = pd.to_numeric(df[comp_col], errors='coerce').fillna(0)
    
    output = []
    output.append(f"ANALYSIS DATE: 2026-01-11")
    output.append(f"ROWS: {len(df)}")

    # 1. Global (All Data)
    global_corr_all = df[rev_col].corr(df[comp_col])
    output.append(f"\n--- GLOBAL (ALL DATA) ---")
    output.append(f"Correlation: {global_corr_all:.4f}")
    
    # 2. Global (Active Threat Only)
    df_active = df[df[comp_col] > 0]
    output.append(f"\n--- GLOBAL (ACTIVE THREATS ONLY, n={len(df_active)}) ---")
    global_corr_active = df_active[rev_col].corr(df_active[comp_col])
    output.append(f"Correlation: {global_corr_active:.4f}")
    
    # 3. By Market (Active Only)
    output.append(f"\n--- BY MARKET (Active Only, Sorted Negative to Positive) ---")
    def get_corr_active(x):
        # Only consider if sufficient data points
        if len(x) < 20: return np.nan
        return x[rev_col].corr(x[comp_col])
        
    market_corr = df_active.groupby(market_col).apply(get_corr_active).sort_values()
    output.append(market_corr.to_string())

    # 4. By Vertical (Active Only)
    output.append(f"\n--- BY VERTICAL (Active Only) ---")
    vert_corr = df_active.groupby(vertical_col).apply(get_corr_active).sort_values()
    output.append(vert_corr.to_string())

    # 5. By Segment (Active Only)
    output.append(f"\n--- BY SEGMENT (Active Only) ---")
    seg_corr = df_active.groupby(segment_col).apply(get_corr_active).sort_values()
    output.append(seg_corr.to_string())
    
    # 6. Top Bleeding Clusters (Market + Segment)
    output.append(f"\n--- TOP BLEEDING CLUSTERS (Market + Segment) ---")
    cluster_corr = df_active.groupby([market_col, segment_col]).apply(get_corr_active).sort_values()
    output.append(cluster_corr.head(15).to_string())

    with open('c:/Dev/entrevista/correlation_results.txt', 'w') as f:
        f.write('\n'.join(output))
    print("Results saved to correlation_results.txt")

if __name__ == "__main__":
    analyze_correlations()
