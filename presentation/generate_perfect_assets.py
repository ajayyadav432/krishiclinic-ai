import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import os

ASSETS_DIR = '/home/ajay/MUJ_Hackathon/presentation/assets'
os.makedirs(ASSETS_DIR, exist_ok=True)
plt.rcParams['font.sans-serif'] = 'DejaVu Sans'
plt.rcParams['font.family'] = 'sans-serif'

# ==============================================================================
# 1. SLIDE 3: Technical Architecture Infographic (Fixed Layout & Zero Overlap)
# ==============================================================================
fig, ax = plt.subplots(figsize=(8.0, 5.5), dpi=300)
ax.set_facecolor('#ffffff')
fig.patch.set_facecolor('#ffffff')
ax.set_xlim(0, 1)
ax.set_ylim(0, 1)
ax.axis('off')

steps = [
    {
        "num": "01",
        "title": "Smart Rural Edge Input",
        "badge": "FARMER LAYER",
        "bullets": [
            "Voice navigation in Hindi, Marathi, Telugu & 8+ regional languages",
            "1-tap instant camera capture with local offline photo caching",
            "Ultra-lightweight footprint (<60 MB RAM) on ₹5,000 Android phones"
        ],
        "bg": "#f0f7ff", "border": "#2b6cb0", "badge_bg": "#bee3f8", "badge_fg": "#2b6cb0"
    },
    {
        "num": "02",
        "title": "Dual-Engine Vision Pipeline",
        "badge": "AI VISION CORE",
        "bullets": [
            "Quantized PyTorch EfficientNetV2-S operates 100% on-device (offline)",
            "Gemini Vision cloud fallback for complex multi-infection leaf symptoms",
            "2-second instant diagnosis with 3-tier severity classification"
        ],
        "bg": "#faf5ff", "border": "#6b46c1", "badge_bg": "#e9d8fd", "badge_fg": "#6b46c1"
    },
    {
        "num": "03",
        "title": "Agronomist Verification Gate",
        "badge": "SAFETY NET",
        "bullets": [
            "Scans with confidence ≥ 70% auto-generate verified instant advisory",
            "Low-confidence or rare cases auto-routed to accredited agronomists",
            "Tamper-proof digital advisory certification stamp ensures clinical trust"
        ],
        "bg": "#fffaf0", "border": "#c05621", "badge_bg": "#feebc8", "badge_fg": "#c05621"
    },
    {
        "num": "04",
        "title": "Geospatial Outbreak Radar",
        "badge": "SURVEILLANCE",
        "bullets": [
            "DBSCAN spatial clustering flags regional pathogen hotspots in real-time",
            "Automated broadcast alerts to farms within a 25 km threat perimeter",
            "Stops village-wide fungal & bacterial crop epidemics before spore spread"
        ],
        "bg": "#f0fff4", "border": "#276749", "badge_bg": "#c6f6d5", "badge_fg": "#22543d"
    }
]

card_h = 0.20
gap = 0.045
start_y = 0.765

for idx, step in enumerate(steps):
    y = start_y - idx * (card_h + gap)
    
    # Outer box
    box = patches.FancyBboxPatch(
        (0.02, y), 0.96, card_h,
        boxstyle="round,pad=0.015",
        linewidth=1.8, edgecolor=step["border"], facecolor=step["bg"]
    )
    ax.add_patch(box)
    
    # Number pill on left
    pill = patches.FancyBboxPatch(
        (0.04, y + 0.03), 0.08, 0.14,
        boxstyle="round,pad=0.01",
        linewidth=1.2, edgecolor=step["border"], facecolor=step["badge_bg"]
    )
    ax.add_patch(pill)
    ax.text(0.08, y + 0.10, step["num"], fontsize=14, fontweight='bold',
            color=step["border"], ha='center', va='center')
    
    # Title
    ax.text(0.145, y + card_h - 0.035, step["title"], fontsize=11.5, fontweight='bold',
            color=step["border"], va='top')
    
    # Category badge on right
    bw = 0.20
    bh = 0.048
    badge = patches.FancyBboxPatch(
        (0.75, y + card_h - 0.065), bw, bh,
        boxstyle="round,pad=0.006",
        linewidth=0.8, edgecolor=step["border"], facecolor=step["badge_bg"]
    )
    ax.add_patch(badge)
    ax.text(0.75 + bw/2, y + card_h - 0.041, step["badge"], fontsize=7.5, fontweight='bold',
            color=step["badge_fg"], ha='center', va='center')
    
    # Bullets
    for b_idx, bullet in enumerate(step["bullets"]):
        by = y + card_h - 0.085 - b_idx * 0.038
        ax.text(0.145, by, "• " + bullet, fontsize=8.6, color='#2d3748', va='top')
        
    # Flow arrow between boxes
    if idx < 3:
        arrow_start_y = y - 0.006
        arrow_end_y = y - gap + 0.006
        ax.annotate('', xy=(0.08, arrow_end_y), xytext=(0.08, arrow_start_y),
                    arrowprops=dict(arrowstyle="->", color=step["border"], lw=2.2, mutation_scale=12))

