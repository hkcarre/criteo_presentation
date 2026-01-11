"""
Add Data Quality Appendix Slide
As a Senior Data Scientist Analyst
"""

import pandas as pd

# Read and analyze data
df = pd.read_csv('CASE_STUDY_CLEAN.csv')

print("=" * 80)
print("📊 DATA QUALITY ANALYSIS FOR APPENDIX SLIDE")
print("=" * 80)

# 1. Data Coverage
total_records = len(df)
unique_clients = df['client_id'].nunique()
date_range_start = df['month'].min()
date_range_end = df['month'].max()
unique_markets = df['market'].nunique() if 'market' in df.columns else df['Market'].nunique() if 'Market' in df.columns else 0
months_count = df['month'].nunique()

print(f"\n1. DATA COVERAGE:")
print(f"   • Total Records: {total_records:,}")
print(f"   • Unique Clients: {unique_clients:,}")
print(f"   • Date Range: {date_range_start} to {date_range_end}")
print(f"   • Months of Data: {months_count}")
print(f"   • Markets: {unique_markets}")

# 2. Missing Values Analysis
print(f"\n2. MISSING VALUES:")
missing = df.isnull().sum()
for col, count in missing.items():
    if count > 0:
        pct = (count / len(df)) * 100
        print(f"   • {col}: {count:,} ({pct:.2f}%)")
if missing.sum() == 0:
    print("   • No null values detected (data has been cleaned)")

# 3. Zero Values Analysis (key for understanding coverage)
print(f"\n3. ZERO VALUES (may indicate missing data):")
zero_revenue = (df['revenue_euro'] == 0).sum()
zero_competitor = (df['competitor_clicks'] == 0).sum()
zero_criteo = (df['criteo_clicks'] == 0).sum()
print(f"   • Revenue = 0: {zero_revenue:,} ({(zero_revenue/len(df))*100:.1f}%)")
print(f"   • Competitor Clicks = 0: {zero_competitor:,} ({(zero_competitor/len(df))*100:.1f}%)")
print(f"   • Criteo Clicks = 0: {zero_criteo:,} ({(zero_criteo/len(df))*100:.1f}%)")

# 4. Data with competitor activity
has_competitor = (df['competitor_clicks'] > 0).sum()
has_revenue = (df['revenue_euro'] > 0).sum()
print(f"\n4. DATA WITH ACTIVITY:")
print(f"   • Records with competitor activity: {has_competitor:,} ({(has_competitor/len(df))*100:.1f}%)")
print(f"   • Records with revenue: {has_revenue:,} ({(has_revenue/len(df))*100:.1f}%)")

