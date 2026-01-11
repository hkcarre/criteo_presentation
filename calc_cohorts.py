import pandas as pd
import numpy as np

df = pd.read_csv('CASE_STUDY_RAW.csv', low_memory=False)
df['month'] = pd.to_datetime(df['month'])

# Filter rows with competitor activity
comp_activity = df[pd.to_numeric(df['competitor_clicks'], errors='coerce') > 0].copy()

# Get first occurrence of competitor activity for each client
first_occurrence = comp_activity.groupby('client_id')['month'].min().reset_index()
first_occurrence.columns = ['client_id', 'first_comp_month']

# Assign cohort year
first_occurrence['cohort_year'] = first_occurrence['first_comp_month'].dt.year

# Count new unique clients per month, broken down by cohort year
monthly_new_clients = first_occurrence.groupby(['first_comp_month', 'cohort_year']).size().unstack(fill_value=0)

# Reindex to ensure all months are present
all_months = pd.date_range('2022-01-01', '2024-10-01', freq='MS')
monthly_new_clients = monthly_new_clients.reindex(all_months, fill_value=0)

# Cumulative sum for each cohort
# For 2022 cohort: Accumulates during 2022, then stays constant (flat) in 2023+
# For 2023 cohort: 0 in 2022, accumulates in 2023, flat in 2024
# For 2024 cohort: 0 in 2022-23, accumulates in 2024
cumulative_cohorts = monthly_new_clients.cumsum()

# Total clients for denominator
total_clients = df['client_id'].nunique()

print('DATA_START')
years = [2022, 2023, 2024]
for year in years:
    if year in cumulative_cohorts.columns:
        series = cumulative_cohorts[year]
        # Calculate pct
        pct_series = (series / total_clients) * 100
        # Format as list string
        data_str = ','.join([f'{x:.2f}' for x in pct_series])
        print(f'Year_{year}:[{data_str}]')
    else:
        print(f'Year_{year}:[]')
print('DATA_END')
