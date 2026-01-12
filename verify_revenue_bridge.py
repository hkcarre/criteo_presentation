
import pandas as pd

def verify_data_bridge():
    df = pd.read_csv('c:/Dev/entrevista/CASE_STUDY_RECALCULATED.csv')
    
    print("--- REVENUE BRIDGE VERIFICATION ---")
    
    # 1. Total Revenue
    total_revenue = df['revenue_euro'].sum()
    print(f"Total Revenue: €{total_revenue:,.2f}")
    
    # 2. Bleeding Revenue (Markets with negative correlation or high risk)
    # Based on previous analysis: Italy, Spain, Eastern Europe, Russia
    bleeding_markets = ['ITALY', 'SPAIN', 'EASTERN EUROPE', 'RUSSIA'] # Check precise names
    risky_markets = df[df['market'].isin(['ITALY', 'IBERIA', 'EASTERN EUROPE', 'RUSSIA'])] # 'IBERIA' likely covers Spain
    bleeding_revenue = risky_markets['revenue_euro'].sum()
    print(f"Bleeding Revenue (Southern/Eastern Europe): €{bleeding_revenue:,.2f}")
    
    # 3. Whale Risk (Top 20 Clients)
    top_20 = df.groupby('client_id')['revenue_euro'].sum().nlargest(20)
    top_20_rev = top_20.sum()
    print(f"Top 20 Whales Total Revenue: €{top_20_rev:,.2f}")
    
    # Check the specific "Risk" vs "Total Revenue"
    # The €39.5M figure in the deck might be 'Revenue at Risk' (e.g. Total Rev * Competitor Share)
    # OR it might be the revenue of the Top 20 *Threatened* clients.
    
    # Let's find the clients with Active Threat
    # Threat = Competitor Clicks > 0
    threatened = df[df['competitor_clicks'] > 0]
    top_20_threatened = threatened.groupby('client_id')['revenue_euro'].sum().nlargest(20)
    top_20_threat_rev = top_20_threatened.sum()
    print(f"Top 20 *Threatened* Whales Revenue: €{top_20_threat_rev:,.2f}")
    
    # 4. Client A Anomaly
    # Find max client revenue
    top_client = df.groupby('client_id')['revenue_euro'].sum().nlargest(1)
    print(f"\n--- CLIENT A CHECK ---")
    print(f"Top Client ID: {top_client.index[0]}")
    print(f"Top Client Annual Revenue: €{top_client.values[0]:,.2f}")
    
    # Check Monthly Peak for Top Client
    top_client_id = top_client.index[0]
    client_a_data = df[df['client_id'] == top_client_id]
    peak_month = client_a_data.groupby('month')['revenue_euro'].sum().max()
    print(f"Top Client Peak Month Revenue: €{peak_month:,.2f}")

    # 5. Efficiency Trap (10/84 Split)
    # Check Pareto
    total_clients = df['client_id'].nunique()
    top_10_count = int(total_clients * 0.1)
    
    client_revs = df.groupby('client_id')['revenue_euro'].sum().sort_values(ascending=False)
    top_10_rev_sum = client_revs.head(top_10_count).sum()
    share_of_wallet = top_10_rev_sum / total_revenue
    
    print(f"\n--- EFFICIENCY TRAP CHECK ---")
    print(f"Total Clients: {total_clients}")
    print(f"Top 10% Count: {top_10_count}")
    print(f"Top 10% Revenue: €{top_10_rev_sum:,.2f}")
    print(f"Top 10% Share: {share_of_wallet:.1%}")

if __name__ == "__main__":
    verify_data_bridge()
