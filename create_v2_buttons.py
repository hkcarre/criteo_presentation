#!/usr/bin/env python3
"""
REBUILD V2: VISIBLE BUTTONS
Outputs to a NEW filename to avoid caching.
Adds clickable buttons to force navigation.
"""

import re

# READ FROM THE ALREADY CLEANED REBUILD (or the original if rebuilt was overwritten)
# We know 'output/presentation/criteo_ceo_presentation.html' is now the rebuilt one (181KB)
html_file = "output/presentation/criteo_ceo_presentation.html"
output_file = "output/presentation/criteo_ceo_presentation_v2.html"

print("="*70)
print("REBUILD V2: VISIBLE BUTTONS")
print("="*70)

with open(html_file, 'r', encoding='utf-8') as f:
    html = f.read()

# We need to inject the buttons and the improved script
# We can just replace the </body> tag
extra_ui = '''
<!-- FORCE UI CONTROLS -->
<div style="position: fixed; bottom: 20px; right: 20px; z-index: 99999; display: flex; gap: 10px; background: rgba(0,0,0,0.5); padding: 10px; border-radius: 8px;">
    <button onclick="changeSlide(-1)" style="font-size: 24px; padding: 10px 20px; cursor: pointer;">◀ PREV</button>
    <div id="slide-counter" style="color: white; font-size: 24px; align-self: center; font-family: sans-serif; min-width: 80px; text-align: center;">1 / ?</div>
    <button onclick="changeSlide(1)" style="font-size: 24px; padding: 10px 20px; cursor: pointer;">NEXT ▶</button>
</div>

<script>
console.log("🚀 V2 NAVIGATION ACTIVE");

// Global scope for button onclick
window.currentIndex = 0;
window.slides = [];

document.addEventListener('DOMContentLoaded', () => {
    window.slides = document.querySelectorAll('.slide');
    console.log("Found slides:", window.slides.length);
    
    // Update counter text
    updateCounter();

    // Show first slide
    showSlide(0);
});

function updateCounter() {
    const counter = document.getElementById('slide-counter');
    if (counter && window.slides.length > 0) {
        counter.innerText = (window.currentIndex + 1) + " / " + window.slides.length;
    }
}

function showSlide(index) {
    if (window.slides.length === 0) return;
    
    // Bounds check
    if (index < 0) index = 0;
    if (index >= window.slides.length) index = window.slides.length - 1;

    // Update visibility
    window.slides.forEach((s, i) => {
        if (i === index) {
            s.style.display = 'block';
            s.style.opacity = '1';
            s.classList.add('active');
            // Force z-index high
            s.style.zIndex = '100';
            s.style.position = 'relative'; // Ensure it flows
        } else {
            s.style.display = 'none';
            s.style.opacity = '0';
            s.classList.remove('active');
            s.style.zIndex = '0';
        }
    });

    window.currentIndex = index;
    updateCounter();
    console.log("Showing slide:", index + 1);
}

// Global wrapper for buttons
window.changeSlide = function(delta) {
    showSlide(window.currentIndex + delta);
};

// Keyboard support
document.addEventListener('keydown', (e) => {
    if (e.key === 'ArrowRight' || e.key === ' ') window.changeSlide(1);
    if (e.key === 'ArrowLeft') window.changeSlide(-1);
});
</script>
</body>
'''

# Replace closing body tag
# Also remove the previous script we added to avoid conflicts?
# The previous script was at the end.
# Let's just strip the last <script>...</script> block if possible, or just append.
# Appending is safer, the new one will overwrite global vars/listeners if needed, 
# or just coexist. But we want ours to run.
# The previous script used 'const slides', limited scope. ours uses window.slides. similar.

# Actually, the file likely has the old script.
# Let's simple Replace </body> with extra_ui
new_html = html.replace('</body>', extra_ui)

with open(output_file, 'w', encoding='utf-8') as f:
    f.write(new_html)

print(f"✅ Created: {output_file}")
print("Contains visible NEXT/PREV buttons")
