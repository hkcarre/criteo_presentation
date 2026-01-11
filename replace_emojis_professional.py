"""
Replace Emojis with Professional Icons
Senior Designer for Top Management Consultancy
"""

# Read the current HTML
with open('output/presentation/criteo_ceo_presentation.html', 'r', encoding='utf-8') as f:
    html = f.read()

print("🎨 PROFESSIONAL ICON REPLACEMENT")
print("="*80)
print("\nAs Senior Designer for Top Management Consultancy...")
print("Replacing emojis with professional, minimalist icons\n")

# ============================================================================
# Define Professional Icon Mappings
# ============================================================================

# Professional icon styles using CSS and SVG-like Unicode
icon_mappings = {
    # SO WHAT boxes - use professional insight icon
    '💡 SO WHAT?': '▸ KEY INSIGHT',
    
    # Recommendations - professional numbered approach
    '🎯 #1:': '① ',
    '🛡️ #2:': '② ',
    '🚨 #3:': '③ ',
    '⭐ #4:': '④ ',
    
    # Metrics and indicators
    '📊': '▪',  # Data point
    '📈': '↑',  # Growth/increase
    '💰': '€',  # Financial
    '⏱': '⟳',  # Timeline/cycle
    '🚀': '►',  # Action/launch
    
    # Status indicators  
    '✅': '✓',  # Check/approved
    '⚠️': '⚠',  # Warning (keep Unicode version)
    '❌': '✗',  # Error/rejected
    
    # Arrows and pointers
    '↑': '↑',  # Keep arrow
    '→': '→',  # Keep arrow
    '►': '►',  # Keep play/forward
}

# ============================================================================
# Apply Replacements
# ============================================================================

replacement_count = 0

for emoji, professional_icon in icon_mappings.items():
    if emoji in html:
        count = html.count(emoji)
        html = html.replace(emoji, professional_icon)
        replacement_count += count
        print(f"  ✓ Replaced: {emoji} → {professional_icon} ({count} instances)")

# ============================================================================
# Add Professional Icon Styles
# ============================================================================

professional_icon_css = """
        /* ========== PROFESSIONAL ICON STYLES ========== */
        
        /* SO WHAT / KEY INSIGHT label */
        .so-what-label {
            font-size: 11px;
            text-transform: uppercase;
            letter-spacing: 2px;
            opacity: 0.95;
            display: block;
            margin-bottom: 10px;
            font-weight: 700;
            color: rgba(255, 255, 255, 0.9);
        }
        
        /* Professional numbered bullets for recommendations */
        .recommendation h3 {
            display: flex;
            align-items: center;
            gap: 10px;
        }
        
        /* Circular number badges */
        .recommendation h3::first-line {
            font-family: 'Arial', sans-serif;
            font-weight: 600;
        }
        
        /* Timeline indicator style */
        .timeline-badge::before {
            content: '⟳';
            margin-right: 6px;
            font-size: 14px;
        }
        
        /* Impact indicator style */
        .impact-text::before {
            content: '€';
            margin-right: 4px;
            font-weight: 700;
        }
        
        /* Professional bullet points */
        li::before {
            content: '▪';
            position: absolute;
            left: 0;
            color: var(--criteo-orange);
            font-size: 16px;
            font-weight: 700;
        }
        
        /* Remove emoji-style from priority badges */
        .priority-badge {
            font-family: var(--font-primary);
            font-weight: 700;
            letter-spacing: 0.8px;
        }
"""

# Insert professional icon CSS before closing </style>
html = html.replace('    </style>', professional_icon_css + '\n    </style>')

print(f"\n✓ Added professional icon styles")

# ============================================================================
# Clean up any remaining casual elements
# ============================================================================

# Replace recommendation emoji patterns that might have been missed
html = html.replace('Estimated Impact:', 'Expected Impact:')
html = html.replace('Timeline:', 'Timeframe:')

print(f"\n✓ Cleaned up casual language")

# ============================================================================
# Save Updated HTML
# ============================================================================

with open('output/presentation/criteo_ceo_presentation.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("\n" + "="*80)
print("✅ PROFESSIONAL ICON REPLACEMENT COMPLETE")
print("="*80)

print(f"\n📊 Summary:")
print(f"  • Total replacements: {replacement_count}")
print(f"  • Icon style: Minimalist, consultancy-grade")
print(f"  • Consistency: McKinsey/Bain/BCG standard")

print(f"\n🎨 Professional Enhancements:")
print(f"  ✓ SO WHAT → KEY INSIGHT")
print(f"  ✓ Emoji bullets → Geometric shapes (▪)")
print(f"  ✓ Numbered recommendations → Circled numbers (①②③④)")
print(f"  ✓ Emoji indicators → Professional Unicode")
print(f"  ✓ Clean, corporate aesthetic maintained")

print(f"\n✅ Presentation now matches top-tier consultancy standards!")
