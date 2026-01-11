
import pandas as pd

def verify_logic():
    df = pd.read_csv('c:/Dev/entrevista/CASE_STUDY_RECALCULATED.csv')
    
    # Filter for imputed rows
    imputed = df[df['Imputation_Flag'] == True]
    
    print(f"Total Imputed Rows: {len(imputed)}")
    
    # Check if RPC is 0 (Zeroed Out) or > 0 (Calculated)
    zeros = imputed[imputed['RPC'] == 0]
    calculated = imputed[imputed['RPC'] > 0]
    
    print(f"Rows with RPC = 0 (Zeroed Out): {len(zeros)}")
    print(f"Rows with RPC > 0 (Calculated): {len(calculated)}")
    
    if len(calculated) > 0:
        sample = calculated.iloc[0]
        print(f"\nSample Row:")
        print(f"Revenue: {sample['revenue_euro']}") # Adjust column name if needed based on previous steps
        print(f"Corrected Clicks: {sample['Corrected_Criteo_Clicks']}")
        print(f"RPC: {sample['RPC']}")
        rec_calc = sample['revenue_euro'] / sample['Corrected_Criteo_Clicks']
        print(f"Manual Calc check: {rec_calc:.2f}")

if __name__ == "__main__":
    verify_logic()
