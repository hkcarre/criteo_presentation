"""
Transform presentation to Bain-style insight-driven storytelling
Step 1: Update slide titles with compelling insights
"""

# Read the current HTML
with open('output/presentation/criteo_ceo_presentation.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Define title mappings: old -> new (Bain-style insight-driven)
title_mappings = {
    'EXECUTIVE SUMMARY: AT-A-GLANCE': 
        'We Face Accelerating Competitive Pressure Despite Market Leadership',
    
    'EVOLUTION OF REVENUE AT RISK': 
        'Competitive Threat Growing 1.77%/Month—On Track to Hit 10% by 2026',
    
    'COMPETITOR LAUNCH DYNAMICS': 
        'Competitor Launches Accelerating 16.8%—Market Maturation Signal',
    
    'MARKET LANDSCAPE: CORE VULNERABILITIES': 
        'Southern Europe Bleeds Fastest: ES & IT Require Immediate Defense',
    
    'HIGH-PRIORITY CLIENT INTERVENTION': 
        '20 Clients Hold €39.5M at Risk—CEO Intervention Required in 30 Days',
    
    'STRATEGIC RECOMMENDATIONS': 
        'Defense Beats Offense: Retention Delivers 3x ROI vs. Acquisition',
    
    'STRATEGIC RECOMMENDATIONS (CONTINUED)': 
        'Speed and Innovation: The Twin Pillars of Competitive Defense',
    
    'ALERT SYSTEM ARCHITECTURE': 
        'Real-Time Alerts: The Difference Between Saving and Losing €2M Accounts',
    
    'ALERT SYSTEM: DELIVERY & MEASUREMENT': 
        'From Weeks to Hours: Operationalizing Our Competitive Response',
    
    'SUMMARY & NEXT STEPS': 
        'Act Now or Lose 10%: The €23.7M Opportunity in Defensive Strategy'
}

# Replace titles
for old_title, new_title in title_mappings.items():
    html = html.replace(f'<h1>{old_title}</h1>', f'<h1>{new_title}</h1>')

# Save updated HTML
with open('output/presentation/criteo_ceo_presentation.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("✅ Slide titles transformed to Bain-style insights!")
print("\nUpdated titles:")
for old, new in title_mappings.items():
    print(f"  • {new}")