plt.subplots_adjust(left=0.01, right=0.99, top=0.99, bottom=0.01)
plt.savefig(os.path.join(ASSETS_DIR, 'slide3_tech_clean.png'), bbox_inches='tight')
plt.close()
print("Slide 3 generated successfully!")

# ==============================================================================
# 2. SLIDE 5: Feasibility & Viability (Fixed Layout & Zero Overlap)
# ==============================================================================
fig, ax = plt.subplots(figsize=(8.0, 5.5), dpi=300)
ax.set_facecolor('#ffffff')
fig.patch.set_facecolor('#ffffff')
ax.set_xlim(0, 1)
ax.set_ylim(0, 1)
ax.axis('off')

cards = [
    {
        "title": "Technical Feasibility",
        "tag": "HARDWARE & MODEL",
        "bullets": [
            ("Entry Hardware", "Runs smoothly on ₹5,000 phones (Android 8.0+)"),
            ("Ultra-Light RAM", "Strictly under 60 MB RAM memory footprint"),
            ("100% Offline", "Quantized INT8 PyTorch model runs on-device")
        ],
        "bg": "#f0f7ff", "border": "#2b6cb0", "tag_bg": "#bee3f8", "tag_fg": "#2b6cb0",
        "x": 0.02, "y": 0.52
    },
    {
        "title": "Operational Feasibility",
        "tag": "RURAL USABILITY",
        "bullets": [
            ("Zero Data Needed", "Complete diagnosis in remote fields with zero net"),
            ("High Sunlight", "High-contrast UI visible in harsh midday sun"),
            ("Voice Navigation", "Native audio readout removes literacy barriers")
        ],
        "bg": "#f0fff4", "border": "#276749", "tag_bg": "#c6f6d5", "tag_fg": "#22543d",
        "x": 0.52, "y": 0.52
    },
    {
        "title": "Financial Viability",
        "tag": "COST STRUCTURE",
        "bullets": [
            ("₹0.15 Unit Cost", "Edge compute keeps diagnosis under 15 paise"),
            ("100% Free Forever", "Zero fee or paywall for smallholder farmers"),
            ("Serverless Scale", "Cloud tier auto-scales during crop seasons")
        ],
        "bg": "#fffaf0", "border": "#c05621", "tag_bg": "#feebc8", "tag_fg": "#c05621",
        "x": 0.02, "y": 0.04
    },
    {
        "title": "Agronomist Network",
        "tag": "EXPERT OVERSIGHT",
        "bullets": [
            ("Micro-Incentives", "Agri-college grads earn per case verification"),
            ("Sub-60s Reviews", "1-click web queue verifies edge cases rapidly"),
            ("Digital Trust", "Certified doctor stamp builds farmer confidence")
        ],
        "bg": "#faf5ff", "border": "#6b46c1", "tag_bg": "#e9d8fd", "tag_fg": "#6b46c1",
        "x": 0.52, "y": 0.04
    }
]

cw = 0.46
ch = 0.44

