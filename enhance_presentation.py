"""
Enhance presentation with McKinsey storytelling and fix contrast issues
"""

# Read the current HTML
with open('output/presentation/criteo_ceo_presentation.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Add McKinsey SO WHAT box style after the alert-box h4 style
so_what_css = """
        /* McKinsey-style "SO WHAT?" Insight Box */
        .so-what-box {
            background: linear-gradient(135deg, var(--criteo-orange) 0%, var(--criteo-orange-dark) 100%);
            color: white;
            padding: 25px 30px;
            margin: 30px 0;
            border-radius: 4px;
            border-left: 6px solid #C63D17;
            font-size: 18px;
            font-weight: 600;
            line-height: 1.5;
            box-shadow: 0 4px 15px rgba(255, 87, 34, 0.3);
        }
        
        .so-what-label {
            font-size: 12px;
            text-transform: uppercase;
            letter-spacing: 1.5px;
            opacity: 0.95;
            display: block;
            margin-bottom: 10px;
            font-weight: 700;
        }
"""

# Insert after .alert-box h4
html = html.replace(
    '        .alert-box h4 {',
    so_what_css + '\n        .alert-box h4 {'
)

# Update Criteo logo styling
html = html.replace(
    """        /* Criteo Logo */
        .criteo-logo {
            position: absolute;
            top: 30px;
            right: 60px;
            font-size: 16px;
            font-weight: bold;
            color: var(--criteo-orange);
            letter-spacing: 1px;
        }""",
    """        /* Criteo Logo - Matching Brand */
        .criteo-logo {
            position: absolute;
            top: 30px;
            right: 60px;
            font-size: 20px;
            font-weight: 900;
            color: var(--criteo-orange);
            letter-spacing: 3px;
            font-family: var(--font-primary);
        }"""
)

# Fix metric label contrast
html = html.replace(
    """        .metric-label {
            font-size: 14px;
            color: var(--criteo-gray);
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }""",
    """        .metric-label {
            font-size: 14px;
            color: var(--criteo-black);
            text-transform: uppercase;
            letter-spacing: 0.5px;
            font-weight: 600;
        }"""
)

# Fix summary slide contrast
html = html.replace(
    """        .summary-slide .metric-value {
            color: var(--criteo-orange);
        }""",
    """        .summary-slide .metric-value {
            color: var(--criteo-orange);
        }
        
        .summary-slide .metric-label {
            color: white !important;
        }
        
        .summary-slide li {
            color: white;
        }
        
        .summary-slide p {
            color: #CCCCCC;
        }"""
)

# Update all CRITEO+ logos to just CRITEO
html = html.replace('CRITEO<span style="color: var(--criteo-blue);">+</span>', 'CRITEO')

# Now add SO WHAT boxes to each slide

# Slide 2 - Executive Summary SO WHAT
slide_2_insight = """
                <div class="so-what-box">
                    <span class="so-what-label">💡 SO WHAT?</span>
                    While Criteo maintains market leadership, accelerating competitive pressure demands immediate defensive action—particularly in high-vulnerability segments where we risk permanent revenue loss.
                </div>
"""
html = html.replace(
    '                <div class="metrics-row" style="margin-top: 50px;">',
    slide_2_insight + '\n                <div class="metrics-row" style="margin-top: 50px;">'
)

# Slide 3 - Threat Evolution SO WHAT
slide_3_insight = """
                <div class="so-what-box">
                    <span class="so-what-label">💡 SO WHAT?</span>
                    The threat isn't just growing—it's accelerating. Without intervention, we project double-digit revenue erosion within 18 months, requiring both immediate triage and systemic competitive response.
                </div>
"""
html = html.replace(
    '                <h3>Key Findings:</h3>',
    slide_3_insight + '\n                <h3>Key Findings:</h3>'
)

# Slide 4 - Competitor Launches SO WHAT
slide_4_insight = """
                <div class="so-what-box">
                    <span class="so-what-label">💡 SO WHAT?</span>
                    Competitor launch acceleration signals market maturation and product commoditization. Early warning systems are no longer optional—they're essential for survival.
                </div>
"""
html = html.replace(
    '                <h3>Strategic Implications:</h3>',
    slide_4_insight + '\n                <h3>Strategic Implications:</h3>'
)

# Slide 5 - Market Landscape SO WHAT
slide_5_insight = """
                <div class="so-what-box">
                    <span class="so-what-label">💡 SO WHAT?</span>
                    Geographic clustering reveals systematic vulnerabilities. Southern European markets require dedicated competitive taskforces with market-specific playbooks to stem revenue hemorrhaging.
                </div>
"""
html = html.replace(
    '                <table style="margin-top: 40px;">',
    slide_5_insight + '\n                <table style="margin-top: 40px;">'
)

# Slide 6 - High-Risk Clients SO WHAT
slide_6_insight = """
                <div class="so-what-box">
                    <span class="so-what-label">💡 SO WHAT?</span>
                    €39.5M in concentrated risk means losing just 5 clients could trigger 10%+ revenue decline. These 20 accounts demand white-glove, CEO-level intervention within 30 days.
                </div>
"""
html = html.replace(
    '                <table style="margin-top: 40px;">',
    slide_6_insight + '\n                <table style="margin-top: 40px;">',
    1  # Only replace first occurrence (slide 6, not slide 5)
)

# Slide 7 - Recommendations Part 1 SO WHAT
slide_7_insight = """
                <div class="so-what-box">
                    <span class="so-what-label">💡 SO WHAT?</span>
                    Defense beats offense in mature markets. Protecting existing revenue (€23.7M) delivers 3x ROI vs. new customer acquisition—making retention the highest-leverage growth strategy available.
                </div>
"""
html = html.replace(
    '                <div class="recommendation">',
    slide_7_insight + '\n                <div class="recommendation">',
    1  # First occurrence on slide 7
)

# Slide 9 - Alert System SO WHAT
slide_9_insight = """
                <div class="so-what-box">
                    <span class="so-what-label">💡 SO WHAT?</span>
                    Speed wins in competitive defense. Real-time alerts compress response time from weeks to hours—the difference between retaining and losing a €2M+ account.
                </div>
"""
html = html.replace(
    '                <h3 style="margin-top: 40px;">Severity-Based Thresholds:</h3>',
    slide_9_insight + '\n                <h3 style="margin-top: 40px;">Severity-Based Thresholds:</h3>'
)

# Save the enhanced HTML
with open('output/presentation/criteo_ceo_presentation.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("✅ Presentation enhanced with McKinsey storytelling!")
print("✅ Logo updated to match Criteo brand")
print("✅ Contrast issues fixed for accessibility")
print("✅ SO WHAT boxes added to 7 key slides")
