#!/usr/bin/env python3
"""
FINAL FIX: Remove malformed HTML nesting and ensure clean JavaScript execution
"""

import re

html_file = "output/presentation/criteo_ceo_presentation.html"

print("="*70)
print("🔧 FINAL HTML & JAVASCRIPT FIX")
print("="*70)

with open(html_file, 'r', encoding='utf-8') as f:
    html = f.read()

print(f"\n📄 Original size: {len(html)} bytes")

# ===== FIX 1: Close any unclosed divs before the script tag =====
print("\n🔨 Fixing HTML structure before script...")

# Find the script tag position
script_pos = html.find('<script>')
if script_pos > 0:
    before_script = html[:script_pos]
    after_script = html[script_pos:]
    
    # Count open and close div tags
    open_divs = before_script.count('<div')
    close_divs = before_script.count('</div>')
    
    print(f"  Open div tags: {open_divs}")
    print(f"  Close div tags: {close_divs}")
    
    missing_closes = open_divs - close_divs
    
    if missing_closes > 0:
        print(f"  ⚠️ Missing {missing_closes} closing </div> tags - adding them")
        # Add missing closing divs before script
        before_script += '\n' + ('</div>\n' * missing_closes)
        html = before_script + after_script
        print(f"  ✅ Added {missing_closes} closing div tags")
    elif missing_closes < 0:
        print(f"  ⚠️ {abs(missing_closes)} extra closing div tags detected")

# ===== FIX 2: Remove leftCRITEO div if it exists =====
print("\n🎨 Removing left-side CRITEO...")
# Remove any div containing just "CRITEO" that's not part of SVG or criteo-logo class
html = re.sub(r'<div[^>]*>\s*CRITEO\s*</div>', '', html, flags=re.IGNORECASE)
print("  ✅ Removed standalone CRITEO divs")

# ===== FIX 3: Ensure Slide 12 has background =====
print("\n🖼️ Ensuring Slide 12 (Questions?) has background class...")
# Find slide 12 and add summary-slide class if missing
pattern = r'(<div class="slide"[^>]*>)\s*(<div class="slide-content"[^>]*>.*?Questions\?.*?</div>\s*</div>)'
match = re.search(pattern, html, re.DOTALL | re.IGNORECASE)
if match:
    slide_div = match.group(1)
    if 'summary-slide' not in slide_div:
        new_slide_div = slide_div.replace('class="slide"', 'class="slide summary-slide"')
        html = html.replace(slide_div, new_slide_div, 1)
        print("  ✅ Added 'summary-slide' class to Slide 12")
else:
    print("  ⚠️ Could not find Slide 12 (Questions?)")

# ===== FIX 4: Restore Appendix A if missing =====
print("\n📑 Checking for Appendix A...")
if 'APPENDIX A' not in html:
    print("  ⚠️ Appendix A missing - restoring...")
    
    appendix_a = '''    <!-- APPENDIX A -->
    <div class="slide">
        <div class="slide-content">
            <h1>Appendix A: Data Quality & Methodology Caveats</h1>
            
            <div style="margin: 30px auto; max-width: 90%;">
                <div style="background: #FFF3E0; padding: 20px; border-left: 5px solid #FF9800; border-radius: 4px; margin-bottom: 30px;">
                    <p style="margin: 0; font-size: 16px;"><strong>⚠️ IMPORTANT:</strong> All revenue estimates and competitive analysis are based on UTM parameters and available data. Actual figures may vary.</p>
                </div>

                <h2 style="font-size: 22px; margin-bottom: 20px;">Data Sources & Methodology</h2>
                
                <table style="width: 100%; border-collapse: collapse;">
                    <thead>
                        <tr style="background: #f5f5f5;">
                            <th style="padding: 12px; text-align: left; border-bottom: 2px solid #ddd;">Data Source</th>
                            <th style="padding: 12px; text-align: left; border-bottom: 2px solid #ddd;">Timeframe</th>
                            <th style="padding: 12px; text-align: left; border-bottom: 2px solid #ddd;">Confidence</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td style="padding: 10px; border-bottom: 1px solid #eee;">Internal Logs (Criteo)</td>
                            <td style="padding: 10px; border-bottom: 1px solid #eee;">Jan 2022 - Oct 2024</td>
                            <td style="padding: 10px; border-bottom: 1px solid #eee;"><span style="color: #4CAF50;">●</span> High</td>
                        </tr>
                        <tr>
                            <td style="padding: 10px; border-bottom: 1px solid #eee;">UTM Parameters</td>
                            <td style="padding: 10px; border-bottom: 1px solid #eee;">34 months</td>
                            <td style="padding: 10px; border-bottom: 1px solid #eee;"><span style="color: #FF9800;">●</span> Medium</td>
                        </tr>
                        <tr>
                            <td style="padding: 10px; border-bottom: 1px solid #eee;">Revenue Estimates</td>
                            <td style="padding: 10px; border-bottom: 1px solid #eee;">Q1 2022 - Q4 2024</td>
                            <td style="padding: 10px; border-bottom: 1px solid #eee;"><span style="color: #FF9800;">●</span> Medium (±20%)</td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>
        <div class="slide-number" style="color: #888;">APPENDIX A</div>
    </div>

'''
    
    # Insert before APPENDIX B
    appendix_b_pos = html.find('<!-- APPENDIX B')
    if appendix_b_pos > 0:
        html = html[:appendix_b_pos] + appendix_a + '\n' + html[appendix_b_pos:]
        print("  ✅ Restored Appendix A before Appendix B")
else:
    print("  ✅ Appendix A already exists")

# ===== SAVE =====
print("\n💾 Saving fixed HTML...")
with open(html_file, 'w', encoding='utf-8') as f:
    f.write(html)

print(f"✅ Saved: {len(html)} bytes")

print("\n" + "="*70)
print("✅ FINAL FIX COMPLETE!")
print("="*70)
print("\n📋 Fixed:")
print("  ✅ Closed unclosed div tags before script")
print("  ✅ Removed left-side CRITEO divs")
print("  ✅ Ensured Slide 12 has background class")
print("  ✅ Checked/restored Appendix A")
print("\n🔄 Refresh browser (Ctrl+F5) to see all fixes!")
