import pandas as pd
df = pd.read_csv('CASE_STUDY_RAW.csv', low_memory=False)
df['month'] = pd.to_datetime(df['month'])
# Filter rows with competitor activity
comp_activity = df[pd.to_numeric(df['competitor_clicks'], errors='coerce') > 0].copy()
# Get first occurrence of competitor activity for each client
first_occurrence = comp_activity.groupby('client_id')['month'].min().reset_index()
first_occurrence.columns = ['client_id', 'first_comp_month']
# Count new unique clients per month
monthly_new_clients = first_occurrence.groupby('first_comp_month').size()
# Reindex
all_months = pd.date_range('2022-01-01', '2024-10-01', freq='MS')
monthly_new_clients = monthly_new_clients.reindex(all_months, fill_value=0)
# Cumulative
cumulative_clients = monthly_new_clients.cumsum()
total_clients = df['client_id'].nunique()
print('DATA_START')
print('[')
rows = []
for date, count in cumulative_clients.items():
    pct = (count / total_clients) * 100
    rows.append(f'{pct:.2f}')
print(','.join(rows))
print(']')
