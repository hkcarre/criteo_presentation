import pandas as pd
import numpy as np

pd.options.mode.chained_assignment = None  # default='warn'

def clean_currency(x):
    if isinstance(x, str):
        return float(x.replace('€', '').replace(',', '').strip())
    return float(x)

def calculate_pareto(df, group_name="Global"):
    if df.empty:
        return {}
    
    # Aggregating by Client ID to get total revenue per client
    client_revenue = df.groupby('client_id')['revenue'].sum().sort_values(ascending=False)
    total_revenue = client_revenue.sum()
    total_clients = len(client_revenue)
    
    if total_revenue == 0:
         return {
            "Group": group_name,
            "Total_Rev": 0,
            "Total_Clients": total_clients,
            "Top_1%_Share": 0,
            "Top_5%_Share": 0,
            "Top_10%_Share": 0,
            "Top_20%_Share": 0
        }

    # Cumulative Revenue
    cumsum_revenue = client_revenue.cumsum()
    
    # Percentiles
    top_1_idx = int(total_clients * 0.01)
    top_5_idx = int(total_clients * 0.05)
    top_10_idx = int(total_clients * 0.10)
    top_20_idx = int(total_clients * 0.20)
    
    # Handling small N cases
    top_1_idx = max(1, top_1_idx)
    top_5_idx = max(1, top_5_idx)
    top_10_idx = max(1, top_10_idx)
    top_20_idx = max(1, top_20_idx)

    return {
        "Group": group_name,
        "Total_Rev": total_revenue,
        "Total_Clients": total_clients,
        "Top_1%_Share": (cumsum_revenue.iloc[top_1_idx-1] / total_revenue) * 100,
        "Top_5%_Share": (cumsum_revenue.iloc[top_5_idx-1] / total_revenue) * 100,
        "Top_10%_Share": (cumsum_revenue.iloc[top_10_idx-1] / total_revenue) * 100,
        "Top_20%_Share": (cumsum_revenue.iloc[top_20_idx-1] / total_revenue) * 100
    }

try:
    print("Loading Data from RAW...")
    df = pd.read_csv('c:/Dev/entrevista/CASE_STUDY_RAW.csv', sep=',')
    
    # Standardize columns
    df.columns = [c.strip().lower().replace(' ', '_') for c in df.columns]
    
    # Convert Date
    df['month'] = pd.to_datetime(df['month'])
    df['year'] = df['month'].dt.year
    print(f"Columns: {df.columns.tolist()}")

    # Rename revenue column if needed
    if 'revenue' not in df.columns:
        if 'revenue_in_euros' in df.columns:
            df.rename(columns={'revenue_in_euros': 'revenue'}, inplace=True)
        elif 'revenue_per_click' in df.columns and 'criteo_clicks' in df.columns:
             print("Constructing Revenue from Clicks * RPC")
             df['revenue_per_click'] = df['revenue_per_click'].apply(clean_currency)
             df['criteo_clicks'] = df['criteo_clicks'].apply(lambda x: float(str(x).replace(',', '.')) if isinstance(x, str) else x)
             df['revenue'] = df['criteo_clicks'] * df['revenue_per_click']
        else:
            raise ValueError(f"Revenue column not found. Available: {df.columns.tolist()}")

    # Clean Revenue
    if df['revenue'].dtype == object:
        df['revenue'] = df['revenue'].apply(clean_currency)

    # 1. YEARLY GLOBAL PARETO
    print("\n--- GLOBAL PARETO BY YEAR ---")
    years = sorted(df['year'].unique())
    results = []
    for year in years:
        df_year = df[df['year'] == year]
        res = calculate_pareto(df_year, f"Year {year}")
        results.append(res)
    
    res_df = pd.DataFrame(results)
    print(res_df.to_string(index=False, float_format="%.2f"))

    # STOP HERE FOR NOW
    exit()

except Exception as e:
    print(f"Error: {e}")
