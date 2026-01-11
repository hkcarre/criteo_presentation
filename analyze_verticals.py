
import pandas as pd

file_path = r"c:\Dev\entrevista\CASE_STUDY_CLEAN.csv"

# Load the data
df = pd.read_csv(file_path)

# Filter for the relevant period (optional, but good practice to match the analysis window if needed) or use all data
# The previous analysis mentioned "Jan 2022 – Oct 2024"

# 1. Total Revenue
total_revenue = df['revenue_euro'].sum()

# 2. Group by Vertical
vertical_stats = df.groupby('vertical').agg({
    'revenue_euro': 'sum',
    'competitor_clicks': 'sum',
    'criteo_clicks': 'sum'
}).reset_index()

# 3. Calculate Metrics
vertical_stats['revenue_share'] = (vertical_stats['revenue_euro'] / total_revenue) * 100
# Competitor Share of Clicks = Competitor Clicks / (Competitor Clicks + Criteo Clicks)
vertical_stats['competitor_click_share'] = (vertical_stats['competitor_clicks'] / (vertical_stats['competitor_clicks'] + vertical_stats['criteo_clicks'])) * 100

print(f"Total Revenue: €{total_revenue:,.2f}\n")
print("Vertical Analysis:")
# Deep dive into "Travel" and "Classifieds" specifically if they contain those strings
print("\n--- Specific Vertical Checks ---")
for v in ["Travel", "Classifieds"]:
    # Case-insensitive match just in case
    match = vertical_stats[vertical_stats['vertical'].str.contains(v, case=False, na=False)]
    if not match.empty:
        print(f"\nVertical: {v}")
        for idx, row in match.iterrows():
            print(f"  Revenue: €{row['revenue_euro']:,.2f}")
            print(f"  Revenue Share: {row['revenue_share']:.2f}%")
            print(f"  Competitor Share: {row['competitor_click_share']:.2f}%")
    else:
        print(f"Vertical '{v}' not found.")
