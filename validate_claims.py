import pandas as pd
import numpy as np

df = pd.read_csv('CASE_STUDY_RAW.csv', low_memory=False)
comp = pd.to_numeric(df['competitor_clicks'], errors='coerce')
criteo = pd.to_numeric(df['criteo_clicks'], errors='coerce')

print("=" * 60)
print("VALIDATING PRESENTATION CLAIMS AGAINST RAW DATA")
print("=" * 60)

print("\n=== 1. CRITEO SHARE BY VERTICAL ===")
print("Checking if 75%+ Criteo share in 'core Retail segments' is accurate...")
vertical_data = []
for vert in df['vertical'].dropna().unique():
    vert_mask = df['vertical'] == vert
    vert_comp = comp[vert_mask].sum()
    vert_criteo = criteo[vert_mask].sum()
    vert_total = vert_comp + vert_criteo
    if vert_total > 0:
        vert_criteo_share = vert_criteo / vert_total * 100
        vert_comp_share = vert_comp / vert_total * 100
        vertical_data.append({
            'vertical': vert,
            'criteo_share': vert_criteo_share,
            'comp_share': vert_comp_share,
            'total_clicks': vert_total
        })

vert_df = pd.DataFrame(vertical_data).sort_values('criteo_share', ascending=False)
print(vert_df.to_string())

print("\n=== 2. UNIQUE VERTICALS IN DATA ===")
print(df['vertical'].unique().tolist())

print("\n=== 3. OVERALL CRITEO SHARE ===")
total_comp = comp.sum()
total_criteo = criteo.sum()
overall_criteo_share = total_criteo / (total_comp + total_criteo) * 100
print(f"Overall Criteo share: {overall_criteo_share:.1f}%")
print(f"Overall Competitor share: {100 - overall_criteo_share:.1f}%")

print("\n=== 4. INVESTIGATING APRIL 2023 JUMP ===")
df['month_dt'] = pd.to_datetime(df['month'])
monthly = df.groupby('month').agg({
    'competitor_clicks': lambda x: pd.to_numeric(x, errors='coerce').sum(),
    'criteo_clicks': lambda x: pd.to_numeric(x, errors='coerce').sum()
})
monthly['comp_share'] = monthly['competitor_clicks'] / (monthly['competitor_clicks'] + monthly['criteo_clicks']) * 100

print("Competitor share around the jump:")
print(monthly['comp_share'].loc['2023-01-01':'2023-06-01'])

print("\n=== 5. COVID TIMING CHECK ===")
# Data starts Jan 2022, COVID restrictions mostly lifted by then
# The jump is in April 2023 - that's POST-pandemic, not during
print("Data range: Jan 2022 - Oct 2024")
print("April 2023 jump is 1.5 years AFTER COVID restrictions lifted in most of Europe")
print("COVID is unlikely to be the direct cause - more likely:")
print("  - New major competitor entered market")
print("  - UTM tracking methodology change")
print("  - Data collection improvement")
print("  - Client portfolio shift")

print("\n=== 6. DEFINING 'HIGH-VULNERABILITY SEGMENTS' ===")
# Which segments have highest competitor share?
segment_data = []
for seg in df['segment'].dropna().unique():
    seg_mask = df['segment'] == seg
    seg_comp = comp[seg_mask].sum()
    seg_criteo = criteo[seg_mask].sum()
    seg_total = seg_comp + seg_criteo
    if seg_total > 0:
        seg_comp_share = seg_comp / seg_total * 100
        segment_data.append({
            'segment': seg,
            'comp_share': seg_comp_share,
            'total_clicks': seg_total
        })

seg_df = pd.DataFrame(segment_data).sort_values('comp_share', ascending=False)
print("Segment-level competitor share:")
print(seg_df.to_string())

print("\n=== ANALYSIS COMPLETE ===")
