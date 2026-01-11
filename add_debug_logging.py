#!/usr/bin/env python3
"""
Quick fix: Add debug console logging to understand what's happening
"""

import re

html_file = "output/presentation/criteo_ceo_presentation.html"

with open(html_file, 'r', encoding='utf-8') as f:
    html = f.read()

# Find the showSlide function and add detailed logging
old_script = '''function showSlide(index) {
                                            if (index < 0) index = 0;
                                            if (index >= slides.length) index = slides.length - 1;

                                            slides.forEach((s, i) => {
                                                if (i === index) {
                                                    s.classList.add('active');
                                                    s.style.display = 'block';
                                                    s.style.opacity = '1';
                                                    s.style.pointerEvents = 'auto';
                                                } else {
                                                    s.classList.remove('active');
                                                    s.style.display = 'none';
                                                    s.style.opacity = '0';
                                                    s.style.pointerEvents = 'none';
                                                }
                                            });
                                            currentIndex = index;
                                        }'''

new_script = '''function showSlide(index) {
                                            console.log("🎯 showSlide called with index:", index);
                                            if (index < 0) index = 0;
                                            if (index >= slides.length) index = slides.length - 1;
                                            console.log("📍 Adjusted index:", index, "Total slides:", slides.length);

                                            slides.forEach((s, i) => {
                                                if (i === index) {
                                                    console.log("✅ Activating slide", i, s);
                                                    s.classList.add('active');
                                                    s.style.display = 'block';
                                                    s.style.opacity = '1';
                                                    s.style.pointerEvents = 'auto';
                                                    s.style.zIndex = '1';
                                                } else {
                                                    s.classList.remove('active');
                                                    s.style.display = 'none';
                                                    s.style.opacity = '0';
                                                    s.style.pointerEvents = 'none';
                                                    s.style.zIndex = '0';
                                                }
                                            });
                                            currentIndex = index;
                                            console.log("✅ Current index now:", currentIndex);
                                        }'''

if old_script.replace(' ', '').replace('\n', '') in html.replace(' ', '').replace('\n', ''):
    html = html.replace(old_script, new_script)
    print("✅ Added debug logging to showSlide function")
else:
    print("⚠️ Could not find exact match for showSlide function")
    print("Will try approximate match...")
    # Try to find and replace the function
    pattern = r'function showSlide\(index\)[\s\S]*?currentIndex = index;\s*\}'
    match = re.search(pattern, html)
    if match:
        html = html.replace(match.group(0), new_script)
        print("✅ Replaced via regex pattern match")
    else:
        print("❌ Could not find showSlide function")

# Save
with open(html_file, 'w', encoding='utf-8') as f:
    f.write(html)

print("\n✅ Saved updated HTML with debug logging")
print("📝 Open browser console (F12) and try navigating to see what happens")