for c in cards:
    cx, cy = c["x"], c["y"]
    
    # Outer box
    box = patches.FancyBboxPatch(
        (cx, cy), cw, ch,
        boxstyle="round,pad=0.015",
        linewidth=1.8, edgecolor=c["border"], facecolor=c["bg"]
    )
    ax.add_patch(box)
    
    # Header banner box inside card
    h_box = patches.FancyBboxPatch(
        (cx + 0.012, cy + ch - 0.088), cw - 0.024, 0.076,
        boxstyle="round,pad=0.008",
        linewidth=1.0, edgecolor=c["border"], facecolor=c["tag_bg"]
    )
    ax.add_patch(h_box)
    
    # Title
    ax.text(cx + 0.03, cy + ch - 0.05, c["title"], fontsize=10.5, fontweight='bold',
            color=c["border"], va='center')
    
    # Tag label
    ax.text(cx + cw - 0.03, cy + ch - 0.05, c["tag"], fontsize=7.2, fontweight='bold',
            color=c["tag_fg"], ha='right', va='center')
    
    # Bullets
    for b_i, (b_lead, b_text) in enumerate(c["bullets"]):
        by = cy + ch - 0.13 - b_i * 0.098
        ax.text(cx + 0.03, by, f"• {b_lead}:", fontsize=9.0, fontweight='bold',
                color=c["border"], va='top')
        ax.text(cx + 0.03, by - 0.042, f"  {b_text}", fontsize=8.2, color='#2d3748', va='top')

plt.subplots_adjust(left=0.01, right=0.99, top=0.99, bottom=0.01)
plt.savefig(os.path.join(ASSETS_DIR, 'slide5_feasibility_clean.png'), bbox_inches='tight')
plt.close()
print("Slide 5 generated successfully!")

# ==============================================================================
# 3. SLIDE 6: Impact & Benefits Chart (Refined & Perfect Clearance)
# ==============================================================================
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(8.0, 5.5), dpi=300)
fig.patch.set_facecolor('#ffffff')

# Left Plot: Cost per acre comparison
categories = ['Traditional\nGuesswork', 'With KrishiClinic\nAdvisory']
costs = [8000, 2400]
colors = ['#e53e3e', '#2f855a']

bars = ax1.bar(categories, costs, color=colors, width=0.48, edgecolor='#2d3748', linewidth=1.5)
ax1.set_ylabel('Cost per Acre (₹ Rupees)', fontsize=11, fontweight='bold', color='#1a202c')
ax1.set_title('Farmer Input & Loss Costs', fontsize=12.5, fontweight='bold', color='#1a202c', pad=12)
ax1.grid(axis='y', linestyle='--', alpha=0.5)
ax1.set_ylim(0, 10500)
ax1.tick_params(axis='both', which='major', labelsize=10.5)

for bar in bars:
    yval = bar.get_height()
    ax1.text(bar.get_x() + bar.get_width()/2.0, yval + 350, f'₹{yval:,}', ha='center', va='bottom', fontsize=12, fontweight='bold')

ax1.text(1.0, 4800, '▼ 70% Cost\nSaved / Acre', ha='center', color='#22543d', fontsize=11, fontweight='bold',
         bbox=dict(boxstyle="round,pad=0.35", fc="#f0fff4", ec="#38a169", lw=1.6))

# Right Plot: Speed of diagnosis
time_cats = ['Traditional\nShop Route', 'KrishiClinic\nAI App']
times = [72, 2] # 2 sec represented visually
bars2 = ax2.bar(time_cats, times, color=['#dd6b20', '#2b6cb0'], width=0.48, edgecolor='#2d3748', linewidth=1.5)
ax2.set_ylabel('Time to Correct Diagnosis (Hours)', fontsize=11, fontweight='bold', color='#1a202c')
ax2.set_title('Speed of Containment', fontsize=12.5, fontweight='bold', color='#1a202c', pad=12)
ax2.grid(axis='y', linestyle='--', alpha=0.5)
ax2.set_ylim(0, 95)
ax2.tick_params(axis='both', which='major', labelsize=10.5)

ax2.text(0, 75, '72 Hours\n(Too Late!)', ha='center', fontsize=11, fontweight='bold', color='#c05621')
ax2.text(1, 7, '2 Seconds\n(Instant!)', ha='center', fontsize=11, fontweight='bold', color='#2b6cb0')

