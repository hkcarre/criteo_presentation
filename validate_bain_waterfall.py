
import pandas as pd
import numpy as np

def validate_bain_logic():
    print("Loading data...")
    df = pd.read_csv('c:/Dev/entrevista/CASE_STUDY_RECALCULATED.csv', parse_dates=['month'])
    
    # Ensure RPC and Est Loss are calculated
    if 'RPC' not in df.columns:
         df['RPC'] = df['revenue_euro'] / df['Corrected_Criteo_Clicks'].replace(0, 1)
    if 'estimated_revenue_lost' not in df.columns:
        df['estimated_revenue_lost'] = df['competitor_clicks'] * df['RPC']

    # 1. REVENUE ANNUALIZATION (2024)
    df_2024 = df[df['month'].dt.year == 2024]
    months_count = df_2024['month'].nunique() # Should be 10 (Jan-Oct)
    
    rev_2024_raw = df_2024['revenue_euro'].sum()
    rev_2024_annualized = (rev_2024_raw / months_count) * 12
    
    print(f"\n--- 1. REVENUE ANNUALIZATION ---")
    print(f"Months Data: {months_count}")
    print(f"Raw 2024 Rev: €{rev_2024_raw:,.0f}")
    print(f"Annualized:   €{rev_2024_annualized:,.0f}")
    
    # 2. GEO REVENUE SPLIT (2024 Annualized Basis)
    # We use 2024 distribution
    geo_rev = df_2024.groupby('market')['revenue_euro'].sum()
    geo_share = (geo_rev / rev_2024_raw) * 100
    
    print(f"\n--- 2. GEO SPLIT (2024) ---")
    for market, share in geo_share.sort_values(ascending=False).items():
        print(f"{market:<15} {share:.1f}%")

    # 3. CLIENT SEGMENTATION
    # "Contested" = Competitor Clicks > 0
    # We look at the CLIENT level (aggregating all months)
    client_totals = df.groupby('client_id').agg({
        'competitor_clicks': 'sum',
        'revenue_euro': 'sum'
    })
    
    total_clients = len(client_totals)
    uncontested = client_totals[client_totals['competitor_clicks'] == 0]
    contested = client_totals[client_totals['competitor_clicks'] > 0]
    
    print(f"\n--- 3. CLIENT SEGMENTATION ---")
    print(f"Total Clients: {total_clients}")
    print(f"Uncontested:   {len(uncontested)} ({len(uncontested)/total_clients:.1%}) - Rev Share: {(uncontested['revenue_euro'].sum()/client_totals['revenue_euro'].sum()):.1%}")
    print(f"Contested:     {len(contested)} ({len(contested)/total_clients:.1%}) - Rev Share: {(contested['revenue_euro'].sum()/client_totals['revenue_euro'].sum()):.1%}")

    # 4. €132M RECONCILIATION & OVERLAP
    # Component A: Bleeding Geos (ES, IT, EE)
    bleeding_markets = ['IBERIA', 'ITALY', 'EASTERN EUROPE'] # 'SPAIN' is likely IBERIA
    df_bleeding = df_2024[df_2024['market'].isin(bleeding_markets)]
    
    # Calculate "Risk" in Bleeding Markets
    # Bain asks: Is it €92.5M?
    # Use Estimated Loss for 2024 annualization
    loss_bleeding_raw = df_bleeding['estimated_revenue_lost'].sum()
    loss_bleeding_annual = (loss_bleeding_raw / months_count) * 12
    
    print(f"\n--- 4. BLEEDING MARKETS CHECK ---")
    print(f"Bleeding Mkts ({bleeding_markets}) Used: €{loss_bleeding_annual:,.0f} (Target: €92.5M)")
    
    # Component B: Whales (Top 20 by Risk)
    # We need to identify Top 20 Risk Clients GLOBAL
    client_risk_2024 = df_2024.groupby('client_id')['estimated_revenue_lost'].sum()
    top_20_risk_ids = client_risk_2024.nlargest(20).index
    
    loss_whales_raw = client_risk_2024.loc[top_20_risk_ids].sum()
    loss_whales_annual = (loss_whales_raw / months_count) * 12
    
    print(f"\n--- 5. WHALE CHECK ---")
    print(f"Top 20 Whales Risk: €{loss_whales_annual:,.0f} (Target: €39.5M)")
    
    # OVERLAP CHECK
    # Identify Whales that are ALSO in Bleeding Markets
    # Get Market for each Whale
    whale_info = df_2024[df_2024['client_id'].isin(top_20_risk_ids)][['client_id', 'market']].drop_duplicates()
    
    overlap_whales = whale_info[whale_info['market'].isin(bleeding_markets)]
    overlap_ids = overlap_whales['client_id'].unique()
    
    print(f"\n--- 6. OVERLAP / DOUBLE COUNTING ---")
    print(f"Whales in Bleeding Geos: {len(overlap_ids)}")
    if len(overlap_ids) > 0:
        overlap_loss = client_risk_2024.loc[overlap_ids].sum()
        overlap_annual = (overlap_loss / months_count) * 12
        print(f"Overlap Value: €{overlap_annual:,.0f}")
        print(f"Corrected Total: €{(loss_bleeding_annual + loss_whales_annual - overlap_annual):,.0f}")
    else:
        print("No Overlap. Sum is valid.")
        print(f"Total Risk: €{(loss_bleeding_annual + loss_whales_annual):,.0f}")

    with open('c:/Dev/entrevista/bain_validation_results.txt', 'w') as f:
        f.write(f"Annualized Rev: {rev_2024_annualized}\n")
        f.write(f"Bleeding Geo Risk: {loss_bleeding_annual}\n")
        f.write(f"Whale Risk: {loss_whales_annual}\n")
        overlap_val = overlap_annual if len(overlap_ids) > 0 else 0
        f.write(f"Overlap: {overlap_val}\n")
        f.write(f"Deduplicated Risk: {loss_bleeding_annual + loss_whales_annual - overlap_val}\n")

if __name__ == "__main__":
    validate_bain_logic()
