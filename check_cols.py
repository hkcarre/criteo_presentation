import pandas as pd

df = pd.read_csv('CASE_STUDY_CLEAN.csv', nrows=5)
print("Column names:")
for i, col in enumerate(df.columns):
    print(f"{i}: '{col}'")
