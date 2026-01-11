"""
Generate visualizations for the presentation
"""
import pandas as pd
import json
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Set style
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")

# Load data
df = pd.read_csv('CASE_STUDY_CLEAN.csv')
df['month'] = pd.to_datetime(df['month'])

with open('analysis_results.json', 'r') as f:
    results = json.load(f)

# Create output directory
import os
os.makedirs('output/presentation/images', exist_ok=True)

# Figure 1: Threat Evolution Over Time
print("Creating Figure 1: Threat Evolution...")
monthly_data = pd.DataFrame(results['q1']['monthly_data'])
monthly_data['month'] = pd.to_datetime(monthly_data['month'])

fig, ax1 = plt.subplots(figsize=(12, 6))

ax1.set_xlabel('Month', fontsize=12, fontweight='bold')
ax1.set_ylabel('Revenue Lost (%)', fontsize=12, fontweight='bold', color='tab:red')
ax1.plot(monthly_data['month'], monthly_data['revenue_lost_pct'], 
         color='tab:red', linewidth=2.5, marker='o', label='Revenue Lost %')
ax1.tick_params(axis='y', labelcolor='tab:red')
ax1.grid(True, alpha=0.3)

ax2 = ax1.twinx()
ax2.set_ylabel('Estimated Revenue Lost (€M)', fontsize=12, fontweight='bold', color='tab:blue')
revenue_millions = [x/1000000 for x in monthly_data['estimated_revenue_lost']]
ax2.plot(monthly_data['month'], revenue_millions,
         color='tab:blue', linewidth=2.5, marker='s', linestyle='--', label='Revenue Lost (€M)')
ax2.tick_params(axis='y', labelcolor='tab:blue')

plt.title('Competitive Threat Evolution: Revenue at Risk Intensifying', 
          fontsize=14, fontweight='bold', pad=20)
fig.tight_layout()
plt.savefig('output/presentation/images/threat_evolution.png', dpi=300, bbox_inches='tight')
plt.close()

# Figure 2: Competitor Launches Over Time
print("Creating Figure 2: Competitor Launches...")
launches_data = pd.DataFrame(results['q2']['launches_by_month'])
launches_data['month'] = pd.to_datetime(launches_data['month'])

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8))

# Launches per month
ax1.bar(launches_data['month'], launches_data['new_launches'], 
        color='coral', alpha=0.7, label='New Launches')
ax1.plot(launches_data['month'], launches_data['ma3'], 
         color='darkred', linewidth=2.5, label='3-Month MA')
ax1.set_ylabel('New Competitor Launches', fontsize=11, fontweight='bold')
ax1.set_title('Competitor Launch Frequency: Accelerating Entry', 
              fontsize=13, fontweight='bold')
ax1.legend()
ax1.grid(True, alpha=0.3)

# Cumulative launches
ax2.fill_between(launches_data['month'], launches_data['cumulative_launches'], 
                  alpha=0.5, color='steelblue')
ax2.plot(launches_data['month'], launches_data['cumulative_launches'], 
         color='navy', linewidth=2.5)
ax2.set_ylabel('Cumulative Launches', fontsize=11, fontweight='bold')
ax2.set_xlabel('Month', fontsize=11, fontweight='bold')
ax2.set_title('Cumulative Competitor Penetration', fontsize=13, fontweight='bold')
ax2.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('output/presentation/images/competitor_launches.png', dpi=300, bbox_inches='tight')
plt.close()

# Figure 3: Market Risk Heatmap
print("Creating Figure 3: Market Risk Heatmap...")
market_data = pd.DataFrame(results['q3']['market'])
top_markets = market_data.nlargest(10, 'threat_score')

fig, ax = plt.subplots(figsize=(10, 6))
colors = ['#d4edda' if x == 'LOW' else '#fff3cd' if x == 'MEDIUM' else '#f8d7da' 
          for x in top_markets['risk_level']]

bars = ax.barh(top_markets['market'], top_markets['revenue_lost_pct'], color=colors, edgecolor='black')
ax.set_xlabel('Revenue Lost (%)', fontsize=12, fontweight='bold')
ax.set_title('Top 10 Markets by Competitive Threat', fontsize=14, fontweight='bold', pad=20)
ax.grid(axis='x', alpha=0.3)

# Add value labels
for i, (idx, row) in enumerate(top_markets.iterrows()):
    ax.text(row['revenue_lost_pct'] + 0.1, i, f"{row['revenue_lost_pct']:.1f}%", 
            va='center', fontweight='bold')

plt.tight_layout()
plt.savefig('output/presentation/images/market_risk.png', dpi=300, bbox_inches='tight')
plt.close()

# Figure 4: Vertical Risk Analysis
print("Creating Figure 4: Vertical Risk...")
vertical_data = pd.DataFrame(results['q3']['vertical'])
top_verticals = vertical_data.nlargest(8, 'threat_score')

fig, ax = plt.subplots(figsize=(10, 6))
x = np.arange(len(top_verticals))
width = 0.35

bars1 = ax.bar(x - width/2, top_verticals['revenue_lost_pct'], width, 
               label='Revenue Lost %', color='indianred', alpha=0.8)
bars2 = ax.bar(x + width/2, top_verticals['competitor_share'], width,
               label='Competitor Click Share %', color='steelblue', alpha=0.8)

ax.set_ylabel('Percentage', fontsize=12, fontweight='bold')
ax.set_title('Vertical Vulnerability Analysis: Top 8 Threatened Industries', 
             fontsize=14, fontweight='bold', pad=20)
ax.set_xticks(x)
ax.set_xticklabels([v[:20] + '...' if len(v) > 20 else v for v in top_verticals['vertical']], 
                   rotation=45, ha='right')
ax.legend()
ax.grid(axis='y', alpha=0.3)

plt.tight_layout()
plt.savefig('output/presentation/images/vertical_risk.png', dpi=300, bbox_inches='tight')
plt.close()

# Figure 5: Client Risk Distribution
print("Creating Figure 5: Client Risk Distribution...")
top_20_clients = pd.DataFrame(results['q4']['top_20_clients'])

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

# Risk score distribution
ax1.scatter(range(1, 21), top_20_clients['risk_score'], 
           s=top_20_clients['revenue_lost']/1000, 
           c=top_20_clients['trend_pct'], cmap='RdYlGn_r', 
           alpha=0.6, edgecolors='black', linewidth=1.5)
ax1.set_xlabel('Client Rank', fontsize=12, fontweight='bold')
ax1.set_ylabel('Risk Score (0-100)', fontsize=12, fontweight='bold')
ax1.set_title('Top 20 High-Risk Clients: Size = Revenue Lost, Color = Trend', 
              fontsize=13, fontweight='bold')
ax1.grid(True, alpha=0.3)

# Revenue concentration
revenue_lost_millions = [x/1000000 for x in top_20_clients['revenue_lost']]
ax2.barh(range(1, 21), revenue_lost_millions, color='crimson', alpha=0.7)
ax2.set_xlabel('Revenue Lost (€M)', fontsize=12, fontweight='bold')
ax2.set_ylabel('Client Rank', fontsize=12, fontweight='bold')
ax2.set_title('Revenue at Risk by Client', fontsize=13, fontweight='bold')
ax2.invert_yaxis()
ax2.grid(axis='x', alpha=0.3)

plt.tight_layout()
plt.savefig('output/presentation/images/client_risk.png', dpi=300, bbox_inches='tight')
plt.close()

print("\n✅ All visualizations created successfully!")
print("   Saved to: output/presentation/images/")
