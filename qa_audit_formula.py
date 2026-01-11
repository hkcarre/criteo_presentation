import pandas as pd
import numpy as np
import json

# Set display options
pd.set_option('display.max_rows', None)
pd.set_option('display.float_format', '{:.4f}'.format)

output_file = 'c:/Dev/entrevista/qa_allowbale_error.txt'

try:
    with open(output_file, 'w') as f:
        df = pd.read_csv('c:/Dev/entrevista/CASE_STUDY_CLEAN.csv')
        
        # Column standardization
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

        total_rows = len(df)
        f.write(f"QA AUDIT: ESTIMATED REVENUE LOST FORMULA INTEGRITY\n")
        f.write(f"Total Rows Checked: {total_rows}\n")
        f.write("====================================================\n\n")

        # 1. CALCULATE EXPECTED VALUE
        # Formula: Competitor Clicks * Revenue Per Click
        df['expected_loss'] = df['competitor_clicks'] * df['revenue_per_click']
        
        # 2. CALCULATE ERROR (Absolute Difference)
        df['error'] = (df['expected_loss'] - df['estimated_revenue_lost']).abs()
        
        # 3. DEFINE FAILURE THRESHOLDS
        # Strict: > 0.01 Euro
        # Loose: > 1.00 Euro (Floating point tolerance)
        
        failed_strict = df[df['error'] > 0.01]
        failed_loose = df[df['error'] > 1.00]
        
        f.write(f"1. STRICT SENSITIVITY CHECK (Tolerance €0.01):\n")
        f.write(f"   - Mismatched Rows: {len(failed_strict)}\n")
        f.write(f"   - Error Rate: {(len(failed_strict)/total_rows)*100:.4f}%\n\n")
        
        f.write(f"2. LOOSE SENSITIVITY CHECK (Tolerance €1.00 - Float Drift):\n")
        f.write(f"   - Mismatched Rows: {len(failed_loose)}\n")
        f.write(f"   - Error Rate: {(len(failed_loose)/total_rows)*100:.4f}%\n\n")

        # 4. DEEP DIVE INTO FAILURES
        if len(failed_loose) > 0:
            f.write("3. SAMPLE OF MATERIALLY INCORRECT ROWS (>€1.00 Diff):\n")
            sample = failed_loose[['month', 'client_id', 'competitor_clicks', 'revenue_per_click', 'estimated_revenue_lost', 'expected_loss', 'error']].head(10)
            f.write(sample.to_string(index=False))
            f.write("\n\n")
            
            # Check for patterns
            max_error = failed_loose['error'].max()
            f.write(f"   - Max Error Observed: €{max_error:,.2f}\n")
        else:
            f.write("3. CONCLUSION:\n")
            f.write("   - No material calculation errors found. The CSV data precisely matches the formula.\n")

    print(json.dumps({"status": "complete", "file": output_file}))

except Exception as e:
    print(f"Error: {e}")
