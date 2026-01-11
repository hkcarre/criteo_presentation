#!/usr/bin/env python3
"""
SENIOR DESIGNER: FINAL POLISH

1. Remove "SCROLL MODE ENABLED" banner
2. Fix Appendix backgrounds (ALL must be LIGHT)
3. Create "APPENDICES" separator slide
4. Apply premium effects
"""

import re

html_file = "output/presentation/criteo_ceo_presentation_scroll.html"

print("="*70)
print("SENIOR DESIGNER: FINAL POLISH")
print("="*70)

with open(html_file, 'r', encoding='utf-8') as f:
    html = f.read()

# 1. REMOVE SCROLL MODE BANNER
# Find and remove the banner div
banner_pattern = r'<div style="position: fixed; top: 0.*?SCROLL MODE ENABLED.*?</div>\s*<div style="height: 50px;"></div>'
html = re.sub(banner_pattern, '', html, flags=re.DOTALL)
print("✅ Removed 'SCROLL MODE ENABLED' banner")

# 2. CREATE APPENDICES SEPARATOR SLIDE
# We need to inject this BEFORE the first Appendix slide
# Find "APPENDIX A" and inject a separator slide before it

appendices_separator = '''
    <!-- APPENDICES SEPARATOR SLIDE -->
    <div class="slide" style="background: linear-gradient(135deg, #1A1A1A 0%, #2C2C2C 100%); display: flex; align-items: center; justify-content: center; text-align: center; min-height: 600px;">
        <div style="width: 100%; padding: 60px;">
            <div style="border-bottom: 6px solid var(--criteo-orange); display: inline-block; padding-bottom: 30px; margin-bottom: 40px;">
                <h1 style="font-size: 56px; color: white; font-weight: 800; letter-spacing: 3px; margin: 0;">APPENDICES</h1>
            </div>
            <p style="font-size: 20px; color: rgba(255,255,255,0.75); margin-top: 40px; font-weight: 300; letter-spacing: 1px;">
                Data Quality & Methodology
            </p>
        </div>
    </div>
'''

# Find the first appendix slide and inject separator before it
# Look for "APPENDIX A" in content
appendix_marker = re.search(r'(<div class="slide[^>]*>.*?APPENDIX A)', html, re.DOTALL)
if appendix_marker:
    # Insert separator before this slide
    insert_position = appendix_marker.start(1)
    html = html[:insert_position] + appendices_separator + '\n' + html[insert_position:]
    print("✅ Created 'APPENDICES' separator slide")
else:
    print("⚠️ Could not find Appendix A marker")

# 3. FIX APPENDIX BACKGROUNDS - FORCE LIGHT THEME
# Update the JavaScript to properly set light backgrounds

# Find the background fix script and update it
old_appendix_fix = '''    // C. ENSURE APPENDIX SLIDES ARE LIGHT (Slide 13+)
    if (slides.length >= 13) {
        for (let i = 12; i < slides.length; i++) {
            const appendixSlide = slides[i];
            appendixSlide.style.background = "white";
            appendixSlide.style.color = "#1A1A1A";
            console.log(`✅ Set Appendix slide ${i+1} to light theme`);
        }
    }'''

new_appendix_fix = '''    // C. FORCE ALL APPENDIX SLIDES TO LIGHT THEME
    // Find slides containing "APPENDIX" and force light background
    slides.forEach((slide, index) => {
        const slideText = slide.textContent || '';
        if (slideText.includes('APPENDIX')) {
            slide.style.setProperty('background', 'white', 'important');
            slide.style.setProperty('background-color', 'white', 'important');
            slide.style.setProperty('color', '#1A1A1A', 'important');
            
            // Force all child elements to dark text
            const allElements = slide.querySelectorAll('*');
            allElements.forEach(el => {
                if (!el.classList.contains('criteo-logo')) {
                    el.style.setProperty('color', '#1A1A1A', 'important');
                }
            });
            console.log(`✅ Forced slide ${index+1} to light theme (contains APPENDIX)`);
        }
    });'''

if old_appendix_fix in html:
    html = html.replace(old_appendix_fix, new_appendix_fix)
    print("✅ Updated Appendix background fix (aggressive)")
else:
    # If not found, inject it before the closing script tag
    print("⚠️ Appendix fix not found, will add new one")
    # Find the last </script> before </body>
    last_script_end = html.rfind('</script>\n</body>')
    if last_script_end > 0:
        injection_point = last_script_end
        new_script = f'''

// D. FORCE APPENDIX BACKGROUNDS (AGGRESSIVE)
const allSlides = document.querySelectorAll('.slide');
allSlides.forEach((slide, index) => {{
    const slideText = slide.textContent || '';
    if (slideText.includes('APPENDIX')) {{
        slide.style.setProperty('background', 'white', 'important');
        slide.style.setProperty('background-color', 'white', 'important');
        slide.style.setProperty('color', '#1A1A1A', 'important');
        
        const allElements = slide.querySelectorAll('*');
        allElements.forEach(el => {{
            if (!el.classList.contains('criteo-logo')) {{
                el.style.setProperty('color', '#1A1A1A', 'important');
            }}
        }});
        console.log(`✅ Forced slide ${{index+1}} to light theme`);
    }}
}});
</script>'''
        html = html[:injection_point] + new_script + html[injection_point:]

# 4. ADD PREMIUM EFFECTS (if not already added)
if 'MCKINSEY PREMIUM EFFECTS' not in html:
    premium_effects_css = '''
<style>
/* ========== MCKINSEY PREMIUM EFFECTS ========== */

/* Staggered List Animations */
li {
    opacity: 0;
    transform: translateX(-20px);
    animation: slideInList 0.6s ease-out forwards;
}

li:nth-child(1) { animation-delay: 0.1s; }
li:nth-child(2) { animation-delay: 0.2s; }
li:nth-child(3) { animation-delay: 0.3s; }
li:nth-child(4) { animation-delay: 0.4s; }
li:nth-child(5) { animation-delay: 0.5s; }
li:nth-child(n+6) { animation-delay: 0.6s; }

@keyframes slideInList {
    to {
        opacity: 1;
        transform: translateX(0);
    }
}

/* Chart Animation Enhancement */
canvas {
    opacity: 0;
    transform: scale(0.95);
    animation: chartReveal 1.2s cubic-bezier(0.34, 1.56, 0.64, 1) 0.3s forwards;
}

@keyframes chartReveal {
    to {
        opacity: 1;
        transform: scale(1);
    }
}

/* Table Rows - Smooth Highlight */
tbody tr {
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

tbody tr:hover {
    background: linear-gradient(90deg, var(--criteo-orange-pale) 0%, transparent 100%) !important;
    transform: translateX(8px) scale(1.01);
}
</style>
'''
    html = html.replace('</head>', premium_effects_css + '</head>')
    print("✅ Added Premium Effects")

# Save
with open(html_file, 'w', encoding='utf-8') as f:
    f.write(html)

print("\n" + "="*70)
print("DESIGN POLISH COMPLETE")
print("="*70)
print("\n✅ Removed scroll banner")
print("✅ Created Appendices separator")  
print("✅ Fixed Appendix backgrounds (forced light)")
print("✅ Premium effects applied")
print("\n🎨 Presentation is Executive-Ready!")
