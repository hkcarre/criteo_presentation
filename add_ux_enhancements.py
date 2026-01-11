"""
Add smooth transitions, animations, and interactive elements
Senior Designer + UX Expert approach
"""

# Read the current HTML
with open('output/presentation/criteo_ceo_presentation.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Advanced CSS for smooth transitions and animations
advanced_css = """
        /* ========== SMOOTH TRANSITIONS & ANIMATIONS ========== */
        
        /* Smooth scroll behavior */
        html {
            scroll-behavior: smooth;
        }
        
        /* Slide fade-in animation */
        .slide {
            opacity: 0;
            transform: translateY(30px);
            animation: slideIn 0.8s ease-out forwards;
        }
        
        @keyframes slideIn {
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        
        /* Stagger slide animations */
        .slide:nth-child(1) { animation-delay: 0s; }
        .slide:nth-child(2) { animation-delay: 0.1s; }
        .slide:nth-child(3) { animation-delay: 0.2s; }
        .slide:nth-child(n+4) { animation-delay: 0.3s; }
        
        /* Metric boxes - scale on hover */
        .metric-box {
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            cursor: pointer;
        }
        
        .metric-box:hover {
            transform: translateY(-8px) scale(1.03);
            box-shadow: 0 12px 24px rgba(255, 87, 34, 0.25);
        }
        
        /* Metric values - count-up animation */
        .metric-value {
            display: inline-block;
            transition: color 0.3s ease;
        }
        
        .metric-box:hover .metric-value {
            color: var(--criteo-orange);
        }
        
        /* SO WHAT boxes - slide in from left */
        .so-what-box {
            animation: slideInLeft 0.6s ease-out;
        }
        
        @keyframes slideInLeft {
            from {
                opacity: 0;
                transform: translateX(-50px);
            }
            to {
                opacity: 1;
                transform: translateX(0);
            }
        }
        
        /* Tables - smooth row highlight */
        tr {
            transition: all 0.2s ease;
        }
        
        tr:hover {
            background: var(--criteo-orange-pale) !important;
            transform: translateX(5px);
        }
        
        /* Recommendation cards - lift effect */
        .recommendation {
            transition: all 0.3s ease;
            cursor: pointer;
        }
        
        .recommendation:hover {
            transform: translateX(10px);
            box-shadow: -5px 0 15px rgba(255, 87, 34, 0.2);
            border-left-width: 10px;
        }
        
        /* Buttons and badges - pulse effect */
        .priority-badge {
            transition: all 0.3s ease;
        }
        
        .priority-badge:hover {
            transform: scale(1.1);
            box-shadow: 0 4px 12px rgba(255, 87, 34, 0.4);
        }
        
        /* Timeline badges - grow effect */
        .timeline-badge {
            transition: all 0.25s ease;
        }
        
        .timeline-badge:hover {
            transform: scale(1.05);
            background: var(--criteo-orange);
            color: white;
        }
        
        /* Progress indicator */
        .progress-bar {
            position: fixed;
            top: 0;
            left: 0;
            width: 0%;
            height: 4px;
            background: linear-gradient(90deg, var(--criteo-orange), var(--criteo-blue));
            z-index: 9999;
            transition: width 0.3s ease;
            box-shadow: 0 2px 8px rgba(255, 87, 34, 0.5);
        }
        
        /* Floating back-to-top button */
        .back-to-top {
            position: fixed;
            bottom: 40px;
            right: 40px;
            width: 50px;
            height: 50px;
            background: var(--criteo-orange);
            color: white;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 20px;
            cursor: pointer;
            opacity: 0;
            transform: translateY(100px);
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            box-shadow: 0 4px 20px rgba(255, 87, 34, 0.4);
            z-index: 9998;
        }
        
        .back-to-top.visible {
            opacity: 1;
            transform: translateY(0);
        }
        
        .back-to-top:hover {
            transform: translateY(-5px);
            box-shadow: 0 8px 30px rgba(255, 87, 34, 0.6);
            background: var(--criteo-orange-dark);
        }
        
        /* Slide number - pulse on hover */
        .slide-number {
            transition: all 0.3s ease;
        }
        
        .slide-number:hover {
            color: var(--criteo-orange);
            transform: scale(1.2);
        }
        
        /* Logo - subtle rotation on hover */
        .criteo-logo svg {
            transition: transform 0.5s ease;
        }
        
        .criteo-logo:hover svg {
            transform: scale(1.05);
        }
        
        /* Insight boxes - expand on hover */
        .insight-box {
            transition: all 0.3s ease;
            cursor: pointer;
        }
        
        .insight-box:hover {
            transform: translateX(10px);
            background: var(--criteo-orange-pale);
            border-left-width: 8px;
        }
        
        /* Alert boxes - shake attention */
        .alert-box {
            transition: all 0.3s ease;
        }
        
        .alert-box:hover {
            animation: shake 0.5s ease;
        }
        
        @keyframes shake {
            0%, 100% { transform: translateX(0); }
            25% { transform: translateX(-5px); }
            75% { transform: translateX(5px); }
        }
        
        /* Chart containers - fade in */
        canvas {
            opacity: 0;
            animation: fadeIn 1s ease-out 0.5s forwards;
        }
        
        @keyframes fadeIn {
            to { opacity: 1; }
        }
        
        /* Text selection */
        ::selection {
            background: var(--criteo-orange-pale);
            color: var(--criteo-black);
        }
        
        /* Summary highlight - pulse */
        .summary-highlight {
            animation: pulse 2s ease-in-out infinite;
        }
        
        @keyframes pulse {
            0%, 100% { transform: scale(1); }
            50% { transform: scale(1.02); }
        }
        
        /* Smooth transitions for all interactive elements */
        h1, h2, h3, li, p, strong {
            transition: color 0.2s ease;
        }
        
        /* Loading animation for slow connections */
        @keyframes shimmer {
            0% { background-position: -1000px 0; }
            100% { background-position: 1000px 0; }
        }
        
        /* Responsive touch feedback */
        @media (hover: none) {
            .metric-box:active {
                transform: scale(0.98);
            }
            
            .recommendation:active {
                transform: translateX(5px);
            }
        }
        
        /* Print optimization */
        @media print {
            .progress-bar,
            .back-to-top {
                display: none !important;
            }
            
            .slide {
                opacity: 1 !important;
                transform: none !important;
                animation: none !important;
            }
        }
</style>"""

# Replace closing </style> tag with advanced CSS + closing tag
html = html.replace('    </style>', advanced_css)

# JavaScript for interactive features
interactive_js = """
<script>
// ========== INTERACTIVE FEATURES ==========

document.addEventListener('DOMContentLoaded', function() {
    
    // 1. Progress Bar
    const progressBar = document.createElement('div');
    progressBar.className = 'progress-bar';
    document.body.prepend(progressBar);
    
    window.addEventListener('scroll', function() {
        const windowHeight = document.documentElement.scrollHeight - window.innerHeight;
        const scrolled = (window.scrollY / windowHeight) * 100;
        progressBar.style.width = scrolled + '%';
    });
    
    // 2. Back to Top Button
    const backToTop = document.createElement('div');
    backToTop.className = 'back-to-top';
    backToTop.innerHTML = '↑';
    backToTop.title = 'Back to Top';
    document.body.appendChild(backToTop);
    
    window.addEventListener('scroll', function() {
        if (window.scrollY > 500) {
            backToTop.classList.add('visible');
        } else {
            backToTop.classList.remove('visible');
        }
    });
    
    backToTop.addEventListener('click', function() {
        window.scrollTo({
            top: 0,
            behavior: 'smooth'
        });
    });
    
    // 3. Count-up animation for metrics
    const animateValue = (element, start, end, duration) => {
        let startTimestamp = null;
        const step = (timestamp) => {
            if (!startTimestamp) startTimestamp = timestamp;
            const progress = Math.min((timestamp - startTimestamp) / duration, 1);
            
            // Handle percentages and numbers
            const isPercentage = element.textContent.includes('%');
            const current = progress * (end - start) + start;
            
            if (isPercentage) {
                element.textContent = current.toFixed(2) + '%';
            } else if (element.textContent.includes('€')) {
                element.textContent = '€' + current.toFixed(1) + 'M';
            } else if (element.textContent.includes(',')) {
                element.textContent = Math.round(current).toLocaleString();
            } else {
                element.textContent = Math.round(current);
            }
            
            if (progress < 1) {
                window.requestAnimationFrame(step);
            }
        };
        window.requestAnimationFrame(step);
    };
    
    // Observe metric values and animate when visible
    const metricObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting && !entry.target.dataset.animated) {
                const text = entry.target.textContent;
                const value = parseFloat(text.replace(/[^0-9.]/g, ''));
                
                if (!isNaN(value) && value > 0) {
                    entry.target.dataset.animated = 'true';
                    animateValue(entry.target, 0, value, 1500);
                }
            }
        });
    }, { threshold: 0.5 });
    
    document.querySelectorAll('.metric-value').forEach(el => {
        metricObserver.observe(el);
    });
    
    // 4. Keyboard navigation
    document.addEventListener('keydown', function(e) {
        if (e.key === 'ArrowDown' || e.key === 'PageDown' || e.key === ' ') {
            e.preventDefault();
            window.scrollBy({ top: window.innerHeight, behavior: 'smooth' });
        } else if (e.key === 'ArrowUp' || e.key === 'PageUp') {
            e.preventDefault();
            window.scrollBy({ top: -window.innerHeight, behavior: 'smooth' });
        } else if (e.key === 'Home') {
            e.preventDefault();
            window.scrollTo({ top: 0, behavior: 'smooth' });
        } else if (e.key === 'End') {
            e.preventDefault();
            window.scrollTo({ top: document.documentElement.scrollHeight, behavior: 'smooth' });
        }
    });
    
    // 5. Slide indicator (current slide)
    const slides = document.querySelectorAll('.slide');
    const slideObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const slideNum = entry.target.querySelector('.slide-number');
                if (slideNum) {
                    console.log('📍 Current:', slideNum.textContent);
                }
            }
        });
    }, { threshold: 0.5 });
    
    slides.forEach(slide => slideObserver.observe(slide));
    
    // 6. Enhanced tooltips for charts
    setTimeout(() => {
        if (typeof Chart !== 'undefined') {
            Chart.defaults.plugins.tooltip.animation = {
                duration: 400,
                easing: 'easeOutQuart'
            };
        }
    }, 100);
    
    // 7. Metric box click feedback
    document.querySelectorAll('.metric-box').forEach(box => {
        box.addEventListener('click', function() {
            this.style.transform = 'scale(0.95)';
            setTimeout(() => {
                this.style.transform = '';
            }, 200);
        });
    });
    
    // 8. Smooth anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({ behavior: 'smooth', block: 'start' });
            }
        });
    });
    
    console.log('✨ Interactive features activated!');
    console.log('📱 Keyboard shortcuts: ↑↓ arrows, Space, PageUp/Down, Home/End');
});
</script>
"""

# Add interactive JS before the closing </body> tag, but after chart scripts
html = html.replace('</body>', interactive_js + '\n</body>')

# Save enhanced HTML
with open('output/presentation/criteo_ceo_presentation.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("✨ Interactive enhancements added!")
print("\n🎨 Design Enhancements:")
print("  ✓ Smooth slide fade-in animations")
print("  ✓ Metric boxes scale on hover")
print("  ✓ Count-up number animations")
print("  ✓ Table row highlights")
print("  ✓ Recommendation card lift effects")
print("  ✓ Button pulse animations")
print("\n⚡ Interactive Features:")
print("  ✓ Progress bar (top of page)")
print("  ✓ Back-to-top button (bottom right)")
print("  ✓ Keyboard navigation (↑↓ arrows, Space)")
print("  ✓ Smooth scrolling")
print("  ✓ Auto-animated metric values")
print("  ✓ Enhanced chart tooltips")
print("\n✅ UX Excellence achieved!")
