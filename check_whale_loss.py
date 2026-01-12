
import pandas as pd

def check_whale_loss():
    print("Loading data...")
    df = pd.read_csv('c:/Dev/entrevista/CASE_STUDY_RECALCULATED.csv')
    
    # Recalculate Estimated Loss
    if 'RPC' not in df.columns:
         df['RPC'] = df['revenue_euro'] / df['Corrected_Criteo_Clicks'].replace(0, 1)
    df['estimated_revenue_lost'] = df['competitor_clicks'] * df['RPC']
    
    # 1. Client A Check (Travel, Top Peak)
    # Finding Client A: Max Peak Monthly Revenue?
    # Or just grouping by client_id
    client_annual = df.groupby('client_id')['revenue_euro'].sum()
    top_client_id = client_annual.idxmax()
    client_a = df[df['client_id'] == top_client_id]
    
    client_a_rev = client_a['revenue_euro'].sum()
    client_a_loss = client_a['estimated_revenue_lost'].sum()
    
    print(f"\n--- CLIENT A ({top_client_id}) ---")
    print(f"Annual Revenue: €{client_a_rev:,.0f}")
    print(f"Est. Rev Loss:  €{client_a_loss:,.0f}")
    
    # 2. Top 20 Whales by RISK (Estimated Loss)
    top_20_risk_idx = df.groupby('client_id')['estimated_revenue_lost'].sum().nlargest(20).index
    top_20_risk = df[df['client_id'].isin(top_20_risk_idx)]
    
    risk_val = top_20_risk['estimated_revenue_lost'].sum()
    rev_val = top_20_risk['revenue_euro'].sum()
    
    print(f"\n--- TOP 20 RISK WHALES ---")
    print(f"Combined Annual Rev:  €{rev_val:,.0f}")
    print(f"Combined Est Loss:    €{risk_val:,.0f}")
    
    # 3. Top 20 Whales by REVENUE (The 'Fortress' Whales)
    top_20_rev_idx = client_annual.nlargest(20).index
    top_20_rev = df[df['client_id'].isin(top_20_rev_idx)]
    
    rev_risk_val = top_20_rev['estimated_revenue_lost'].sum()
    rev_rev_val = top_20_rev['revenue_euro'].sum()
    
    print(f"\n--- TOP 20 REVENUE WHALES ---")
    print(f"Combined Annual Rev:  €{rev_rev_val:,.0f}")
    print(f"Combined Est Loss:    €{rev_risk_val:,.0f}")

    with open('c:/Dev/entrevista/whale_check_results.txt', 'w') as f:
        f.write(f"Client A Loss: {client_a_loss}\n")
        f.write(f"Top 20 Risk Loss: {risk_val}\n")
        f.write(f"Top 20 Rev Revenue: {rev_rev_val}\n") # This is the €19.5M? No €19.5M was Recoverable?

if __name__ == "__main__":
    check_whale_loss()
