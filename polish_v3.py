#!/usr/bin/env python3
"""
POLISH V3: 
1. Fix Typo (FASTERN -> EASTERN)
2. Add IntersectionObserver for elegant Scroll Transitions
3. Force Background on Slide 12 using JS (reliable)
"""

html_file = "output/presentation/criteo_ceo_presentation_scroll.html"

print("="*70)
print("FINAL DESIGN POLISH")
print("="*70)

with open(html_file, 'r', encoding='utf-8') as f:
    html = f.read()

# 1. FIX TYPO
html = html.replace("FASTERN EUROPE", "EASTERN EUROPE")
print("✅ Fixed Typo: EASTERN EUROPE")

# 2. ADD SCROLL ANIMATIONS (CSS + JS)
# CSS for animation
animation_css = '''
<style>
    /* SCROLL ANIMATION STYLES */
    .slide {
        opacity: 0;
        transform: translateY(40px);
        transition: opacity 0.8s ease-out, transform 0.8s ease-out;
        will-change: opacity, transform;
    }
    
    .slide.is-visible {
        opacity: 1;
        transform: translateY(0);
    }
    
    /* Ensure first slide is visible immediately */
    .slide:nth-child(1) {
        opacity: 1;
        transform: translateY(0);
    }
</style>
'''

# JS for IntersectionObserver and Background Fix
animation_js = '''
<script>
document.addEventListener('DOMContentLoaded', () => {
    // A. SCROLL ANIMATIONS
    const observerOptions = {
        root: null,
        rootMargin: '0px',
        threshold: 0.15 // Trigger when 15% visible
    };

    const observer = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('is-visible');
                // Optional: Stop observing once visible? 
                // observer.unobserve(entry.target); 
                // Keeping it allows re-animating if we wanted, but standard is "reveal once"
                // Let's keep it simple: add class, don't remove.
            }
        });
    }, observerOptions);

    document.querySelectorAll('.slide').forEach(slide => {
        observer.observe(slide);
    });

    // B. FIX SLIDE 12 BACKGROUND (Questions Slide)
    // We target the 12th slide (index 11)
    const slides = document.querySelectorAll('.slide');
    if (slides.length >= 12) {
        const qSlide = slides[11]; // Slide 12
        console.log("🎨 Applying background to Slide 12");
        
        // Apply Criteo Title Background
        qSlide.style.background = "linear-gradient(rgba(0,0,0,0.6), rgba(0,0,0,0.8)), url('images/criteo_title_bg.png')";
        qSlide.style.backgroundSize = "cover";
        qSlide.style.backgroundPosition = "center";
        qSlide.style.color = "white";
        
        // Ensure text contrast
        const headings = qSlide.querySelectorAll('h1, h2, h3, p, div');
        headings.forEach(el => el.style.color = "white");
    } else {
        console.warn("⚠️ Could not find Slide 12");
    }
});
</script>
'''

# Inject CSS
html = html.replace('</head>', animation_css + '</head>')
# Inject JS (at end)
html = html.replace('</body>', animation_js + '</body>')

with open(html_file, 'w', encoding='utf-8') as f:
    f.write(html)

print("✅ Added Scroll Animations (IntersectionObserver)")
print("✅ Injected Slide 12 Background Fix")
