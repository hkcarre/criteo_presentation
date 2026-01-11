import pandas as pd
import numpy as np

# Load the data
df = pd.read_csv('CASE_STUDY_RAW.csv')

print("="*80)
print("DATA OVERVIEW")
print("="*80)
print(f"\nShape: {df.shape}")
print(f"\nColumns: {df.columns.tolist()}")
print(f"\nData types:\n{df.dtypes}")

print("\n" + "="*80)
print("FIRST 20 ROWS")
print("="*80)
print(df.head(20))

print("\n" + "="*80)
print("BASIC STATISTICS")
print("="*80)
print(df.describe())

print("\n" + "="*80)
print("NULL VALUES")
print("="*80)
print(df.isnull().sum())

print("\n" + "="*80)
print("UNIQUE VALUES")
print("="*80)
for col in df.columns:
    print(f"{col}: {df[col].nunique()} unique values")

if 'month' in df.columns:
    print(f"\nDate range: {df['month'].min()} to {df['month'].max()}")
if 'Market' in df.columns:
    print(f"\nMarkets: {df['Market'].unique()}")
if 'Vertical' in df.columns:
    print(f"\nVerticals: {df['Vertical'].unique()}")
if 'Segment' in df.columns:
    print(f"\nSegments: {df['Segment'].unique()}")