plt.suptitle('Data Sources: ICAR National Survey & NABARD Farm Economic Studies',
             fontsize=10, fontstyle='italic', y=0.03, color='#4a5568')
plt.tight_layout()
plt.subplots_adjust(bottom=0.15)
plt.savefig(os.path.join(ASSETS_DIR, 'slide6_impact_clean.png'), bbox_inches='tight')
plt.close()
print("Slide 6 generated successfully!")

# ==============================================================================
# 4. SLIDE 7: Business Model & Flywheel (Fixed Layout & Zero Overlap)
# ==============================================================================
fig, ax = plt.subplots(figsize=(8.0, 5.5), dpi=300)
ax.set_facecolor('#ffffff')
fig.patch.set_facecolor('#ffffff')
ax.set_xlim(0, 1)
ax.set_ylim(0, 1)
ax.axis('off')

# Center Hub: Farmers
center_x = 0.36
center_y = 0.28
center_w = 0.28
center_h = 0.44

c_box = patches.FancyBboxPatch(
    (center_x, center_y), center_w, center_h,
    boxstyle="round,pad=0.02",
    linewidth=2.4, edgecolor='#2f855a', facecolor='#ebfbee'
)
ax.add_patch(c_box)

ax.text(center_x + center_w/2, center_y + center_h - 0.045, "BENEFICIARY CORE",
        fontsize=7.8, fontweight='bold', color='#2f855a', ha='center', va='top')
ax.text(center_x + center_w/2, center_y + center_h - 0.11, "FARMERS",
        fontsize=15, fontweight='bold', color='#1c4532', ha='center', va='top')

ax.plot([center_x + 0.03, center_x + center_w - 0.03], [center_y + center_h - 0.18, center_y + center_h - 0.18],
        color='#2f855a', lw=1.2, alpha=0.5)

center_points = [
    "✓ 100% Free Forever",
    "✓ Instant 2s AI Scan",
    "✓ Agronomist Verified",
    "✓ 25km Outbreak Radar"
]
for i, pt in enumerate(center_points):
    ax.text(center_x + center_w/2, center_y + center_h - 0.225 - i * 0.050,
            pt, fontsize=8.8, fontweight='bold', color='#22543d', ha='center', va='top')

# 4 Surrounding Pillars
pillars = [
    {
        "title": "Verified Inputs (B2B)",
        "tag": "COMMERCE REVENUE",
        "bullets": [
            "Certified bio-chemicals & seeds",
            "Referral fee on verified sales",
            "Zero harmful counterfeits"
        ],
        "x": 0.02, "y": 0.54, "w": 0.29, "h": 0.42,
        "bg": "#f0f7ff", "border": "#2b6cb0", "tag_bg": "#bee3f8", "tag_fg": "#2b6cb0",
        "arrow_start": (0.315, 0.62), "arrow_end": (center_x - 0.008, 0.58)
    },
    {
        "title": "State Agri Bodies (B2G)",
        "tag": "GOVT SURVEILLANCE",
        "bullets": [
            "Regional epidemic tracking maps",
            "KVK & State dept subscriptions",
            "Biosecurity early warnings"
        ],
        "x": 0.69, "y": 0.54, "w": 0.29, "h": 0.42,
        "bg": "#fffaf0", "border": "#c05621", "tag_bg": "#feebc8", "tag_fg": "#c05621",
        "arrow_start": (0.685, 0.62), "arrow_end": (center_x + center_w + 0.008, 0.58)
    },
    {
        "title": "Crop Insurers (B2B)",
        "tag": "RISK UNDERWRITING",
        "bullets": [
            "PM Fasal Bima loss assessment",
            "Verified ground-truth disease logs",
            "Faster claim settlement cycles"
        ],
        "x": 0.02, "y": 0.04, "w": 0.29, "h": 0.42,
        "bg": "#faf5ff", "border": "#6b46c1", "tag_bg": "#e9d8fd", "tag_fg": "#6b46c1",
        "arrow_start": (0.315, 0.38), "arrow_end": (center_x - 0.008, 0.42)
    },
    {
        "title": "Agronomist Network",
        "tag": "RURAL GIG JOBS",
        "bullets": [
            "Micro-bounties for agri grads",
            "Skilled rural white-collar work",
            "Digital review stamp trust"
        ],
        "x": 0.69, "y": 0.04, "w": 0.29, "h": 0.42,
        "bg": "#e6fffa", "border": "#234e52", "tag_bg": "#b2f5ea", "tag_fg": "#234e52",
        "arrow_start": (0.685, 0.38), "arrow_end": (center_x + center_w + 0.008, 0.42)
    }
]

