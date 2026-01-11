#!/usr/bin/env python3
"""
CRITICAL FIX: Replace navigation to only use slides with slide-content
This will filter the 44 divs down to only the ~17 real slides
"""

import re

html_file = "output/presentation/criteo_ceo_presentation.html"

print("="*70)
print("CRITICAL NAVIGATION FIX")
print("="*70)

with open(html_file, 'r', encoding='utf-8') as f:
    html = f.read()

# Find the EMERGENCY LIFEBOAT SCRIPT section
script_start = html.find('console.log("🚀 EMERGENCY LIFEBOAT SCRIPT ACTIVATED");')
script_end = html.find('</script>', script_start)

if script_start == -1 or script_end == -1:
    print("ERROR: Could not find the navigation script")
    exit(1)

print("✅ Found navigation script")

# Create new script that filters to only real slides
new_script = '''console.log("🚀 EMERGENCY LIFEBOAT SCRIPT ACTIVATED - FILTERED VERSION");

                                    document.addEventListener('DOMContentLoaded', function () {
                                        // 1. Get ALL slide divs, then filter to only those with slide-content
                                        const allSlides = document.querySelectorAll('.slide');
                                        console.log("Found total divs with .slide class:", allSlides.length);
                                        
                                        // Filter to only slides that have .slide-content as a direct child
                                        const slides = Array.from(allSlides).filter(slide => {
                                            return slide.querySelector(':scope > .slide-content') !== null;
                                        });
                                        
                                        console.log("✅ Filtered to slides with content:", slides.length);

                                        if (slides.length === 0) {
                                            console.error("❌ No slides with content found!");
                                            return;
                                        }

                                        // 2. Force first slide visible
                                        slides[0].classList.add('active');
                                        slides[0].style.display = 'block';
                                        slides[0].style.opacity = '1';
                                        slides[0].style.pointerEvents = 'auto';
                                        slides[0].style.zIndex = '10';

                                        // 3. Navigation Logic
                                        let currentIndex = 0;

                                        function showSlide(index) {
                                            console.log("🎯 Navigating to slide:", index + 1, "of", slides.length);
                                            
                                            if (index < 0) index = 0;
                                            if (index >= slides.length) index = slides.length - 1;

                                            slides.forEach((s, i) => {
                                                if (i === index) {
                                                    s.classList.add('active');
                                                    s.style.display = 'block';
                                                    s.style.opacity = '1';
                                                    s.style.pointerEvents = 'auto';
                                                    s.style.zIndex = '10';
                                                } else {
                                                    s.classList.remove('active');
                                                    s.style.display = 'none';
                                                    s.style.opacity = '0';
                                                    s.style.pointerEvents = 'none';
                                                    s.style.zIndex = '0';
                                                }
                                            });
                                            
                                            currentIndex = index;
                                            console.log("✅ Now on slide", currentIndex + 1);
                                        }

                                        // 4. Bind Keys
                                        document.addEventListener('keydown', (e) => {
                                            if (e.key === 'ArrowRight' || e.key === ' ') {
                                                e.preventDefault();
                                                showSlide(currentIndex + 1);
                                            }
                                            if (e.key === 'ArrowLeft') {
                                                e.preventDefault();
                                                showSlide(currentIndex - 1);
                                            }
                                            if (e.key === 'Home') {
                                                e.preventDefault();
                                                showSlide(0);
                                            }
                                            if (e.key === 'End') {
                                                e.preventDefault();
                                                showSlide(slides.length - 1);
                                            }
                                        });

                                        console.log("✅ Navigation ready. Total slides:", slides.length);
                                        console.log("📍 Use → and ← arrows to navigate");
                                    });
                                '''

# Replace the old script content
old_script_content = html[script_start:script_end]
html = html.replace(old_script_content, new_script)

# Save
with open(html_file, 'w', encoding='utf-8') as f:
    f.write(html)

print("\n✅ SAVED FIXED VERSION")
print("="*70)
print("\nCHANGES:")
print("  • Filters 44 divs → only slides with <div class='slide-content'>")
print("  • Should now show ~17 real slides")
print("  • Added Home/End key support")
print("  • Better console logging")
print("\nTEST NOW:")
print("  1. Open in browser")
print("  2. Hard refresh (Ctrl+Shift+R)")
print("  3. Press → arrow")
print("  4. Should navigate to Slide 2!")
print("="*70)
