import pandas as pd
df = pd.read_csv('CASE_STUDY_RAW.csv', low_memory=False)
comp = pd.to_numeric(df['competitor_clicks'], errors='coerce')
criteo = pd.to_numeric(df['criteo_clicks'], errors='coerce')

# Oct 2023 vs Oct 2024
oct_2023 = df[df['month'] == '2023-10-01']
oct_2024 = df[df['month'] == '2024-10-01']

oct23_comp = comp[oct_2023.index].sum()
oct23_criteo = criteo[oct_2023.index].sum()
oct23_share = oct23_comp / (oct23_comp + oct23_criteo) * 100

oct24_comp = comp[oct_2024.index].sum()
oct24_criteo = criteo[oct_2024.index].sum()
oct24_share = oct24_comp / (oct24_comp + oct24_criteo) * 100

pp_change = oct24_share - oct23_share
pct_change = ((oct24_share - oct23_share) / oct23_share) * 100

print('Oct 2023 to Oct 2024 Comparison:')
print(f'Oct 2023 share: {oct23_share:.2f}%')
print(f'Oct 2024 share: {oct24_share:.2f}%')
print()
print(f'Percentage Points Change: +{pp_change:.1f} pp')
print(f'Percentage Growth: +{pct_change:.1f}%')
print()
print('For CEO Presentation:')
print(f'Option 1: "+{pp_change:.1f} pp YoY growth" (clearer)')
print(f'Option 2: "+{pct_change:.1f}% YoY growth" (traditional)')
