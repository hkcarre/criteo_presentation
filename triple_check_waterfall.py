
import pandas as pd
import numpy as np

def calibrate_risk():
    print("Loading CASE_STUDY_RECALCULATED.csv...")
    try:
        df = pd.read_csv('c:/Dev/entrevista/CASE_STUDY_RECALCULATED.csv')
    except Exception as e:
        print(f"Error loading CSV: {e}")
        return

    print("Columns found:", df.columns.tolist())

    # Identify key columns
    # We need 'revenue_euro', 'competitor_clicks', and 'estimated_revenue_lost'
    # Based on previous output, 'estimated_revenue_lost' might be named differently or need calc.
    # Looking for 'loss' or 'lost'
    loss_col = [c for c in df.columns if 'loss' in c.lower() or 'lost' in c.lower()]
    target_loss_col = loss_col[0] if loss_col else None
    
    if not target_loss_col:
        # If missing, calculate it: Competitor Clicks * RPC (Revenue / Corrected Clicks)
        print("Warning: 'estimated_revenue_lost' column not found. Calculating...")
        # RPC is likely in 'RPC' column (from imputation script)
        if 'RPC' not in df.columns:
             df['RPC'] = df['revenue_euro'] / df['Corrected_Criteo_Clicks'].replace(0, 1)
        
        df['estimated_revenue_lost'] = df['competitor_clicks'] * df['RPC']
        target_loss_col = 'estimated_revenue_lost'
    else:
        print(f"Using existing loss column: {target_loss_col}")

    # 1. Gross Estimated Loss (Total Universe)
    gross_loss = df[target_loss_col].sum()
    print(f"\n--- 1. GROSS ESTIMATED LOSS (All Competitor Activity) ---")
    print(f"Total: €{gross_loss:,.0f}")

    # 2. Segment-Level Correlation Analysis
    # We will group by Market + Vertical to find "Bleeding Segments"
    print(f"\n--- 2. CALIBRATION (Correlation Filter) ---")
    
    results = []
    
    # Group by Market and Vertical (broader clusters than Segment to get stat significance)
    groups = df.groupby(['market', 'vertical'])
    
    calibrated_loss_sum = 0
    
    print(f"{'Market':<15} {'Vertical':<20} {'Points':<8} {'Corr (r)':<10} {'Est Loss (€)':<15} {'Status'}")
    print("-" * 85)

    for name, group in groups:
        market, vertical = name
        n = len(group)
        loss_val = group[target_loss_col].sum()
        
        # Calculate Correlation if data sufficiency met
        if n > 10 and group['competitor_clicks'].sum() > 0:
            corr = group['revenue_euro'].corr(group['competitor_clicks'])
            if pd.isna(corr): corr = 0
        else:
            corr = 0 # Default to neutral
            
        status = "PARASITIC (Safe)"
        if corr < -0.05: # Threshold for Negative Correlation
            status = "BLEEDING (Risk)"
            calibrated_loss_sum += loss_val
            
        print(f"{str(market)[:15]:<15} {str(vertical)[:20]:<20} {n:<8} {corr:<10.4f} €{loss_val:,.0f}      {status}")

    # --- RE-INSERTED LOGIC ---
    bleeding_keys = []
    for name, group in groups:
        if len(group) > 10 and group['competitor_clicks'].sum() > 0:
             corr = group['revenue_euro'].corr(group['competitor_clicks'])
             if corr < -0.05:
                 bleeding_keys.append(name)

    # Filter DF for Whale Risk
    bleeding_mask = df.set_index(['market', 'vertical']).index.isin(bleeding_keys)
    df_bleeding = df[bleeding_mask]
    whale_risk = df_bleeding.groupby('client_id')[target_loss_col].sum().nlargest(20).sum()

    with open('c:/Dev/entrevista/triple_check_results.txt', 'w', encoding='utf-8') as f:
        f.write(f"--- 3. TRIPLE CHECKED FIGURES ---\n")
        f.write(f"A. Gross Estimated Loss (Total):     €{gross_loss:,.2f}\n")
        f.write(f"B. Calibrated Risk (Bleeding Only):  €{calibrated_loss_sum:,.2f}\n")
        f.write(f"   (Segments with Correlation < -0.05)\n")
        f.write(f"C. Whale Risk (Top 20 in Bleeding):  €{whale_risk:,.2f}\n")
        
        f.write(f"\n--- DETAIL: BLEEDING SEGMENTS ---\n")
        for name in bleeding_keys:
             f.write(f"- {name}\n")
    
    print("Results saved to triple_check_results.txt")

if __name__ == "__main__":
    calibrate_risk()
