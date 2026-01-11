import pandas as pd
import sys

# Set display options to avoid truncation
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', 1000)

output_file = 'c:/Dev/entrevista/analysis_output.txt'

try:
    with open(output_file, 'w') as f:
        # Load dataset
        df = pd.read_csv('c:/Dev/entrevista/CASE_STUDY_CLEAN.csv')
        df['month'] = pd.to_datetime(df['month'])
        
        # 1. Audit Client 31782
        f.write("\n" + "="*50 + "\n")
        f.write("AUDIT: Client 31782\n")
        f.write("="*50 + "\n")
        client_df = df[df['client_id'] == 31782].sort_values('month')
        
        # Check definition: Estimated Revenue Lost = Competitor Clicks * Revenue Per Click
        headers = ["Date", "Comp Clicks", "RPC", "Est Lost (CSV)", "Calc Lost (Clicks*RPC)", "Diff", "Discrepancy?"]
        f.write(f"{headers[0]:<12} {headers[1]:<12} {headers[2]:<10} {headers[3]:<15} {headers[4]:<22} {headers[5]:<10} {headers[6]}\n")
        f.write("-" * 100 + "\n")
        
        for index, row in client_df.iterrows():
            calc_lost = row['competitor_clicks'] * row['revenue_per_click']
            diff = abs(calc_lost - row['estimated_revenue_lost'])
            is_discrepancy = "YES" if diff > 1.0 else "NO"
            
            f.write(f"{str(row['month'].date()):<12} {row['competitor_clicks']:<12} {row['revenue_per_click']:<10.2f} {row['estimated_revenue_lost']:<15.2f} {calc_lost:<22.2f} {diff:<10.2f} {is_discrepancy}\n")

        # 2. Sector Evolution (2022-2024)
        f.write("\n" + "="*50 + "\n")
        f.write("SECTOR EVOLUTION (Aggregated by Year)\n")
        f.write("="*50 + "\n")
        
        df['year'] = df['month'].dt.year
        
        # Group by Vertical and Year
        sector_trends = df.groupby(['vertical', 'year']).agg({
            'client_id': 'nunique',
            'competitor_clicks': 'sum',
            'estimated_revenue_lost': 'sum',
            'criteo_clicks': 'sum'
        }).reset_index()
        
        # Sort vertical order by total lost revenue
        top_verticals = df.groupby('vertical')['estimated_revenue_lost'].sum().nlargest(5).index.tolist()
        
        f.write(f"Top 5 Verticals by Risk: {top_verticals}\n\n")
        
        for vertical in top_verticals:
            f.write(f"--- Vertical: {vertical} ---\n")
            v_data = sector_trends[sector_trends['vertical'] == vertical]
            # Format columns for simpler reading
            f.write(v_data[['year', 'competitor_clicks', 'estimated_revenue_lost', 'criteo_clicks']].to_string(index=False))
            f.write("\n\n")

    print(f"Analysis written to {output_file}")

except Exception as e:
    print(f"Error: {e}")