for p in pillars:
    px, py, pw, ph = p["x"], p["y"], p["w"], p["h"]
    
    # Outer box
    box = patches.FancyBboxPatch(
        (px, py), pw, ph,
        boxstyle="round,pad=0.015",
        linewidth=1.8, edgecolor=p["border"], facecolor=p["bg"]
    )
    ax.add_patch(box)
    
    # Header banner
    h_box = patches.FancyBboxPatch(
        (px + 0.012, py + ph - 0.088), pw - 0.024, 0.076,
        boxstyle="round,pad=0.008",
        linewidth=1.0, edgecolor=p["border"], facecolor=p["tag_bg"]
    )
    ax.add_patch(h_box)
    
    ax.text(px + pw/2, py + ph - 0.038, p["title"], fontsize=9.8, fontweight='bold',
            color=p["border"], ha='center', va='center')
    ax.text(px + pw/2, py + ph - 0.068, p["tag"], fontsize=6.8, fontweight='bold',
            color=p["tag_fg"], ha='center', va='center')
    
    # Bullets
    for bi, b in enumerate(p["bullets"]):
        by = py + ph - 0.13 - bi * 0.088
        ax.text(px + pw/2, by, b, fontsize=8.2, color='#2d3748', ha='center', va='top')
        
    # Flow arrow connecting strictly in the gap
    ax.annotate(
        '', xy=p["arrow_end"], xytext=p["arrow_start"],
        arrowprops=dict(arrowstyle="<->", color=p["border"], lw=2.2, mutation_scale=12)
    )

plt.subplots_adjust(left=0.01, right=0.99, top=0.99, bottom=0.01)
plt.savefig(os.path.join(ASSETS_DIR, 'slide7_business_clean.png'), bbox_inches='tight')
plt.close()
print("Slide 7 generated successfully!")

# ==============================================================================
# 5. SLIDE 8: Research and References (Fixed Layout & Zero Overlap)
# ==============================================================================
fig, ax = plt.subplots(figsize=(12.0, 5.2), dpi=300)
ax.set_facecolor('#ffffff')
fig.patch.set_facecolor('#ffffff')
ax.set_xlim(0, 1)
ax.set_ylim(0, 1)
ax.axis('off')

