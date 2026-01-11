import re

file_path = r'c:\Dev\entrevista\output\presentation\criteo_ceo_presentation.html'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Redesign Appendix C specifically
print("Redesigning Appendix C with visual...")

# Define the new content for Appendix C
new_appendix_c = """
    <!-- APPENDIX C: Statistical Deep-Dive -->
    <div class="slide" style="background: #FAFAFA;">
        <div class="slide-content" style="width: 95%; max-width: 1300px; margin: 0 auto; padding: 40px 0;">
            <h1 style="font-size: 26px; margin-bottom: 30px; text-align: left; border-bottom: 2px solid var(--criteo-orange); padding-bottom: 10px;">APPENDIX C: Statistical Deep-Dive & Growth Methodology</h1>
            
            <div style="display: grid; grid-template-columns: 1fr 1.5fr; gap: 50px; align-items: start;">
                <!-- Left Side: Professional Visual -->
                <div style="background: white; padding: 20px; border-radius: 12px; box-shadow: 0 10px 30px rgba(0,0,0,0.05); border: 1px solid #eee;">
                    <img src="images/appendix_c_viz.png" style="width: 100%; height: auto; border-radius: 8px;" alt="Statistical Analysis Visual">
                    <p style="font-size: 13px; color: #666; margin-top: 15px; font-style: italic;">
                        Fig C.1: Multi-dimensional variance analysis showing the shift from stochastic noise (MoM) to structural signal (YoY).
                    </p>
                </div>

                <!-- Right Side: Data Tables (Stacked or in internal grid) -->
                <div>
                    <div class="grid-2" style="gap: 30px; margin: 0;">
                        <!-- Column 1: Stability -->
                        <div>
                            <h2 style="color: var(--criteo-orange); font-size: 16px; margin-bottom: 15px; margin-top: 0;">📊 Statistical Stability</h2>
                            <table style="font-size: 13px; background: white !important;">
                                <thead>
                                    <tr><th>Metric</th><th>MoM</th><th>YoY</th></tr>
                                </thead>
                                <tbody>
                                    <tr><td>Trend Clarity</td><td style="color: #D32F2F;">Low Noise</td><td style="color: #4CAF50;"><strong>High Signal</strong></td></tr>
                                    <tr><td>Volatility</td><td style="color: #D32F2F;">High Var</td><td>Smoothed</td></tr>
                                    <tr><td>Actionability</td><td>Interpretative</td><td style="color: #4CAF50;"><strong>Actionable</strong></td></tr>
                                </tbody>
                            </table>

                            <h2 style="color: #D32F2F; font-size: 16px; margin-top: 25px; margin-bottom: 12px;">⚠️ April 2023 Break</h2>
                            <div style="background: #FFEBEE; padding: 12px; border-radius: 4px; border-left: 3px solid #D32F2F;">
                                <p style="font-size: 14px; margin: 0;"><strong>5.1% → 20.8%</strong> (4x Jump)</p>
                                <p style="font-size: 12px; color: #666; margin-top: 5px;">Fundamental shift in market competitive intensity.</p>
                            </div>
                        </div>

                        <!-- Column 2: Evolution & Revenue -->
                        <div>
                            <h2 style="color: #1976D2; font-size: 16px; margin-bottom: 15px; margin-top: 0;">📈 Two-Phase Evolution</h2>
                            <table style="font-size: 13px; background: white !important;">
                                <thead>
                                    <tr><th>Phase</th><th>Period</th><th>Share</th></tr>
                                </thead>
                                <tbody>
                                    <tr><td><strong>Phase 1</strong></td><td>'22 - Q1 '23</td><td>2% - 6%</td></tr>
                                    <tr><td><strong>Phase 2</strong></td><td>Apr '23 - Present</td><td>17% - 27%</td></tr>
                                </tbody>
                            </table>

                            <h2 style="color: #1976D2; font-size: 16px; margin-top: 25px; margin-bottom: 12px;">💰 Revenue Impact</h2>
                            <div style="background: #E3F2FD; padding: 12px; border-radius: 4px; border-left: 3px solid #1976D2;">
                                <table style="font-size: 13px; margin: 0; background: transparent !important; border: none !important;">
                                    <tr style="border:none !important;"><td style="padding: 4px; border:none !important;">2022:</td><td style="padding: 4px; border:none !important;"><strong>€112.3M</strong></td></tr>
                                    <tr style="border:none !important;"><td style="padding: 4px; border:none !important;">2023:</td><td style="padding: 4px; border:none !important;">€101.2M</td></tr>
                                    <tr style="border:none !important;"><td style="padding: 4px; border:none !important;">2024 (Est):</td><td style="padding: 4px; border:none !important; color: #D32F2F;"><strong>€92.6M</strong></td></tr>
                                </table>
                            </div>
                        </div>
                    </div>
                    
                    <!-- Bottom Insight -->
                    <div style="margin-top: 30px; background: #FFF3E0; padding: 15px; border-radius: 4px; border-left: 5px solid #FF9800;">
                        <p style="font-size: 13px; margin: 0;"><strong>Analyst Note:</strong> Methodology pivots to 12-month trailing averages to remove seasonal bias in competitor detection rates.</p>
                    </div>
                </div>
            </div>
        </div>
        <div class="slide-number" style="color: #888;">APPENDIX C</div>
    </div>"""

# Replace the entire Appendix C block
pattern = r'<!-- APPENDIX C: Statistical Deep-Dive -->.*?<div class="slide".*?>.*?</div>\s+<div class="slide-number".*?>APPENDIX C</div>\s+</div>'
content = re.sub(pattern, new_appendix_c, content, flags=re.DOTALL)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Done!")
