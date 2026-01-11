import pandas as pd
import numpy as np

# Set display options
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', 1000)
pd.set_option('display.float_format', '{:.2f}'.format) # Clean float formatting

output_file = 'c:/Dev/entrevista/data_quality_report.txt'

try:
    with open(output_file, 'w') as f:
        df = pd.read_csv('c:/Dev/entrevista/CASE_STUDY_CLEAN.csv')
        
        # Dynamic renaming to be safe from previous step
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

        df['month'] = pd.to_datetime(df['month'])
        df['year'] = df['month'].dt.year
        
        # REMCVE INF VALUES
        df.replace([np.inf, -np.inf], np.nan, inplace=True)

        f.write("DATA QUALITY & RE-CALCULATION REPORT (CLEANED)\n")
        f.write("===============================================\n\n")

        # --- 2. RE-CALCULATION LOGIC ("The Correction") ---
        # 1. Calculate 'Stable RPC' (Median of months where RPC > 0.1)
        client_rpc = df[df['revenue_per_click'] > 0.1].groupby('client_id')['revenue_per_click'].median().reset_index()
        client_rpc.rename(columns={'revenue_per_click': 'stable_rpc'}, inplace=True)
        
        # 2. Merge back
        df = df.merge(client_rpc, on='client_id', how='left')
        
        # 3. Fill missing with Sector Median
        sector_rpc = df[df['revenue_per_click'] > 0.1].groupby('vertical')['revenue_per_click'].median().reset_index()
        sector_rpc.rename(columns={'revenue_per_click': 'sector_rpc'}, inplace=True)
        df = df.merge(sector_rpc, on='vertical', how='left')
        df['stable_rpc'].fillna(df['sector_rpc'], inplace=True)
        df['stable_rpc'].fillna(0, inplace=True) 

        # 4. Calculate CORRECTED Lost Revenue
        df['corrected_revenue_lost'] = df['competitor_clicks'] * df['stable_rpc']
        
        # 5. Measure the 'Hidden Loss' (Gap vs Original Estimate)
        df['hidden_loss'] = df['corrected_revenue_lost'] - df['estimated_revenue_lost']

        # --- 3. TOP IMPACTED CLIENTS ---
        f.write("2. TOP 10 CLIENTS WITH HIDDEN REVENUE LOSS:\n")
        client_impact = df.groupby('client_id').agg({
            'hidden_loss': 'sum',
            'estimated_revenue_lost': 'sum',
            'corrected_revenue_lost': 'sum',
            'vertical': 'first'
        }).sort_values('hidden_loss', ascending=False).head(10)
        
        f.write(client_impact.to_string())
        f.write("\n\n")

        # Check Client 31782 specifically
        f.write("3. CLIENT 31782 SPECIFIC CHECK:\n")
        c31782 = client_impact[client_impact.index == 31782]
        if not c31782.empty:
            f.write(c31782.to_string())
        else:
             c31782_full = df[df['client_id'] == 31782].agg({
                'hidden_loss': 'sum',
                'estimated_revenue_lost': 'sum',
                'corrected_revenue_lost': 'sum'
            })
             f.write(str(c31782_full))
        f.write("\n\n")

        # --- 4. SECTOR IMPACT (Re-evaluated) ---
        f.write("4. SECTOR RISK RE-EVALUATION (2024 Only):\n")
        df_2024 = df[df['year'] == 2024]
        sector_impact = df_2024.groupby('vertical').agg({
            'estimated_revenue_lost': 'sum',
            'corrected_revenue_lost': 'sum',
            'hidden_loss': 'sum'
        }).sort_values('corrected_revenue_lost', ascending=False)
        
        f.write(sector_impact.to_string())
        f.write("\n\n")

    print(f"Report written to {output_file}")

except Exception as e:
    print(f"Error: {e}")
