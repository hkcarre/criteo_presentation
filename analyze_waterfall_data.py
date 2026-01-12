
import pandas as pd

def analyze_waterfall():
    print("Loading data...")
    # Load the recalculated dataset which is the source of truth
    df = pd.read_csv('c:/Dev/entrevista/CASE_STUDY_RECALCULATED.csv')
    
    # 1. Total Universe (All Revenue)
    total_revenue = df['revenue_euro'].sum()
    
    # 2. Exposed Revenue (Revenue of clients where Competitor Clicks > 0)
    # This represents the "Gross Risk"
    exposed_mask = df['competitor_clicks'] > 0
    exposed_revenue = df[exposed_mask]['revenue_euro'].sum()
    
    # 3. High Risk / Bleeding (Revenue in "CRITICAL" segments: Identity, Russia, SE Europe?)
    # Let's use the definition of "Bleeding" from previous steps (Southern/Eastern Europe)
    # or arguably, we can use the "High Risk" clients.
    # User asked for "Revenue Exposed" -> "Estimated Revenue Loss"
    # Let's look at the intermediate step. Maybe "High Probability Risk"?
    # For now, let's get the 'estimated_revenue_lost' sum.
    
    # Check if 'estimated_revenue_lost' exists and is numeric
    # If not, we might need to calculate it or look for a similar column
    # The user mentioned "estimated revenue loss metric".
    
    col_loss = [c for c in df.columns if 'loss' in c.lower() or 'lost' in c.lower()]
    print(f"Loss columns found: {col_loss}")
    
    est_loss_sum = 0
    if col_loss:
        # distinct name 'estimated_revenue_lost'
        target_col = col_loss[0]
        est_loss_sum = df[target_col].sum()
    
    print(f"\n--- WATERFALL DATA ---")
    print(f"1. Total Annual Revenue (Base): €{total_revenue:,.0f}")
    print(f"2. Gross Exposed Revenue (Competitor Presense): €{exposed_revenue:,.0f}")
    print(f"   (% of Total: {exposed_revenue/total_revenue:.1%})")
    
    # Let's try to find a meaningful intermediate step if possible.
    # Maybe "Top 20 Whales" portion of Exposed?
    whales_revenue = df.groupby('client_id')['revenue_euro'].sum().nlargest(20).sum()
    print(f"   (Top 20 Whales Revenue: €{whales_revenue:,.0f})")

    print(f"3. Estimated Revenue Loss (Metric): €{est_loss_sum:,.0f}")
    print(f"   (% of Exposed: {est_loss_sum/exposed_revenue:.1%})")

if __name__ == "__main__":
    analyze_waterfall()
