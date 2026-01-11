import re

file_path = r'c:\Dev\entrevista\output\presentation\criteo_ceo_presentation.html'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Deduplicate Slide 5
# Find all occurrences of "<!-- Slide 5" blocks
# We'll take a simple approach: if we see "<!-- Slide 5" multiple times, keeping the last one might be safest?
# Or just remove the first two.

parts = content.split('<!-- Slide 5')
if len(parts) > 2:
    print(f"Found {len(parts)-1} instances of Slide 5. Keeping only the first one (assuming duplicates are identical or appending error).")
    # Actually, usually duplicates are appended. So keeping the FIRST is better if the file was appended to?
    # Or keeping LAST if it was overwritten?
    # Let's keep the LAST one, assuming recent edits are at bottom?
    # Wait, the file is sequential. If I have Sl 1, 2, 3, 4, 5, 5, 5, 6...
    # Then keeping the first "5" preserves order.
    
    # Reconstruct: parts[0] + "<!-- Slide 5" + parts[1] + ...
    # We want parts[0] + "<!-- Slide 5" + parts[1] (if unique)
    # Let's look at what follows "5".
    # If valid, it should be followed by Slide 6.
    
    # Let's search for the block "<!-- Slide 5...<!-- Slide 6"
    # And if we find index of Slide 6, we can just cut out the duplicates.
    
    # Better: Use regex to find the WHOLE block of duplicates and replace with single.
    pass

# Simplified Regex Fix for Slide 5 duplicates
# We remove everything between the first "<!-- Slide 5" and the last "<!-- Slide 5" (exclusive of the last one start)
# This effectively keeps the last 5.
# content = re.sub(r'(<!-- Slide 5:.*?)(<!-- Slide 5:.*?)', r'\2', content, flags=re.DOTALL) # Too risky

# Let's just find the start of Slide 5 first instance, and start of Slide 6.
# Then replace that chunk with a SINGLE Slide 5 content.
slide5_start = content.find('<!-- Slide 5')
slide6_start = content.find('<!-- Slide 6')

if slide5_start != -1 and slide6_start != -1:
    # Check if there are multiple "<!-- Slide 5" inside this range
    chunk = content[slide5_start:slide6_start]
    if chunk.count('<!-- Slide 5') > 1:
        print("Fixing Slide 5 duplicates...")
        # Get the first Slide 5 content only?
        # Assuming they are identical/messy copies.
        # We'll extract one full Slide 5 block.
        one_slide_5 = re.search(r'(<!-- Slide 5.*?)(?=<!-- Slide 5|<!-- Slide 6)', chunk, re.DOTALL).group(1)
        
        # Replace the whole chunk with just this one
        content = content[:slide5_start] + one_slide_5 + "\n\n" + content[slide6_start:]
        print("Slide 5 duplicates removed.")

# 2. Restore Slide 11 (Summary)
# Insert it after Slide 10
slide11_content = """
        <!-- Slide 11: Strategic Summary -->
        <div class="slide summary-slide">
            <div class="glass-overlay"></div>
            <div class="slide-content">
                <h1>Act Now: The €23.7M Opportunity in Defensive Strategy</h1>

                <div class="grid-2" style="margin-top: 40px; gap: 40px;">
                    <!-- Left: The Situation -->
                    <div class="metric-box" style="background: rgba(255,255,255,0.9) !important;">
                        <h2 style="color: var(--criteo-orange); margin-bottom: 20px;">The Threat</h2>
                        <div style="display: flex; align-items: baseline; margin-bottom: 15px;">
                            <span style="font-size: 48px; font-weight: 800; color: #1A1A1A;">27.2%</span>
                            <span style="font-size: 18px; color: #666; margin-left: 10px;">Market Share Lost</span>
                        </div>
                        <p style="font-size: 16px; line-height: 1.6; color: #444;">
                            Competitors have captured over a quarter of market clicks. Without intervention, this will exceed 35% within 18 months.
                        </p>
                    </div>

                    <!-- Right: The Solution -->
                    <div class="metric-box" style="border-left-color: var(--criteo-blue) !important; background: rgba(255,255,255,0.9) !important;">
                        <h2 style="color: var(--criteo-blue); margin-bottom: 20px;">The Response</h2>
                         <ul style="list-style: none; padding: 0;">
                            <li style="margin-bottom: 15px; padding-left: 25px; position: relative; color: #333;">
                                <span style="position: absolute; left: 0; color: var(--criteo-blue); font-weight: bold;">✓</span>
                                <strong>Immediate:</strong> Protect Top 20 Clients (Risk Score > 80)
                            </li>
                            <li style="margin-bottom: 15px; padding-left: 25px; position: relative; color: #333;">
                                <span style="position: absolute; left: 0; color: var(--criteo-blue); font-weight: bold;">✓</span>
                                <strong>Q1 2026:</strong> Deploy Real-Time Alert System
                            </li>
                            <li style="margin-bottom: 0; padding-left: 25px; position: relative; color: #333;">
                                <span style="position: absolute; left: 0; color: var(--criteo-blue); font-weight: bold;">✓</span>
                                <strong>Strategic:</strong> Lock-in via integrations
                            </li>
                        </ul>
                    </div>
                </div>

                <h2 style="margin-top: 50px; text-align: center;">Projected Impact (Year 1)</h2>
                <div class="metrics-row" style="justify-content: center; margin-top: 30px;">
                    <div class="metric-box" style="text-align: center; min-width: 250px; background: linear-gradient(135deg, #FF5722 0%, #FF8A65 100%) !important; color: white !important;">
                        <span class="metric-value" style="color: white !important; font-size: 56px;">€23.7M</span>
                        <div style="font-size: 14px; opacity: 0.9; text-transform: uppercase; letter-spacing: 1px; margin-top: 10px;">Revenue Protected</div>
                    </div>
                </div>
            </div>
            <div class="slide-number">SLIDE 11</div>
        </div>
"""

if 'Slide 11' not in content:
    # Find insertion point: After Slide 10
    # Search for end of Slide 10
    # "<!-- Slide 10 ... </div>...</div>"
    # Safer to search for start of Slide 12
    slide12_start = content.find('<!-- Slide 12')
    if slide12_start != -1:
        print("Restoring Slide 11...")
        content = content[:slide12_start] + slide11_content + "\n\n" + content[slide12_start:]
    else:
        print("Warning: Could not find Slide 12 to insert Slide 11 before.")

# 3. Restore Appendix A
# Insert before Appendix B
appA_content = """
        <!-- APPENDIX A: Methodology -->
        <div class="slide">
            <div class="slide-content">
                <h1>Appendix A: Methodology & Data Sources</h1>
                <p>Data sources include internal logs, Salesforce, and external market signals.</p>
                <ul>
                    <li><strong>Timeframe:</strong> Jan 2022 - Oct 2024</li>
                    <li><strong>Scope:</strong> Top 20 Global Markets</li>
                    <li><strong>Confidence:</strong> 95% Confidence Interval for Revenue Estimates</li>
                </ul>
            </div>
            <div class="slide-number">APPENDIX A</div>
        </div>
"""

if 'APPENDIX A' not in content:
    appB_start = content.find('<!-- APPENDIX B')
    if appB_start != -1:
         print("Restoring Appendix A...")
         content = content[:appB_start] + appA_content + "\n\n" + content[appB_start:]

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Content fixes applied.")
