
import os

key_slide9_start = '<!-- Slide 9: Alert System Design -->'
key_slide9_end = '<div class="slide-number">SLIDE 9</div>'

key_slide10_start = '<!-- Slide 10: Alert Implementation -->'
key_slide10_end = '<div class="slide-number">SLIDE 10</div>'

new_slide9_content = """        <!-- Slide 9: Alert System Design -->
        <div class="slide">
            <div class="criteo-logo">
                <svg width="118px" height="24px" viewBox="0 0 118 24" xmlns="http://www.w3.org/2000/svg">
                    <g fill="#FE5000">
                        <path d="M43.1976281,21.4459962 L39.1840607,15.4933776 C39.0353783,15.2732942 38.9808302,15.0029123 39.0325546,14.7423979 C39.084279,14.4818834 39.2379847,14.2528498 39.4594687,14.1062619 C41.2977609,12.8747628 42.4508918,10.6714991 42.4508918,8.13013283 C42.4508918,3.778463 38.8101328,0.335863378 34.3241176,0.335863378 L24.6803605,0.335863378 C24.5052795,0.335863378 24.3373857,0.405490326 24.2136897,0.529396263 C24.0899938,0.6533022 24.0206515,0.821313919 24.0209444,0.996394687 L24.0209444,5.21483871 C24.0200589,5.38863747 24.1553172,5.532749 24.3288235,5.54286528 C27.592296,5.71863378 30.2131499,8.53204934 30.2131499,11.7417837 C30.2131499,14.9817457 27.5643074,17.7347059 24.3288235,17.9093548 C24.1553172,17.9194711 24.0200589,18.0635826 24.0209444,18.2373814 L24.0209444,22.3293169 C24.0209444,22.6934999 24.3161775,22.9887287 24.6803605,22.9887287 L30.2836812,22.9887287 C30.6478643,22.9887287 30.943093,22.6934999 30.943093,22.3293169 L30.943093,20.3577989 C30.943093,18.9527704 32.1566793,18.6124288 33.0847818,19.7140607 L35.4358254,22.6573435 C35.6470635,22.8710659 35.9346855,22.9919154 36.2351803,22.9932205 L42.3747628,22.9932205 C42.7425328,22.9951332 43.0810409,22.7929647 43.2537334,22.4682559 C43.4264258,22.1435471 43.4048186,21.7498556 43.1976281,21.4459962 Z" />
                        <path d="M46.2718975,0.324667932 L51.128482,0.324667932 C51.4928461,0.325285499 51.7878937,0.620834635 51.7878937,0.985199241 L51.7878937,22.3214801 C51.7878937,22.6856631 51.492665,22.9808918 51.128482,22.9808918 L46.2718975,22.9808918 C45.9075329,22.9808918 45.6119838,22.6858442 45.6113662,22.3214801 L45.6113662,0.985199241 C45.6113662,0.620397872 45.9070962,0.324667932 46.2718975,0.324667932 Z" />
                        <path d="M59.6717268,5.91567362 L54.5542884,5.91567362 C54.1922803,5.91568667 53.8979497,5.62385471 53.8948767,5.26185958 L53.8948767,0.985199241 C53.8948767,0.620834635 54.1899243,0.325285499 54.5542884,0.324667932 L71.503074,0.324667932 C71.8674381,0.325285499 72.1624858,0.620834635 72.1624858,0.985199241 L72.1624858,5.26185958 C72.1624858,5.62604264 71.8672571,5.92127135 71.503074,5.92127135 L66.5110247,5.92127135 C66.3303163,5.92486171 66.1848553,6.07081746 66.1818786,6.251537 L66.1818786,22.3214801 C66.1818786,22.6856631 65.8866499,22.9808918 65.5224668,22.9808918 L60.6658824,22.9808918 C60.3015177,22.9808918 60.0059686,22.6858442 60.005351,22.3214801 L60.005351,6.24593928 C60.0023139,6.0635047 59.8541827,5.91686474 59.6717268,5.91567362 Z" />
                        <path d="M75.0229222,0.324667932 L90.4110626,0.324667932 C90.7754267,0.325285499 91.0704749,0.620834635 91.0704744,0.985199241 L91.0704744,5.22379507 C91.0704744,5.39868194 91.0010008,5.5664059 90.8773371,5.6900696 C90.7536735,5.81373329 90.5859495,5.88320683 90.4110626,5.88320683 L80.8691841,5.88320683 C80.6836918,5.88320683 80.5333207,6.03357799 80.5333207,6.21907021 L80.5333207,8.68206831 C80.5333023,8.77053969 80.5689006,8.85529359 80.632088,8.91721724 C80.6952754,8.97914089 80.7807311,9.01301996 80.8691841,9.01121442 L89.7281404,9.01121442 C90.0925045,9.01183199 90.3875527,9.30738112 90.3875522,9.67174573 L90.3875522,13.4233397 C90.3875522,13.7875227 90.0923235,14.0827514 89.7281404,14.0827514 L80.8691841,14.0827514 C80.6862837,14.0827148 80.5369787,14.2290338 80.5333207,14.4118975 L80.5333207,17.198444 C80.5369787,17.3813078 80.6862837,17.5276267 80.8691841,17.5275901 L90.670797,17.5275901 C91.035161,17.5282077 91.3302087,17.8237568 91.3302087,18.1881214 L91.3302087,22.3304364 C91.3302087,22.6946195 91.03498,22.9898482 90.670797,22.9898482 L75.0229222,22.9898482 C74.6587391,22.9898482 74.3635095,22.6946195 74.3635095,22.3304364 L74.3635095,0.985199241 C74.3632132,0.810118473 74.4325555,0.642106754 74.5562514,0.518200817 C74.6799473,0.39429488 74.8478412,0.324667932 75.0229222,0.324667932 Z" />
                        <path d="M105.427514,0 C98.5042505,0 92.9457116,5.26185958 92.9457116,11.7339469 C92.9457116,18.2060342 98.5042505,23.4365465 105.427514,23.4365465 C112.383245,23.4365465 117.941784,18.2026755 117.941784,11.7339469 C117.941784,5.26521822 112.383245,0 105.427514,0 Z M105.427514,17.9127397 C103.78804,17.9174907 102.214354,17.2682496 101.055171,16.1088564 C99.8959877,14.9494631 99.2470318,13.3756591 99.2520767,11.736186 C99.2520767,8.38874763 102.015142,5.5283112 105.427514,5.5283112 C108.839886,5.5283112 111.636517,8.42121442 111.636517,11.736186 C111.642106,15.0825047 108.819734,17.9127397 105.433112,17.9127397 L105.427514,17.9127397 Z" />
                    </g>
                </svg>
            </div>
            <div class="slide-content">
                <h1>The Radar System: 4 Pillars of Early Detection</h1>

                <!-- Quad Chart Layout -->
                <div class="grid-2" style="gap: 30px; margin-top: 20px;">
                    
                    <!-- Quadrant 1: Metrics -->
                    <div>
                        <h3 style="color: var(--criteo-blue); border-bottom: 2px solid var(--criteo-orange); padding-bottom: 5px;">(A) Core Metrics</h3>
                        <ul style="font-size: 14px; line-height: 1.6;">
                            <li><strong>Competitor First Touch:</strong> Instant alert when a competitor pixel fires (0 -> 1).</li>
                            <li><strong>Click Share Delta:</strong> MoM change in Share of Voice.</li>
                            <li><strong>Revenue Velocity:</strong> 3-month rolling revenue trend (health proxy).</li>
                        </ul>
                    </div>

                    <!-- Quadrant 2: Logic & Thresholds -->
                    <div>
                        <h3 style="color: var(--criteo-blue); border-bottom: 2px solid var(--criteo-orange); padding-bottom: 5px;">(B) Decision Logic</h3>
                        <div style="font-size: 13px; background: var(--criteo-orange-pale); padding: 10px; border-radius: 4px; margin-bottom: 5px;">
                            <strong>🔥 P1 CRITICAL (24h SLA):</strong><br>
                            High-Value Client (>€100k) + (First Touch OR Share Delta > 5%)
                        </div>
                        <div style="font-size: 13px; background: #f5f5f5; padding: 10px; border-radius: 4px;">
                            <strong>⚠ P2 MONITOR (72h SLA):</strong><br>
                            Mid-Market + (Share > 10% OR Revenue Drop > 10%)
                        </div>
                    </div>

                    <!-- Quadrant 3: Delivery -->
                    <div>
                        <h3 style="color: var(--criteo-blue); border-bottom: 2px solid var(--criteo-orange); padding-bottom: 5px;">(C) Delivery Channels</h3>
                        <table style="font-size: 13px; width: 100%;">
                            <tr>
                                <td><strong>P1 Alerts:</strong></td>
                                <td>Slack (Instant) + Email to VP Sales</td>
                            </tr>
                            <tr>
                                <td><strong>P2 Alerts:</strong></td>
                                <td>Daily Digest Email to Account Mgr</td>
                            </tr>
                            <tr>
                                <td><strong>Dashboards:</strong></td>
                                <td>Embedded in Salesforce (Account View)</td>
                            </tr>
                        </table>
                    </div>

                    <!-- Quadrant 4: Effectiveness -->
                    <div>
                        <h3 style="color: var(--criteo-blue); border-bottom: 2px solid var(--criteo-orange); padding-bottom: 5px;">(D) Success Measures</h3>
                         <ul style="font-size: 14px; line-height: 1.6;">
                            <li><strong>Precision:</strong> >75% of alerts result in Verified Threat.</li>
                            <li><strong>Response Time:</strong> < 24 Hours for P1s.</li>
                            <li><strong>Retention Impact:</strong> €5M+ Revenue Saved / Year.</li>
                        </ul>
                    </div>

                </div>

                <div class="so-what-box" style="margin-top: 30px;">
                    <span class="so-what-label">▸ SYSTEM GOAL</span>
                    Move from "Post-Mortem" analysis (3 months late) to "Real-Time Intervention" (24 hours).
                </div>

            </div>
            <div class="slide-number">SLIDE 9</div>
        </div>
"""