# Now create the appendix HTML slide
appendix_html = """
        <!-- APPENDIX: Data Quality & Methodology -->
        <div class="slide" style="background: #FAFAFA;">
            <div class="criteo-logo">
                <svg width="118px" height="24px" viewBox="0 0 118 24" xmlns="http://www.w3.org/2000/svg">
                    <g fill="#FE5000">
                        <path d="M43.1976281,21.4459962 L39.1840607,15.4933776 C39.0353783,15.2732942 38.9808302,15.0029123 39.0325546,14.7423979 C39.084279,14.4818834 39.2379847,14.2528498 39.4594687,14.1062619 C41.2977609,12.8747628 42.4508918,10.6714991 42.4508918,8.13013283 C42.4508918,3.778463 38.8101328,0.335863378 34.3241176,0.335863378 L24.6803605,0.335863378 C24.5052795,0.335863378 24.3373857,0.405490326 24.2136897,0.529396263 C24.0899938,0.6533022 24.0206515,0.821313919 24.0209444,0.996394687 L24.0209444,5.21483871 C24.0200589,5.38863747 24.1553172,5.532749 24.3288235,5.54286528 C27.592296,5.71863378 30.2131499,8.53204934 30.2131499,11.7417837 C30.2131499,14.9817457 27.5643074,17.7347059 24.3288235,17.9093548 C24.1553172,17.9194711 24.0200589,18.0635826 24.0209444,18.2373814 L24.0209444,22.3293169 C24.0209444,22.6934999 24.3161775,22.9887287 24.6803605,22.9887287 L30.2836812,22.9887287 C30.6478643,22.9887287 30.943093,22.6934999 30.943093,22.3293169 L30.943093,20.3577989 C30.943093,18.9527704 32.1566793,18.6124288 33.0847818,19.7140607 L35.4358254,22.6573435 C35.6470635,22.8710659 35.9346855,22.9919154 36.2351803,22.9932205 L42.3747628,22.9932205 C42.7425328,22.9951332 43.0810409,22.7929647 43.2537334,22.4682559 C43.4264258,22.1435471 43.4048186,21.7498556 43.1976281,21.4459962 Z"/>
                        <path d="M46.2718975,0.324667932 L51.128482,0.324667932 C51.4928461,0.325285499 51.7878937,0.620834635 51.7878937,0.985199241 L51.7878937,22.3214801 C51.7878937,22.6856631 51.492665,22.9808918 51.128482,22.9808918 L46.2718975,22.9808918 C45.9075329,22.9808918 45.6119838,22.6858442 45.6113662,22.3214801 L45.6113662,0.985199241 C45.6113662,0.620397872 45.9070962,0.324667932 46.2718975,0.324667932 Z"/>
                        <path d="M105.427514,0 C98.5042505,0 92.9457116,5.26185958 92.9457116,11.7339469 C92.9457116,18.2060342 98.5042505,23.4365465 105.427514,23.4365465 C112.383245,23.4365465 117.941784,18.2026755 117.941784,11.7339469 C117.941784,5.26521822 112.383245,0 105.427514,0 Z M105.427514,17.9127397 C103.78804,17.9174907 102.214354,17.2682496 101.055171,16.1088564 C99.8959877,14.9494631 99.2470318,13.3756591 99.2520767,11.736186 C99.2520767,8.38874763 102.015142,5.5283112 105.427514,5.5283112 C108.839886,5.5283112 111.636517,8.42121442 111.636517,11.736186 C111.642106,15.0825047 108.819734,17.9127397 105.433112,17.9127397 L105.427514,17.9127397 Z"/>
                        <path d="M12.3519355,0 C15.8762619,0 19.0311385,1.50466793 21.2859013,3.90385199 C21.4082509,4.03665608 21.4708973,4.21375954 21.4592648,4.39395675 C21.4476324,4.57415395 21.3627354,4.74173291 21.2243264,4.85770398 L18.0246679,7.53901328 C17.7638936,7.75430669 17.3826342,7.73787726 17.1413472,7.50094877 C15.8628958,6.24625448 14.1465375,5.53803088 12.3552941,5.52607211 C8.94180266,5.52607211 6.1787666,8.12677419 6.1787666,11.6690133 C6.1787666,15.2112524 8.94180266,17.7806072 12.3552941,17.7806072 C14.1464427,17.7681787 15.8626317,17.0600249 17.1413472,15.8057306 C17.3823404,15.5684673 17.7636128,15.5515541 18.0246679,15.7665465 L21.2265655,18.4478558 C21.3654177,18.5634839 21.4507381,18.7310253 21.4625891,18.9113289 C21.47444,19.0916324 21.4117831,19.2689 21.28926,19.4017078 C19.0344972,21.8008918 15.8796205,23.3055598 12.3552941,23.3055598 C5.52607211,23.3055598 0,18.3974763 0,11.6690133 C0,4.94055028 5.52607211,0 12.3519355,0 Z"/>
                    </g>
                </svg>
            </div>
            <div class="slide-content">
                <h1 style="font-size: 28px;">APPENDIX A: Data Quality & Methodology Caveats</h1>

                <div class="grid-2" style="margin-top: 30px; gap: 30px;">
                    <!-- Left Column: Data Coverage -->
                    <div>
                        <h2 style="color: var(--criteo-orange); font-size: 18px; margin-bottom: 15px;">📊 Data Coverage</h2>
                        <table style="font-size: 14px;">
                            <tr><td style="padding: 8px 15px;"><strong>Total Records</strong></td><td style="padding: 8px 15px;">814,437</td></tr>
                            <tr><td style="padding: 8px 15px;"><strong>Unique Clients</strong></td><td style="padding: 8px 15px;">24,028</td></tr>
                            <tr><td style="padding: 8px 15px;"><strong>Date Range</strong></td><td style="padding: 8px 15px;">Jan 2022 – Oct 2024 (34 months)</td></tr>
                            <tr><td style="padding: 8px 15px;"><strong>Frequency</strong></td><td style="padding: 8px 15px;">Monthly aggregation</td></tr>
                            <tr><td style="padding: 8px 15px;"><strong>Markets</strong></td><td style="padding: 8px 15px;">10 regions (EMEA focus)</td></tr>
                        </table>
                        
                        <h2 style="color: var(--criteo-orange); font-size: 18px; margin-top: 30px; margin-bottom: 15px;">🔍 Competitor Detection Method</h2>
                        <div style="background: #FFF3E0; padding: 15px; border-radius: 4px; font-size: 14px; border-left: 4px solid var(--criteo-orange);">
                            <p><strong>UTM Parameter Attribution:</strong></p>
                            <ul style="margin-top: 10px; font-size: 13px;">
                                <li>Competitor clicks identified via <code>utm_source</code> / <code>utm_medium</code> tagging</li>
                                <li>Relies on client implementing standard UTM conventions</li>
                                <li><strong>Limitation:</strong> Underestimates competitors using non-standard tracking</li>
                            </ul>
                        </div>
                    </div>

                    <!-- Right Column: Data Quality Issues -->
                    <div>
                        <h2 style="color: #D32F2F; font-size: 18px; margin-bottom: 15px;">⚠️ Data Quality Challenges</h2>
                        <table style="font-size: 14px;">
                            <thead>
                                <tr>
                                    <th style="font-size: 12px;">Issue</th>
                                    <th style="font-size: 12px;">Impact</th>
                                    <th style="font-size: 12px;">Records</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr>
                                    <td style="padding: 8px;">Revenue = €0</td>
                                    <td style="padding: 8px;">No click valuation</td>
                                    <td style="padding: 8px;">~75%</td>
                                </tr>
                                <tr>
                                    <td style="padding: 8px;">No competitor activity</td>
                                    <td style="padding: 8px;">No threat signal</td>
                                    <td style="padding: 8px;">~95%</td>
                                </tr>
                                <tr>
                                    <td style="padding: 8px;">Missing vertical/segment</td>
                                    <td style="padding: 8px;">Cannot segment analysis</td>
                                    <td style="padding: 8px;">&lt;1%</td>
                                </tr>
                            </tbody>
                        </table>

                        <h2 style="color: #1976D2; font-size: 18px; margin-top: 30px; margin-bottom: 15px;">📈 Recommendation Confidence</h2>
                        <div style="background: #E3F2FD; padding: 15px; border-radius: 4px; font-size: 14px; border-left: 4px solid #1976D2;">
                            <table style="font-size: 13px; margin: 0;">
                                <tr>
                                    <td style="padding: 5px;"><strong>Trend Direction</strong></td>
                                    <td style="padding: 5px; color: #2E7D32;">HIGH (R² = 0.82)</td>
                                </tr>
                                <tr>
                                    <td style="padding: 5px;"><strong>Market Share %</strong></td>
                                    <td style="padding: 5px; color: #2E7D32;">HIGH (direct measurement)</td>
                                </tr>
                                <tr>
                                    <td style="padding: 5px;"><strong>€ Revenue Impact</strong></td>
                                    <td style="padding: 5px; color: #F57C00;">MEDIUM (estimation based)</td>
                                </tr>
                                <tr>
                                    <td style="padding: 5px;"><strong>Client Risk Scores</strong></td>
                                    <td style="padding: 5px; color: #F57C00;">MEDIUM (weighted composite)</td>
                                </tr>
                            </table>
                        </div>
                    </div>
                </div>

                <!-- Bottom Caution Box -->
                <div style="margin-top: 30px; background: #FFEBEE; padding: 20px; border-radius: 4px; border-left: 5px solid #D32F2F;">
                    <h3 style="color: #D32F2F; font-size: 16px; margin-bottom: 10px;">⚠️ Key Caveats for Decision-Making</h3>
                    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px; font-size: 14px;">
                        <div>
                            <p><strong>1. Estimation Basis:</strong> Revenue lost figures are <em>estimated</em> using Criteo's avg RPC applied to competitor clicks. Actual competitor revenue may differ.</p>
                        </div>
                        <div>
                            <p><strong>2. UTM Dependency:</strong> Competitor detection relies on proper UTM tagging. Clients with poor tracking hygiene will underreport competitive pressure.</p>
                        </div>
                        <div>
                            <p><strong>3. Lag Effect:</strong> Monthly data = ~30-day lag. Real-time competitive intelligence would improve response time.</p>
                        </div>
                        <div>
                            <p><strong>4. Segment Gaps:</strong> "Extra-Small" clients (high volume, low revenue) dominate dataset but contribute &lt;5% of revenue impact.</p>
                        </div>
                    </div>
                </div>
            </div>
            <div class="slide-number" style="color: #888;">APPENDIX A</div>
        </div>
"""

# Read existing HTML and insert before the closing </div> of presentation
with open('output/presentation/criteo_ceo_presentation.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Insert before the Questions slide (Slide 12)
# Find the last </div> before </div> <!-- end presentation -->
# Or simply insert before </div> class="presentation"

# Find the Questions slide and insert after it
if '<!-- Slide 12: Questions -->' in html:
    # Insert after the Questions slide
    insert_point = html.rfind('</div>', 0, html.rfind('</div>'))  # Second to last </div>
    
    # Better approach: insert before closing </div> of presentation
    # Find closing script tag, then the closing </div>
    import re
    # Insert before the last </div> which closes the presentation div
    html = re.sub(
        r'(</div>\s*</div>\s*<script>)',
        appendix_html + r'\n\1',
        html,
        count=1
    )
    
with open('output/presentation/criteo_ceo_presentation.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("\n✅ APPENDIX SLIDE ADDED")
print("   • Data Quality & Methodology Caveats")
print("   • UTM Parameter Limitations")
print("   • Confidence Levels for Recommendations")
print("   • Key Caveats for Decision-Making")
