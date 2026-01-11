
import os

file_path = r"c:\Dev\entrevista\output\presentation\criteo_ceo_presentation.html"

new_slide_7_content = """        <!-- Slide 7: Recommendations Part 1 (Redesigned) -->
        <div class="slide">
            <div class="criteo-logo">
                <svg width="118px" height="24px" viewBox="0 0 118 24" xmlns="http://www.w3.org/2000/svg">
                    <g fill="#FE5000">
                        <path d="M43.1976281,21.4459962 L39.1840607,15.4933776 C39.0353783,15.2732942 38.9808302,15.0029123 39.0325546,14.7423979 C39.084279,14.4818834 39.2379847,14.2528498 39.4594687,14.1062619 C41.2977609,12.8747628 42.4508918,10.6714991 42.4508918,8.13013283 C42.4508918,3.778463 38.8101328,0.335863378 34.3241176,0.335863378 L24.6803605,0.335863378 C24.5052795,0.335863378 24.3373857,0.405490326 24.2136897,0.529396263 C24.0899938,0.6533022 24.0206515,0.821313919 24.0209444,0.996394687 L24.0209444,5.21483871 C24.0200589,5.38863747 24.1553172,5.532749 24.3288235,5.54286528 C27.592296,5.71863378 30.2131499,8.53204934 30.2131499,11.7417837 C30.2131499,14.9817457 27.5643074,17.7347059 24.3288235,17.9093548 C24.1553172,17.9194711 24.0200589,18.0635826 24.0209444,18.2373814 L24.0209444,22.3293169 C24.0209444,22.6934999 24.3161775,22.9887287 24.6803605,22.9887287 L30.2836812,22.9887287 C30.6478643,22.9887287 30.943093,22.6934999 30.943093,22.3293169 L30.943093,20.3577989 C30.943093,18.9527704 32.1566793,18.6124288 33.0847818,19.7140607 L35.4358254,22.6573435 C35.6470635,22.8710659 35.9346855,22.9919154 36.2351803,22.9932205 L42.3747628,22.9932205 C42.7425328,22.9951332 43.0810409,22.7929647 43.2537334,22.4682559 C43.4264258,22.1435471 43.4048186,21.7498556 43.1976281,21.4459962 Z" />
                    </g>
                </svg>
            </div>
            <div class="slide-content">
                <h1>Strategic Pivot: Two Levers to Secure the Core</h1>
                
                <div class="insight-box">
                    <span class="insight-number">●</span>
                    <strong>STRATEGIC IMPERATIVE:</strong> We cannot "manage" our way out of product obsolescence. We must 
                    <strong>Operationalize Defense</strong> (Squads) and <strong>Restructure Economics</strong> (SPO).
                </div>

                <div class="grid-2" style="margin-top: 40px; gap: 40px;">
                    
                    <!-- Lever 1: The Squads -->
                    <div style="background: white; border: 1px solid #eee; border-radius: 8px; box-shadow: 0 4px 12px rgba(0,0,0,0.05); overflow: hidden;">
                        <div style="background: var(--criteo-blue-dark); color: white; padding: 15px;">
                            <h3 style="margin: 0; font-size: 18px;">① Strategic Response Squads</h3>
                            <div style="font-size: 12px; opacity: 0.8; margin-top: 5px;">DEFENSIVE | IMMEDIATE</div>
                        </div>
                        <div style="padding: 20px;">
                            <p style="font-size: 14px; color: #555; margin-bottom: 20px; min-height: 40px;">
                                <strong>Problem:</strong> Top clients churn because generalist AMs cannot solve technical gaps (e.g. Travel logic).
                            </p>
                            <ul style="font-size: 13px; color: #333; line-height: 1.6;">
                                <li style="margin-bottom: 10px;"><strong>The Change:</strong> Replace AMs with cross-functional "Tiger Teams" (Sales + Product Lead + Solutions Engineer).</li>
                                <li style="margin-bottom: 10px;"><strong>The Mandate:</strong> Co-build bespoke features for Top 20 clients.</li>
                                <li><strong>The Goal:</strong> Stop the feature-gap bleeding immediately.</li>
                            </ul>
                        </div>
                    </div>

                    <!-- Lever 2: SPO -->
                    <div style="background: white; border: 1px solid #eee; border-radius: 8px; box-shadow: 0 4px 12px rgba(0,0,0,0.05); overflow: hidden;">
                        <div style="background: var(--criteo-orange); color: white; padding: 15px;">
                            <h3 style="margin: 0; font-size: 18px;">② Supply Path Optimization</h3>
                            <div style="font-size: 12px; opacity: 0.8; margin-top: 5px;">STRUCTURAL | FINANCIAL</div>
                        </div>
                        <div style="padding: 20px;">
                            <p style="font-size: 14px; color: #555; margin-bottom: 20px; min-height: 40px;">
                                <strong>Problem:</strong> "Legacy Cost" perception. Competitors underprice us by bypassing SSP fees.
                            </p>
                            <ul style="font-size: 13px; color: #333; line-height: 1.6;">
                                <li style="margin-bottom: 10px;"><strong>The Change:</strong> Force-migrate spend to Criteo Direct Bidder (cut out the middleman).</li>
                                <li style="margin-bottom: 10px;"><strong>The Mandate:</strong> 100% Fee Transparency. Pass savings to Working Media.</li>
                                <li><strong>The Goal:</strong> Neutralize Adform's price advantage permanently.</li>
                            </ul>
                        </div>
                    </div>

                </div>

                <div style="margin-top: 40px; text-align: center; background: #F5F5F5; padding: 15px; border-radius: 8px;">
                    <strong style="color: var(--criteo-blue);">Expected Impact:</strong> 
                    Churn Reduction (-40%) + Working Media Efficiency (+15%)
                </div>

            </div>
            <div class="slide-number">SLIDE 7</div>
        </div>
"""

try:
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    start_idx = -1
    end_idx = -1
    
    # Locate markers
    for i, line in enumerate(lines):
        if "<!-- Slide 7: Recommendations Part 1 -->" in line:
            start_idx = i
        if "<!-- Slide 8: Recommendations Part 2 -->" in line:
            end_idx = i
            break
            
    if start_idx != -1 and end_idx != -1:
        # Replace content
        new_lines = lines[:start_idx] + [new_slide_7_content + "\n\n"] + lines[end_idx:]
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.writelines(new_lines)
        print("Successfully replaced Slide 7.")
    else:
        print(f"Could not find markers. Start: {start_idx}, End: {end_idx}")

except Exception as e:
    print(f"Error: {e}")
