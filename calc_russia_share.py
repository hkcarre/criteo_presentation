import pandas as pd
try:
    df = pd.read_csv('c:/Dev/entrevista/CASE_STUDY_CLEAN.csv')
    df['market'] = df['market'].str.upper()
    r = df[df['market'] == 'RUSSIA']
    
    comp = r['competitor_clicks'].sum()
    criteo = r['criteo_clicks'].sum()
    share = comp / (comp + criteo) * 100
    
    print(f"Russia Comp Share: {share:.1f}%")
except Exception as e:
    print(e)
