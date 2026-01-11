import pandas as pd

# Load Data
try:
    df = pd.read_csv('c:/Dev/entrevista/CASE_STUDY_CLEAN.csv')
except:
    df = pd.read_csv('c:/Dev/entrevista/CASE_STUDY_CLEAN.csv', sep=';')

# Clean columns
df.columns = [c.strip().lower().replace(' ', '_').replace('.', '') for c in df.columns]

# Index Mapping
try:
    df.rename(columns={
        df.columns[6]: 'revenue',
        df.columns[7]: 'competitor_clicks',
        df.columns[8]: 'criteo_clicks'
    }, inplace=True)
except:
    pass
    
clicks_col = 'criteo_clicks'
comp_clicks_col = 'competitor_clicks'

# Filter Russia 2024
df['month'] = pd.to_datetime(df['month'])
russia_24 = df[(df['market'] == 'RUSSIA') & (df['month'].dt.year == 2024)]

total_criteo = russia_24[clicks_col].sum()
total_comp = russia_24[comp_clicks_col].sum()

if (total_criteo + total_comp) > 0:
    click_share = total_comp / (total_criteo + total_comp) * 100
else:
    click_share = 0

print(f"RUSSIA 2024 STATS:")
print(f"Criteo Clicks: {total_criteo:,.0f}")
print(f"Competitor Clicks: {total_comp:,.0f}")
print(f"Competitor Click Share: {click_share:.2f}%")

# Detection Rate (Frequency)
rows_with_comp = len(russia_24[russia_24[comp_clicks_col] > 0])
total_rows = len(russia_24)
print(f"Detection Rate (Rows with Comp > 0): {rows_with_comp}/{total_rows} ({rows_with_comp/total_rows*100:.2f}%)")
