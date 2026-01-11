import pandas as pd
import numpy as np
from scipy import stats

df = pd.read_csv('CASE_STUDY_RAW.csv', low_memory=False)

# Convert to numeric
revenue = pd.to_numeric(df['revenue_euro'], errors='coerce')
criteo_clicks = pd.to_numeric(df['criteo_clicks'], errors='coerce')
comp_clicks = pd.to_numeric(df['competitor_clicks'], errors='coerce')
rpc = pd.to_numeric(df['revenue_per_click'], errors='coerce')

print("=" * 70)
print("STATISTICAL CORRELATION ANALYSIS: REVENUE vs CLICKS")
print("Senior Data Scientist Deep-Dive")
print("=" * 70)

# Filter to non-zero values for meaningful analysis
valid_mask = (revenue > 0) & (criteo_clicks > 0)
rev_valid = revenue[valid_mask]
clicks_valid = criteo_clicks[valid_mask]

print(f"\n=== 1. DATA OVERVIEW ===")
print(f"Total records: {len(df):,}")
print(f"Records with revenue > 0 AND clicks > 0: {valid_mask.sum():,} ({valid_mask.sum()/len(df)*100:.1f}%)")
print(f"Records excluded (zero revenue or zero clicks): {(~valid_mask).sum():,}")

print(f"\n=== 2. PEARSON CORRELATION: Revenue vs Criteo Clicks ===")
# Pearson correlation (linear relationship)
pearson_r, pearson_p = stats.pearsonr(clicks_valid, rev_valid)
print(f"Pearson r: {pearson_r:.4f}")
print(f"P-value: {pearson_p:.2e}")
print(f"R-squared: {pearson_r**2:.4f}")
print(f"Interpretation: {'Strong' if abs(pearson_r) > 0.7 else 'Moderate' if abs(pearson_r) > 0.4 else 'Weak'} "
      f"{'positive' if pearson_r > 0 else 'negative'} linear correlation")

print(f"\n=== 3. SPEARMAN CORRELATION (Rank-based, robust to outliers) ===")
spearman_r, spearman_p = stats.spearmanr(clicks_valid, rev_valid)
print(f"Spearman rho: {spearman_r:.4f}")
print(f"P-value: {spearman_p:.2e}")
print(f"Interpretation: {'Strong' if abs(spearman_r) > 0.7 else 'Moderate' if abs(spearman_r) > 0.4 else 'Weak'} "
      f"monotonic relationship")

print(f"\n=== 4. LINEAR REGRESSION: Revenue = a + b x Criteo_Clicks ===")
slope, intercept, r_value, p_value, std_err = stats.linregress(clicks_valid, rev_valid)
print(f"Slope (b): {slope:.4f} EUR per click")
print(f"Intercept (a): {intercept:.2f} EUR")
print(f"R-squared: {r_value**2:.4f}")
print(f"Standard Error: {std_err:.4f}")
print(f"P-value: {p_value:.2e}")
print(f"\nModel: Revenue = {intercept:.2f} + {slope:.4f} × Clicks")
print(f"Meaning: Each additional Criteo click is associated with €{slope:.4f} in revenue")

print(f"\n=== 5. REVENUE PER CLICK (RPC) ANALYSIS ===")
rpc_valid = rpc[rpc > 0]
print(f"RPC statistics (non-zero values only):")
print(f"  Mean RPC: €{rpc_valid.mean():.4f}")
print(f"  Median RPC: €{rpc_valid.median():.4f}")
print(f"  Std Dev: €{rpc_valid.std():.4f}")
print(f"  Min: €{rpc_valid.min():.4f}")
print(f"  Max: €{rpc_valid.max():.4f}")
print(f"  CV (Coefficient of Variation): {rpc_valid.std() / rpc_valid.mean() * 100:.1f}%")

print(f"\n=== 6. CLICK SHARE vs REVENUE RELATIONSHIP ===")
# Calculate monthly aggregates for time-series correlation
monthly = df.groupby('month').agg({
    'revenue_euro': lambda x: pd.to_numeric(x, errors='coerce').sum(),
    'criteo_clicks': lambda x: pd.to_numeric(x, errors='coerce').sum(),
    'competitor_clicks': lambda x: pd.to_numeric(x, errors='coerce').sum()
})
monthly['total_clicks'] = monthly['criteo_clicks'] + monthly['competitor_clicks']
monthly['comp_share'] = monthly['competitor_clicks'] / monthly['total_clicks'] * 100
monthly['criteo_share'] = monthly['criteo_clicks'] / monthly['total_clicks'] * 100

# Correlation: Does higher competitor share = lower Criteo revenue?
corr_share_rev, corr_p = stats.pearsonr(monthly['comp_share'], monthly['revenue_euro'])
print(f"Pearson correlation: Competitor Click Share vs Criteo Revenue")
print(f"  r = {corr_share_rev:.4f}, p = {corr_p:.2e}")
print(f"  Interpretation: {'Strong' if abs(corr_share_rev) > 0.7 else 'Moderate' if abs(corr_share_rev) > 0.4 else 'Weak'} "
      f"{'negative' if corr_share_rev < 0 else 'positive'} relationship")

# Does this mean competitor share erodes revenue?
if corr_share_rev < -0.4:
    print(f"\n  ⚠️ FINDING: Higher competitor click share is associated with LOWER Criteo revenue")
    print(f"     This supports the hypothesis that competitor clicks 'steal' revenue")
elif corr_share_rev > 0.4:
    print(f"\n  🔍 FINDING: Higher competitor click share is associated with HIGHER Criteo revenue")
    print(f"     This is counterintuitive - may indicate confounding (market growth affects both)")
else:
    print(f"\n  📊 FINDING: Weak relationship - competitor share and revenue not strongly linked")

print(f"\n=== 7. SEGMENT-LEVEL CORRELATION ===")
for seg in ['Extra-Small', 'Small', 'Medium', 'Large']:
    seg_mask = (df['segment'] == seg) & valid_mask
    if seg_mask.sum() > 100:
        seg_rev = revenue[seg_mask]
        seg_clicks = criteo_clicks[seg_mask]
        seg_r, seg_p = stats.pearsonr(seg_clicks, seg_rev)
        print(f"{seg:12s}: r = {seg_r:.4f} (n = {seg_mask.sum():,})")

print(f"\n=== 8. KEY STATISTICAL CONCLUSIONS ===")
print(f"""
1. CLICKS-REVENUE CORRELATION:
   - Pearson r = {pearson_r:.4f} → {'Strong' if abs(pearson_r) > 0.7 else 'Moderate' if abs(pearson_r) > 0.4 else 'Weak'} linear relationship
   - Each Criteo click ≈ €{slope:.4f} in revenue (on average)
   - R² = {r_value**2:.4f} → Clicks explain {r_value**2*100:.1f}% of revenue variance

2. CLICK SHARE AS REVENUE PROXY:
   - Correlation (Comp Share vs Revenue): r = {corr_share_rev:.4f}
   - {'VALIDATED: Click share is a reasonable proxy for revenue impact' if abs(corr_share_rev) > 0.4 else 'CAUTION: Click share is a WEAK proxy for revenue impact'}

3. STATISTICAL VALIDITY OF APPROACH:
   - Using click-based market share is {'statistically justified' if abs(pearson_r) > 0.6 else 'acceptable but imperfect'}
   - Recommendation: Always note "click-based" when presenting market share
""")

print("=" * 70)
print("ANALYSIS COMPLETE")
print("=" * 70)
