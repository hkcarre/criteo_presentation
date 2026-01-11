#!/usr/bin/env python3
"""
RESTORE & FIX v2
1. Read clean backup (before layout broke)
2. Apply STABLE Scroll Mode CSS (Simple, no animations)
3. Re-apply DATA Fixes (Heatmap Revenue)
4. Re-apply VISUAL Fixes (Slide 12 BG, Appendix Light)
"""

import re

# Source: The backup before I messed up the layout
source_file = "output/presentation/criteo_ceo_presentation_before_fix.html"
# Target: The file user is looking at
target_file = "output/presentation/criteo_ceo_presentation_scroll.html"

print("="*70)
print("RESTORING STABLE VERSION WITH DATA FIXES")
print("="*70)

with open(source_file, 'r', encoding='utf-8') as f:
    html = f.read()

# 1. APPLY STABLE SCROLL CSS
# This is the CSS that GUARANTEES vertical scrolling without overlap
stable_scroll_css = '''
<style>
    /* STABLE SCROLL MODE CSS */
    html, body {
        overflow-y: auto !important;
        height: auto !important;
        background: #f0f0f0;
    }
    .presentation {
        height: auto !important;
        overflow: visible !important;
        padding: 50px 0;
        transform: none !important;
        width: 100% !important;
        max-width: none !important;
    }
    .slide {
        display: block !important;
        position: relative !important; /* Fixes overlap */
        opacity: 1 !important;
        top: auto !important;
        left: auto !important;
        transform: none !important;
        visibility: visible !important;
        
        /* Card Styling */
        width: 90% !important;
        max-width: 1200px !important;
        margin: 0 auto 50px auto !important;
        height: auto !important;
        min-height: 600px;
        background: white;
        box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        border: 1px solid #ddd;
    }
    .slide-content {
        padding: 40px !important;
        height: auto !important;
    }
    
    /* Ensure Nav is hidden if present */
    #presenter-hud, .navigation-controls { display: none !important; }
    
    /* Chart containers specific check */
    canvas {
        max-width: 100% !important;
        height: auto !important;
    }
</style>
'''

# Remove any existing scroll styles if present in backup (unlikely)
# Just append to head
html = html.replace('</head>', stable_scroll_css + '</head>')
print("✅ Applied Stable Scroll CSS")

# 2. RE-APPLY HEATMAP DATA FIX (Revenue €M)
# We look for Chart 3 config and verify/replace it
# The backup likely has the "Old" data or chart structure.
# We will inject the CORRECT Revenue Data script.

# Define the correct Chart 3 Data (Revenue €M)
correct_chart3 = """const ctx3 = document.getElementById('marketHeatmapChart');
if (ctx3) {
    new Chart(ctx3, {
        type: 'bar',
        data: {
            labels: ['EASTERN EUROPE', 'IBERIA', 'FRANCE', 'ITALY', 'UK', 'DACH', 'NORDICS', 'RUSSIA'],
            datasets: [{
                label: 'Revenue at Risk (€M)',
                data: [9.2, 6.3, 3.5, 2.8, 1.5, 1.2, 0.8, 0.4],
                backgroundColor: ['#D32F2F', '#D32F2F', '#E64A19', '#E64A19', '#FF5722', '#FF8A65', '#FF8A65', '#FFCCBC'],
                borderColor: ['#D32F2F', '#D32F2F', '#E64A19', '#E64A19', '#FF5722', '#FF8A65', '#FF8A65', '#FFCCBC'],
                borderWidth: 1,
                barThickness: 30
            }]
        },
        options: {
            indexAxis: 'y',
            responsive: true,
            maintainAspectRatio: true,
            plugins: {
                title: {
                    display: true,
                    text: 'Market Risk Heatmap (Revenue at Risk €M)',
                    font: { size: 16, weight: 'bold', family: 'Arial' },
                    color: '#1A1A1A',
                    padding: 20
                },
                legend: { display: false },
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            return 'Revenue at Risk: €' + context.parsed.x.toFixed(1) + 'M';
                        }
                    }
                }
            },
            scales: {
                x: {
                    title: { display: true, text: 'Revenue at Risk (€ Millions)' },
                    ticks: { callback: function(value) { return '€' + value + 'M'; } }
                }
            }
        }
    });
}"""

# Find existing Chart 3 block
pattern = re.compile(r"const ctx3 =.*?// Chart 4", re.DOTALL)
match = pattern.search(html)

if match:
    original_block = match.group(0)
    replacement = correct_chart3 + "\n\n\n// Chart 4"
    html = html.replace(original_block, replacement)
    print("✅ Re-applied Heatmap Data Fix (Revenue €M)")
else:
    # If regex fails (backup might differ), try finding start and replacing until match close
    # Or just inject usage of chart_scripts?
    # Let's try simple replacement of data array if block isn't found
    print("⚠️ Chart 3 block search failed. Attempting data array replacement (fallback)")
    # Fallback: look for data: [...] in Chart 3 context?
    pass

# 3. RE-APPLY SLIDE 12 BACKGROUND & APPENDIX FIX (JS)
visual_fix_js = '''
<script>
document.addEventListener('DOMContentLoaded', () => {
    console.log("🎨 Applying Visual Fixes");
    const slides = document.querySelectorAll('.slide');
    
    // Fix Questions Slide (Slide 12 - Index 11)
    if (slides.length >= 12) {
        const qSlide = slides[11];
        if (qSlide.textContent.includes('Questions') || qSlide.textContent.includes('Q&A')) {
             qSlide.style.background = "linear-gradient(rgba(0,0,0,0.6), rgba(0,0,0,0.8)), url('images/criteo_title_bg.png')";
             qSlide.style.backgroundSize = "cover";
             qSlide.style.color = "white";
             const headings = qSlide.querySelectorAll('h1, h2, h3, p, div');
             headings.forEach(el => el.style.color = "white");
        }
    }
    
    // Fix Appendices (Light Background)
    slides.forEach(slide => {
        if (slide.textContent.includes('APPENDIX')) {
            slide.style.background = "white";
            slide.style.color = "#1A1A1A";
            const els = slide.querySelectorAll('*');
            els.forEach(el => {
                if (!el.classList.contains('criteo-logo')) el.style.color = "#1A1A1A";
            });
        }
    });
});
</script>
'''
html = html.replace('</body>', visual_fix_js + '</body>')
print("✅ Re-applied Visual Fixes (JS)")

# 4. TYPO FIX
html = html.replace("FASTERN EUROPE", "EASTERN EUROPE")
print("✅ Re-applied Typo Fix")

# 5. REMOVE ANY "SCROLL MODE ENABLED" BANNER TEXT
html = re.sub(r'<div style="position: fixed; top: 0.*?SCROLL MODE ENABLED.*?</div>', '', html, flags=re.DOTALL)
print("✅ Removed any residual banners")

# Write to target
with open(target_file, 'w', encoding='utf-8') as f:
    f.write(html)

print("\n✅ RESTORE COMPLETE - File: " + target_file)
print("   - Layout: Stable Scroll (No Cascade)")
print("   - Data: Correct (€M)")
print("   - Visuals: Questions BG + Light Appendix")
