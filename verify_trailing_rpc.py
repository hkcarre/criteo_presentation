import pandas as pd

# Load dataset
df = pd.read_csv('c:/Dev/entrevista/CASE_STUDY_CLEAN.csv')
df['month'] = pd.to_datetime(df['month'])

# Dynamic column renaming (safety first)
col_map = {c: c.lower() for c in df.columns}
if 'revenue_in_euros' in col_map:
     df.rename(columns={'revenue_in_euros': 'revenue'}, inplace=True)
elif 'revenue (in euros)' in col_map:
     df.rename(columns={'revenue (in euros)': 'revenue'}, inplace=True)
if 'revenue' not in df.columns:
     for c in df.columns:
         if 'revenue' in c and 'lost' not in c and 'click' not in c:
             df.rename(columns={c: 'revenue'}, inplace=True)
             break

# Filter for Client 31782
client_df = df[df['client_id'] == 31782].sort_values('month')

print("\n=== VERIFICATION: Client 31782 (April 2024) ===")

# 1. Get April 2024 Data (The "Nuisance" Month)
april_2024 = client_df[client_df['month'] == '2024-04-01'].iloc[0]
print(f"Date: {april_2024['month'].date()}")
print(f"Reported Est. Revenue Lost: €{april_2024['estimated_revenue_lost']:,.2f}")
print(f"Current Month RPC: €{april_2024['revenue_per_click']:.2f}")
print(f"Competitor Clicks: {april_2024['competitor_clicks']:,.0f}")

# 2. Calculate Trailing 12-Month RPC (Apr 2023 - Mar 2024)
# We want the average RPC of the *previous* 12 months to avoid the churn drop.
start_date = '2023-04-01'
end_date = '2024-03-31'
trailing_data = client_df[(client_df['month'] >= start_date) & (client_df['month'] <= end_date)]

# Filter out "Zero/Low" RPC artifacts if any (though trailing usually has valid data)
valid_trailing = trailing_data[trailing_data['revenue_per_click'] > 1.0]

avg_trailing_rpc = valid_trailing['revenue_per_click'].mean()
median_trailing_rpc = valid_trailing['revenue_per_click'].median()

print(f"\n--- TRILING 12-MONTH DATA ({start_date} to {end_date}) ---")
print(f"Months with Valid Data: {len(valid_trailing)}")
print(f"Average Trailing RPC: €{avg_trailing_rpc:.2f}")
print(f"Median Trailing RPC: €{median_trailing_rpc:.2f}")

# 3. Recalculate Risk
recalc_risk_avg = april_2024['competitor_clicks'] * avg_trailing_rpc
recalc_risk_median = april_2024['competitor_clicks'] * median_trailing_rpc


output_str = ""
output_str += f"\n--- RECALCULATION ---\n"
output_str += f"Scenario A (Avg RPC * Clicks): €{recalc_risk_avg:,.2f}\n"
output_str += f"Scenario B (Median RPC * Clicks): €{recalc_risk_median:,.2f}\n"

if recalc_risk_avg > 150000000:
    output_str += "\n>>> CONFIRMED: Risk is > €150M using Trailing RPC. <<<\n"
else:
    output_str += "\n>>> RESULT: Risk is lower than expected. Check assumptions. <<<\n"

with open('c:/Dev/entrevista/verify_loss_output.txt', 'w') as f:
    f.write(output_str)
print("Written to c:/Dev/entrevista/verify_loss_output.txt")
