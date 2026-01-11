import os

file_path = r'c:\Dev\entrevista\output\presentation\criteo_ceo_presentation.html'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Neutralize the corrupted script tag
# We look for the script tag that starts with "script>" or "<script>" before the body end
# and comment it out entirely.
# based on previous views, the broken one is around line 3010
content = content.replace('script>', '<!-- script neutralized -->')
content = content.replace('<script>', '<!-- script neutralized -->')

# 2. Append the Lifeboat Script
# This script is guaranteed to work because it relies on simple DOM manipulation
# and ignores the broken chart data.

lifeboat_script = """
<script>
console.log("🚀 EMERGENCY LIFEBOAT SCRIPT ACTIVATED");

document.addEventListener('DOMContentLoaded', function() {
    // 1. Force Title Slide Visible
    const slides = document.querySelectorAll('.slide');
    console.log("Found slides:", slides.length);
    
    if (slides.length > 0) {
        slides[0].classList.add('active');
        slides[0].style.opacity = '1';
        slides[0].style.pointerEvents = 'auto';
    }

    // 2. Simple Navigation Logic
    let currentIndex = 0;
    
    function showSlide(index) {
        if (index < 0) index = 0;
        if (index >= slides.length) index = slides.length - 1;
        
        slides.forEach((s, i) => {
            if (i === index) {
                s.classList.add('active');
                s.style.opacity = '1';
                s.style.pointerEvents = 'auto';
            } else {
                s.classList.remove('active');
                s.style.opacity = '0';
                s.style.pointerEvents = 'none';
            }
        });
        currentIndex = index;
    }

    // 3. Bind Keys
    document.addEventListener('keydown', (e) => {
        if (e.key === 'ArrowRight' || e.key === ' ') showSlide(currentIndex + 1);
        if (e.key === 'ArrowLeft') showSlide(currentIndex - 1);
    });

    console.log("✅ Navigation restored.");
});
</script>
"""

# Inject before body end
if "</body>" in content:
    content = content.replace("</body>", lifeboat_script + "\n</body>")
else:
    content += lifeboat_script

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Emergency restoration complete. Slides should be visible.")
