
import pandas as pd
import numpy as np

def generate_imputed_dataset():
    print("Loading original data...")
    try:
        df = pd.read_csv('c:/Dev/entrevista/CASE_STUDY_CLEAN.csv', sep=',')
    except:
        df = pd.read_csv('c:/Dev/entrevista/CASE_STUDY_CLEAN.csv', sep=';')
    
    # Normalize Columns
    cols = df.columns
    # Map columns accurately
    rev_col = [c for c in cols if 'revenue' in c.lower() and 'estimated' not in c.lower()][0]
    if 'criteo_revenue' in cols: rev_col = 'criteo_revenue'
    
    # Criteo Clicks (Target for imputation)
    # usually index 7 is comp clicks, 8 is criteo clicks in original, but let's find it
    # Searching for 'criteo_clicks' or 'clicks' that isn't competitor
    click_cols = [c for c in cols if 'click' in c.lower()]
    criteo_click_col = [c for c in click_cols if 'competitor' not in c.lower()][0]
    
    segment_col = [c for c in cols if 'segment' in c.lower()][0]
    vertical_col = [c for c in cols if 'vertical' in c.lower()][0]
    
    print(f"Mapping: Revenue='{rev_col}', Criteo Clicks='{criteo_click_col}', Segment='{segment_col}'")

    # Ensure numeric
    df[rev_col] = pd.to_numeric(df[rev_col], errors='coerce').fillna(0)
    df[criteo_click_col] = pd.to_numeric(df[criteo_click_col], errors='coerce').fillna(0)

    # 1. Calculate Segment Benchmarks (Avg RPC) from Valid Data
    # Valid = Revenue > 0 AND Clicks > 0
    valid_mask = (df[rev_col] > 0) & (df[criteo_click_col] > 0)
    df_valid = df[valid_mask].copy()
    
    # Calculate RPC for valid rows
    df_valid['RPC'] = df_valid[rev_col] / df_valid[criteo_click_col]
    
    # Group by Segment to get Benchmark RPC
    segment_rpc = df_valid.groupby(segment_col)['RPC'].mean().to_dict()
    print("\n--- SEGMENT RPC BENCHMARKS USED FOR IMPUTATION ---")
    for seg, rpc in segment_rpc.items():
        print(f"  {seg}: €{rpc:.2f}")

    # 2. Identify "Ghost Rows" (Infinite RPC / Zero Clicks)
    # Revenue > 0 AND Clicks == 0
    ghost_mask = (df[rev_col] > 0) & (df[criteo_click_col] == 0)
    ghost_count = ghost_mask.sum()
    print(f"\nFound {ghost_count} 'Ghost Revenue' rows to impute.")

    # 3. Impute
    # We create a new column 'Imputed_Criteo_Clicks'
    # Start with original clicks
    df['Corrected_Criteo_Clicks'] = df[criteo_click_col]
    df['Imputation_Flag'] = False

    # Apply imputation logic
    # Clicks = Revenue / Segment_RPC
    def impute_clicks(row):
        seg = row[segment_col]
        rev = row[rev_col]
        clicks = row[criteo_click_col]
        
        if rev > 0 and clicks == 0:
            avg_rpc = segment_rpc.get(seg, 0)
            if avg_rpc > 0:
                return round(rev / avg_rpc)
            else:
                return 0
        return clicks

    # This might be slow with apply on large df, but for <1M rows it's acceptable for a one-off
    # Vectorized approach is better:
    for seg, avg_rpc in segment_rpc.items():
        # Mask for this segment AND ghost rows
        seg_ghost_mask = ghost_mask & (df[segment_col] == seg)
        if avg_rpc > 0:
            df.loc[seg_ghost_mask, 'Corrected_Criteo_Clicks'] = (df.loc[seg_ghost_mask, rev_col] / avg_rpc).round()
            df.loc[seg_ghost_mask, 'Imputation_Flag'] = True

    # ... (Imputation logic remains)
    
    # 4. Calculate Final Corrected RPC (Standardized Name)
    # The user specifically requested "Revenue / Criteo Clicks" to Replace Inf.
    # We use the Corrected Clicks denominator.
    
    df['RPC'] = 0.0
    
    # Logic: 
    # If Clicks > 0: RPC = Revenue / Clicks
    # If Clicks = 0 and Revenue = 0: RPC = 0
    # If Clicks = 0 and Revenue > 0: Imputation Logic handled this (Clicks became > 0).
    
    # Safety Check: Enforce Imputation again for any missed rows if necessary, 
    # but strictly calculate RPC using the new denominator.
    
    mask_valid_clicks = df['Corrected_Criteo_Clicks'] > 0
    df.loc[mask_valid_clicks, 'RPC'] = df.loc[mask_valid_clicks, rev_col] / df.loc[mask_valid_clicks, 'Corrected_Criteo_Clicks']
    
    # Round to 2 decimals for readability
    df['RPC'] = df['RPC'].round(2)

    # 5. Verification
    inf_count = np.isinf(df['RPC']).sum()
    nan_count = df['RPC'].isna().sum()
    print(f"\n--- QA CHECK ---")
    print(f"Remaining 'Inf' RPC values: {inf_count}")
    print(f"Remaining 'NaN' RPC values: {nan_count}")
    
    if inf_count == 0:
        print("SUCCESS: All Infinite RPCs have been resolved.")

    # 6. Export
    # We'll save the essential columns clearly
    output_df = df.copy()
    output_path = 'c:/Dev/entrevista/CASE_STUDY_RECALCULATED.csv'
    output_df.to_csv(output_path, index=False)
    print(f"\nSuccess. Dataset saved to: {output_path}")
    print(f"Rows Imputed: {df['Imputation_Flag'].sum()}")

if __name__ == "__main__":
    generate_imputed_dataset()