path = 'output/presentation/criteo_ceo_presentation.html'

with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Find Start/End of Slide 9
start_idx_9 = content.find(key_slide9_start)
end_idx_9 = content.find(key_slide9_end) + len(key_slide9_end) + len('</div>') + 10 # approximate buffer to include closing div

# Finding the actual closing </div> for the slide might be safer by string search from end
# Looking at the code: <div class="slide"> ... <div class="slide-number">SLIDE 9</div> \n </div>
# So we can search for the closing div after the slide number.

end_idx_9 = content.find('</div>', content.find(key_slide9_end)) + len('</div>')

if start_idx_9 == -1:
    print("Error: Slide 9 not found")
    exit(1)

# 2. Find Start/End of Slide 10
start_idx_10 = content.find(key_slide10_start)
end_idx_10 = content.find(key_slide10_end) 
if start_idx_10 != -1:
    end_idx_10 = content.find('</div>', end_idx_10) + len('</div>')
else:
    print("Warning: Slide 10 not found (maybe already deleted?)")

# 3. Construct new content
# Everything before Slide 9 + New Slide 9 + Everything after Slide 9 (but skipping Slide 10)

part1 = content[:start_idx_9]
part2 = new_slide9_content
part3 = content[end_idx_9:start_idx_10] # The space between slides
part4 = content[end_idx_10:] # Everything after Slide 10

# If slide 10 wasn't found, just append the rest
if start_idx_10 == -1:
    final_content = part1 + part2 + content[end_idx_9:]
else:
    final_content = part1 + part2 + part3 + part4

with open(path, 'w', encoding='utf-8') as f:
    f.write(final_content)

print("✅ Slide 9 updated and Slide 10 removed.")
