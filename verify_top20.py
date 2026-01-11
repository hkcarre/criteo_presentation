
import json

with open('analysis_results.json', 'r') as f:
    data = json.load(f)

clients = data['q4']['top_20_clients']

print(f"Total Clients in list: {len(clients)}")

total_revenue = sum(c['revenue'] for c in clients)
total_lost = sum(c['revenue_lost'] for c in clients)

print(f"Sum of 'revenue': €{total_revenue:,.2f}")
print(f"Sum of 'revenue_lost': €{total_lost:,.2f}")

# Check if there is a whale
whales = [c for c in clients if c['revenue_lost'] > 50000000]
if whales:
    print(f"Whale found: {whales[0]['client_id']} with €{whales[0]['revenue_lost']:,.2f} lost")

# Sum excluding whale logic (if appl)
filtered_revenue = sum(c['revenue'] for c in clients if c['revenue_lost'] < 50000000)
print(f"Sum of 'revenue' (excluding >€50M lost): €{filtered_revenue:,.2f}")