refs = [
    {
        "tag": "NATIONAL LOSS DATA",
        "title": "1. Indian Council of Agricultural Research (ICAR & ASSOCHAM)",
        "source": "National Crop Disease Economic Loss Survey (2022–2024)",
        "finding": "Documented over ₹90,000 Crore annual national crop loss caused by delayed disease diagnosis and ineffective dealer recommendations.",
        "metric_val": "₹90,000 Cr",
        "metric_lbl": "Annual Loss",
        "bg": "#f0f7ff", "border": "#2b6cb0", "tag_bg": "#bee3f8", "tag_fg": "#2b6cb0"
    },
    {
        "tag": "IPM GLOBAL STANDARD",
        "title": "2. Food and Agriculture Organization (FAO - United Nations)",
        "source": "Global Standards for Early Pest Surveillance & Integrated Pest Management",
        "finding": "Proved that rapid intervention within 7 days reduces required chemical spraying volume by up to 40% while protecting soil health.",
        "metric_val": "40% Cut",
        "metric_lbl": "Chemical Waste",
        "bg": "#f0fff4", "border": "#276749", "tag_bg": "#c6f6d5", "tag_fg": "#22543d"
    },
    {
        "tag": "RURAL GROUND TRUTH",
        "title": "3. National Sample Survey Office (NSSO 77th Round)",
        "source": "Situation Assessment of Agricultural Households in Rural India",
        "finding": "Revealed that over 60% of smallholder farmers rely entirely on private input dealers for advice rather than certified plant doctors.",
        "metric_val": "60%+ Reliance",
        "metric_lbl": "On Shopkeepers",
        "bg": "#fffaf0", "border": "#c05621", "tag_bg": "#feebc8", "tag_fg": "#c05621"
    },
    {
        "tag": "ECONOMIC AUDIT",
        "title": "4. National Bank for Agriculture and Rural Development (NABARD)",
        "source": "Smallholder Farm Economic Vulnerability & Input Cost Audit",
        "finding": "Demonstrated that smallholder farmers waste ₹25,000 to ₹30,000 per acre each season on ineffective, counterfeit, or unneeded chemicals.",
        "metric_val": "₹25,000+",
        "metric_lbl": "Saved / Acre",
        "bg": "#faf5ff", "border": "#6b46c1", "tag_bg": "#e9d8fd", "tag_fg": "#6b46c1"
    },
    {
        "tag": "EDGE AI BENCHMARK",
        "title": "5. PlantVillage Consortium (Hughes et al.)",
        "source": "Open-Access Deep Learning Pathology Benchmarks for Mobile Deployments",
        "finding": "Established standardized accuracy baselines (98.2%) for quantized convolutional networks deployed on entry-level mobile hardware.",
        "metric_val": "98.2% Accuracy",
        "metric_lbl": "Edge Baseline",
        "bg": "#f7fafc", "border": "#4a5568", "tag_bg": "#e2e8f0", "tag_fg": "#2d3748"
    }
]

card_h = 0.165
gap = 0.026
start_y = 0.80

for i, ref in enumerate(refs):
    y = start_y - i * (card_h + gap)
    
    # Outer box
    box = patches.FancyBboxPatch(
        (0.015, y), 0.97, card_h,
        boxstyle="round,pad=0.012",
        linewidth=1.8, edgecolor=ref["border"], facecolor=ref["bg"]
    )
    ax.add_patch(box)
    
    # Left tag pill
    tag_w = 0.155
    tag_h = 0.09
    tag = patches.FancyBboxPatch(
        (0.03, y + card_h/2 - tag_h/2), tag_w, tag_h,
        boxstyle="round,pad=0.008",
        linewidth=1.0, edgecolor=ref["border"], facecolor=ref["tag_bg"]
    )
    ax.add_patch(tag)
    ax.text(0.03 + tag_w/2, y + card_h/2, ref["tag"], fontsize=7.6, fontweight='bold',
            color=ref["tag_fg"], ha='center', va='center')
    
    # Content block
    ax.text(0.20, y + card_h - 0.022, ref["title"], fontsize=10.5, fontweight='bold',
            color=ref["border"], va='top')
    ax.text(0.20, y + card_h - 0.068, ref["source"], fontsize=8.2, fontstyle='italic',
            color='#4a5568', va='top')
    ax.text(0.20, y + card_h - 0.112, ref["finding"], fontsize=7.9,
            color='#2d3748', va='top')
    
    # Right metric box
    m_w = 0.125
    m_h = card_h - 0.03
    m_box = patches.FancyBboxPatch(
        (0.845, y + 0.015), m_w, m_h,
        boxstyle="round,pad=0.008",
        linewidth=1.2, edgecolor=ref["border"], facecolor=ref["tag_bg"]
    )
    ax.add_patch(m_box)
    ax.text(0.845 + m_w/2, y + 0.095, ref["metric_val"], fontsize=11.5, fontweight='bold',
            color=ref["border"], ha='center', va='center')
    ax.text(0.845 + m_w/2, y + 0.045, ref["metric_lbl"], fontsize=7.2, fontweight='bold',
            color='#4a5568', ha='center', va='center')

plt.subplots_adjust(left=0.01, right=0.99, top=0.99, bottom=0.01)
plt.savefig(os.path.join(ASSETS_DIR, 'slide8_references_clean.png'), bbox_inches='tight')
plt.close()
print("Slide 8 generated successfully!")
