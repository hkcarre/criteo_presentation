import pandas as pd

print("--- CLEAN CSV ---")
try:
    df_clean = pd.read_csv('c:/Dev/entrevista/CASE_STUDY_CLEAN.csv')
    print(df_clean.columns.tolist())
except Exception as e:
    print(f"Error reading CLEAN: {e}")

print("\n--- RAW CSV HEADERS ---")
try:
    with open('c:/Dev/entrevista/CASE_STUDY_RAW.csv', 'r') as f:
        print(f.readline().strip())
        print(f.readline().strip())
except Exception as e:
    print(f"Error reading RAW: {e}")
