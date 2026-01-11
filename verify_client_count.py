import pandas as pd

try:
    df = pd.read_csv('c:/Dev/entrevista/CASE_STUDY_CLEAN.csv')
    print("Columns:", df.columns.tolist())
    
    total_unique_clients = df['client_id'].nunique()
    print(f"Total Unique Clients: {total_unique_clients}")
    
    if 'competitor_clicks' in df.columns:
        impacted_clients = df[df['competitor_clicks'] > 0]['client_id'].nunique()
        print(f"Impacted Clients (competitor_clicks > 0): {impacted_clients}")
        
        if total_unique_clients > 0:
            penetration = (impacted_clients / total_unique_clients) * 100
            print(f"Calculated Penetration: {penetration:.2f}%")
            
except Exception as e:
    print(f"Error: {e}")
