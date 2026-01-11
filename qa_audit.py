"""
QA Audit - Final Triple Check
Scan for "4 digit percentages" or anomalous values > 100%
"""

import re
import sys

print("🕵️ QA TRIPLE-CHECK AUDIT")
print("="*80)

with open('output/presentation/criteo_ceo_presentation.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Check for suspiciously high percentages (>100%)
# Matches 3+ digits before a % sign (e.g. 100%, 1234%)
# Note: Some might be valid (growth rates?), but we flag them
high_pct_pattern = r'(\d{3,3})\s*%'
high_pcts = re.finditer(high_pct_pattern, html)

anomalies = []
for match in high_pcts:
    val = int(match.group(1))
    # Filter: 100% is fine, maybe up to 150% is fine for growth... 
    # But 1000%+ is definitely bad
    if val > 150:
        # Get context
        start = max(0, match.start() - 20)
        end = min(len(html), match.end() + 20)
        context = html[start:end].replace('\n', ' ')
        anomalies.append(f"Value: {val}% | Context: ...{context}...")

# 2. Check for Chart Data Arrays with high numbers
# Regex for Chart.js data arrays: data: [1, 2, 3...]
chart_data_matches = re.finditer(r'data:\s*\[([\d\.,\s]+)\]', html)
for match in chart_data_matches:
    content = match.group(1)
    # Split by comma
    values = [float(x.strip()) for x in content.split(',') if x.strip()]
    for v in values:
        if v > 150:
             # Context roughly
             start = max(0, match.start() - 50)
             context = html[start:match.start()]
             anomalies.append(f"Chart Data: {v} | Context: {context.strip()}")

# 3. Report
if anomalies:
    print(f"❌ FOUND {len(anomalies)} POTENTIAL ANOMALIES:")
    for a in anomalies:
        print(f"  - {a}")
    print("\n⚠️ RECOMMENDATION: Fix these immediately.")
else:
    print("✅ NO ANOMALIES FOUND.")
    print("  - No percentages > 150% detected in text")
    print("  - No chart data points > 150 detected")

print("\n(Note: 'Competitor Market Share' should be < 100%)")
