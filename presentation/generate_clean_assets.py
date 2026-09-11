import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import textwrap
import os

ASSETS_DIR = '/home/ajay/MUJ_Hackathon/presentation/assets'
os.makedirs(ASSETS_DIR, exist_ok=True)
plt.rcParams['font.sans-serif'] = 'DejaVu Sans'
plt.rcParams['font.family'] = 'sans-serif'

# ==============================================================================
# 1. SLIDE 2: Problem Comparison (Flawless Spacing & Large Fonts)
# ==============================================================================
fig, ax = plt.subplots(figsize=(7.5, 5.4), dpi=300)
ax.set_facecolor('#ffffff')
fig.patch.set_facecolor('#ffffff')
ax.set_xlim(0, 1)
ax.set_ylim(0, 1)
ax.axis('off')

# Left Card: Traditional Trap (Red)
b_left = patches.FancyBboxPatch((0.02, 0.03), 0.46, 0.94, boxstyle="round,pad=0.02",
                               linewidth=2.2, edgecolor='#e53e3e', facecolor='#fff5f5')
ax.add_patch(b_left)

ax.text(0.25, 0.90, "TRADITIONAL TRAP", fontsize=15, fontweight='bold', color='#9b2c2c', ha='center')
ax.text(0.25, 0.84, "Unverified Guesswork & Delays", fontsize=11, fontstyle='italic', color='#c53030', ha='center')

left_items = [
    ("Unqualified Advice", "60%+ of farmers rely entirely on chemical shopkeeper quotas."),
    ("Wrong Chemical Sprays", "Fungal vs bacterial errors burn leaves and kill soil biology."),
    ("Catastrophic Debt", "₹80,000 lost in 72 hours per family farm with zero recovery.")
]

for idx, (title, desc) in enumerate(left_items):
    y = 0.74 - idx * 0.20
    ax.text(0.05, y, f"• {title}", fontsize=12.5, fontweight='bold', color='#742a2a')
    w_desc = textwrap.fill(desc, width=30)
    ax.text(0.07, y - 0.038, w_desc, fontsize=10.5, color='#4a1515', linespacing=1.25, va='top')

# Metric Pill Left
pill_l = patches.FancyBboxPatch((0.04, 0.06), 0.42, 0.09, boxstyle="round,pad=0.01",
                               linewidth=1.2, edgecolor='#e53e3e', facecolor='#fed7d7')
ax.add_patch(pill_l)
ax.text(0.25, 0.105, "₹90,000 Cr National Loss / Yr", fontsize=11.5, fontweight='bold', color='#9b2c2c', ha='center')

# Right Card: KrishiClinic AI (Green)
b_right = patches.FancyBboxPatch((0.52, 0.03), 0.46, 0.94, boxstyle="round,pad=0.02",
                                linewidth=2.2, edgecolor='#2f855a', facecolor='#f0fff4')
ax.add_patch(b_right)

ax.text(0.75, 0.90, "KRISHICLINIC AI", fontsize=15, fontweight='bold', color='#22543d', ha='center')
ax.text(0.75, 0.84, "2-Sec AI + Certified Doctor Gate", fontsize=11, fontstyle='italic', color='#276749', ha='center')

right_items = [
    ("Instant Diagnosis", "2-second on-device scan in Hindi & 8 regional languages."),
    ("Doctor Safety Net", "Accredited agronomists verify low-confidence leaf cases."),
    ("Targeted Medicine", "Exact active salt dosage + verified low-cost organic recipes.")
]

for idx, (title, desc) in enumerate(right_items):
    y = 0.74 - idx * 0.20
    ax.text(0.55, y, f"• {title}", fontsize=12.5, fontweight='bold', color='#22543d')
    w_desc = textwrap.fill(desc, width=30)
    ax.text(0.57, y - 0.038, w_desc, fontsize=10.5, color='#1c4532', linespacing=1.25, va='top')

# Metric Pill Right
pill_r = patches.FancyBboxPatch((0.54, 0.06), 0.42, 0.09, boxstyle="round,pad=0.01",
                                linewidth=1.2, edgecolor='#2f855a', facecolor='#c6f6d5')
ax.add_patch(pill_r)
ax.text(0.75, 0.105, "₹25,000 - ₹30,000 Saved / Acre", fontsize=11.5, fontweight='bold', color='#22543d', ha='center')

plt.savefig(os.path.join(ASSETS_DIR, 'slide2_problem_clean.png'), bbox_inches='tight')
plt.close()


# ==============================================================================
# 2. SLIDE 3: Technical Architecture Infographic (Flawless)
# ==============================================================================
fig, ax = plt.subplots(figsize=(7.5, 5.4), dpi=300)
ax.set_facecolor('#ffffff')
fig.patch.set_facecolor('#ffffff')
ax.set_xlim(0, 1)
ax.set_ylim(0, 1)
ax.axis('off')

steps_s3 = [
    {
        "num": "01",
        "title": "Smart Rural Edge Input",
        "badge": "FARMER LAYER",
        "bullets": [
            "1-tap camera capture & native voice in 8+ Indian languages",
            "Runs on ₹5,000 Android phones with <60 MB RAM memory"
        ],
        "bg": "#f0f7ff", "border": "#2b6cb0", "badge_bg": "#bee3f8", "badge_fg": "#2b6cb0"
    },
    {
        "num": "02",
        "title": "Dual-Engine Vision Core",
        "badge": "AI ENGINE",
        "bullets": [
            "Quantized EfficientNetV2-S runs 100% offline on device",
            "Gemini Vision cloud fallback for multi-disease leaves"
        ],
        "bg": "#faf5ff", "border": "#6b46c1", "badge_bg": "#e9d8fd", "badge_fg": "#6b46c1"
    },
    {
        "num": "03",
        "title": "Agronomist Safety Gate",
        "badge": "SAFETY GATE",
        "bullets": [
            "Confidence ≥ 70% auto-approves; rare cases route to experts",
            "Digital certification seal ensures trusted clinical advice"
        ],
        "bg": "#fffaf0", "border": "#c05621", "badge_bg": "#feebc8", "badge_fg": "#c05621"
    },
    {
        "num": "04",
        "title": "Outbreak Radar (25 km)",
        "badge": "SURVEILLANCE",
        "bullets": [
            "DBSCAN geospatial clustering detects pathogen hotspots",
            "Automated broadcast alerts prevent village-wide epidemics"
        ],
        "bg": "#f0fff4", "border": "#276749", "badge_bg": "#c6f6d5", "badge_fg": "#22543d"
    }
]

card_h = 0.20
gap = 0.045
start_y = 0.765

for idx, step in enumerate(steps_s3):
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
        (0.04, y + 0.025), 0.09, 0.15,
        boxstyle="round,pad=0.01",
        linewidth=1.2, edgecolor=step["border"], facecolor=step["badge_bg"]
    )
    ax.add_patch(pill)
    ax.text(0.085, y + 0.10, step["num"], fontsize=15, fontweight='bold',
            color=step["border"], ha='center', va='center')
    
    # Title
    ax.text(0.155, y + card_h - 0.038, step["title"], fontsize=13.5, fontweight='bold',
            color=step["border"], va='top')
    
    # Category badge on right
    bw = 0.24
    bh = 0.052
    badge = patches.FancyBboxPatch(
        (0.72, y + card_h - 0.065), bw, bh,
        boxstyle="round,pad=0.006",
        linewidth=0.8, edgecolor=step["border"], facecolor=step["badge_bg"]
    )
    ax.add_patch(badge)
    ax.text(0.72 + bw/2, y + card_h - 0.039, step["badge"], fontsize=9.5, fontweight='bold',
            color=step["badge_fg"], ha='center', va='center')
    
    # Bullets (large fonts)
    for b_idx, bullet in enumerate(step["bullets"]):
        by = y + card_h - 0.095 - b_idx * 0.048
        ax.text(0.155, by, "• " + bullet, fontsize=10.5, color='#2d3748', va='top')
        
    # Flow arrow between boxes
    if idx < 3:
        ax.annotate('', xy=(0.085, y - gap + 0.008), xytext=(0.085, y - 0.006),
                    arrowprops=dict(arrowstyle="->", color=step["border"], lw=2.4, mutation_scale=12))

plt.savefig(os.path.join(ASSETS_DIR, 'slide3_tech_clean.png'), bbox_inches='tight')
plt.close()


# ==============================================================================
# 3. SLIDE 4: User Experience Infographic (Strict Wrapping, Zero Overflow)
# ==============================================================================
fig, ax = plt.subplots(figsize=(7.5, 5.4), dpi=300)
ax.set_facecolor('#ffffff')
fig.patch.set_facecolor('#ffffff')
ax.set_xlim(0, 1)
ax.set_ylim(0, 1)
ax.axis('off')

ux_steps = [
    {
        "step": "STEP 1",
        "title": "Snap or Speak",
        "sub": "Zero-Typing Input",
        "points": [
            "1-tap instant camera capture",
            "Native voice in 8+ Indian languages",
            "100% offline edge capture"
        ],
        "bg": "#f7fafc", "border": "#4a5568", "badge_bg": "#edf2f7"
    },
    {
        "step": "STEP 2",
        "title": "Instant Severity",
        "sub": "2-Second AI Scan",
        "points": [
            "Color badges: Green / Orange / Red",
            "Zero scientific jargon",
            "70%+ auto-approval safety gate"
        ],
        "bg": "#faf5ff", "border": "#6b46c1", "badge_bg": "#e9d8fd"
    },
    {
        "step": "STEP 3",
        "title": "Verified Cure",
        "sub": "Doctor Certified",
        "points": [
            "Exact salt names & dilution ratios",
            "Affordable organic cures",
            "Audio player reads cure aloud"
        ],
        "bg": "#f0fff4", "border": "#276749", "badge_bg": "#c6f6d5"
    }
]

for idx, s in enumerate(ux_steps):
    x = 0.02 + idx * 0.335
    w = 0.29
    box = patches.FancyBboxPatch((x, 0.05), w, 0.90, boxstyle="round,pad=0.02",
                                linewidth=2.0, edgecolor=s["border"], facecolor=s["bg"])
    ax.add_patch(box)
    
    # Step header pill
    pill = patches.FancyBboxPatch((x + 0.03, 0.85), w - 0.06, 0.07, boxstyle="round,pad=0.01",
                                 linewidth=1, edgecolor=s["border"], facecolor=s["badge_bg"])
    ax.add_patch(pill)
    ax.text(x + w/2, 0.885, s["step"], fontsize=12, fontweight='bold', color=s["border"], ha='center', va='center')
    
    # Title & Sub
    ax.text(x + w/2, 0.78, s["title"], fontsize=13.5, fontweight='bold', color='#1a202c', ha='center')
    ax.text(x + w/2, 0.72, s["sub"], fontsize=10.5, fontstyle='italic', color=s["border"], ha='center')
    
    # Bullets with strict wrapping
    for p_idx, pt in enumerate(s["points"]):
        py = 0.58 - p_idx * 0.16
        w_pt = textwrap.fill(pt, width=17)
        ax.text(x + 0.02, py, "• " + w_pt.replace("\n", "\n  "), fontsize=10, color='#2d3748', linespacing=1.2, va='top')
        
    # Flow arrow between columns
    if idx < 2:
        ax.annotate('', xy=(x + w + 0.035, 0.50), xytext=(x + w + 0.008, 0.50),
                    arrowprops=dict(arrowstyle="->", color="#718096", lw=2.2, mutation_scale=12))

plt.savefig(os.path.join(ASSETS_DIR, 'slide4_ux_clean.png'), bbox_inches='tight')
plt.close()


# ==============================================================================
# 4. SLIDE 5: Feasibility & Viability (4 Clean Pillars)
# ==============================================================================
fig, ax = plt.subplots(figsize=(7.5, 5.4), dpi=300)
ax.set_facecolor('#ffffff')
fig.patch.set_facecolor('#ffffff')
ax.set_xlim(0, 1)
ax.set_ylim(0, 1)
ax.axis('off')

feasibility_cards = [
    {
        "title": "Low-Cost Mobile",
        "metric": "₹5,000 Phones",
        "desc": "Runs smoothly on Android 8.0+ smartphones with <60 MB RAM footprint.",
        "bg": "#f0f7ff", "border": "#2b6cb0", "badge_bg": "#bee3f8"
    },
    {
        "title": "Offline Resilience",
        "metric": "Zero Internet",
        "desc": "Quantized models diagnose leaves directly in zero-network farm fields.",
        "bg": "#f0fff4", "border": "#276749", "badge_bg": "#c6f6d5"
    },
    {
        "title": "Minimal Unit Cost",
        "metric": "< ₹0.15 / Scan",
        "desc": "Edge compute offloads servers, ensuring 100% free access for farmers.",
        "bg": "#faf5ff", "border": "#6b46c1", "badge_bg": "#e9d8fd"
    },
    {
        "title": "Doctor Network",
        "metric": "Agri Colleges",
        "desc": "Micro-incentivized agriculture graduates verify edge cases on the portal.",
        "bg": "#fffaf0", "border": "#c05621", "badge_bg": "#feebc8"
    }
]

for idx, card in enumerate(feasibility_cards):
    col = idx % 2
    row = idx // 2
    x = 0.03 + col * 0.49
    y = 0.52 - row * 0.46
    w = 0.45
    h = 0.42
    
    box = patches.FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.02",
                                linewidth=1.8, edgecolor=card["border"], facecolor=card["bg"])
    ax.add_patch(box)
    
    # Metric pill
    pill = patches.FancyBboxPatch((x + 0.03, y + h - 0.11), w - 0.06, 0.08, boxstyle="round,pad=0.01",
                                 linewidth=1, edgecolor=card["border"], facecolor=card["badge_bg"])
    ax.add_patch(pill)
    ax.text(x + w/2, y + h - 0.07, card["metric"], fontsize=13, fontweight='bold', color=card["border"], ha='center', va='center')
    
    # Title & description
    ax.text(x + 0.03, y + h - 0.16, card["title"], fontsize=13, fontweight='bold', color='#1a202c')
    w_desc = textwrap.fill(card["desc"], width=26)
    ax.text(x + 0.03, y + h - 0.22, w_desc, fontsize=10.5, color='#4a5568', linespacing=1.3, va='top')

plt.savefig(os.path.join(ASSETS_DIR, 'slide5_feasibility_clean.png'), bbox_inches='tight')
plt.close()


# ==============================================================================
# 5. SLIDE 6: Impact & Benefits Chart (Clear Dual Plots)
# ==============================================================================
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(7.5, 5.4), dpi=300)
fig.patch.set_facecolor('#ffffff')

# Left Plot: Cost per acre
categories = ['Traditional\nGuesswork', 'KrishiClinic\nAdvisory']
costs = [8000, 2400]
colors = ['#e53e3e', '#38a169']

bars = ax1.bar(categories, costs, color=colors, width=0.48, edgecolor='#2d3748', linewidth=1.5)
ax1.set_ylabel('Agri-Input Cost (₹ / Acre)', fontsize=11, fontweight='bold', color='#1a202c')
ax1.set_title('Farmer Savings / Acre', fontsize=13, fontweight='bold', color='#22543d', pad=10)
ax1.set_ylim(0, 10000)
ax1.grid(axis='y', linestyle='--', alpha=0.4)
ax1.tick_params(axis='both', labelsize=10)

for bar in bars:
    yval = bar.get_height()
    ax1.text(bar.get_x() + bar.get_width()/2.0, yval + 300, f"₹{yval:,}", ha='center', va='bottom',
             fontsize=12, fontweight='bold', color='#1a202c')

ax1.text(0.5, 5200, "70% Direct\nSavings!", fontsize=13, fontweight='bold', color='#22543d', ha='center',
         bbox=dict(boxstyle="round,pad=0.3", fc="#c6f6d5", ec="#276749", lw=1.5))

# Right Plot: Key Impact Metrics
ax2.axis('off')
impact_metrics = [
    ("40% Less Chemicals", "Precision active salt ratios reduce excessive chemical spraying."),
    ("2s vs 72h Delay", "Instant on-field diagnosis stops crop destruction within hours."),
    ("25 km Threat Radar", "Village alerts halt fungal and bacterial spore epidemic spread.")
]

for idx, (title, desc) in enumerate(impact_metrics):
    y = 0.72 - idx * 0.32
    box = patches.FancyBboxPatch((0.02, y), 0.96, 0.27, boxstyle="round,pad=0.02",
                                linewidth=1.8, edgecolor='#276749', facecolor='#f0fff4')
    ax2.add_patch(box)
    ax2.text(0.06, y + 0.18, title, fontsize=13, fontweight='bold', color='#22543d')
    w_desc = textwrap.fill(desc, width=28)
    ax2.text(0.06, y + 0.11, w_desc, fontsize=10.5, color='#2d3748', linespacing=1.25, va='top')

plt.tight_layout()
plt.savefig(os.path.join(ASSETS_DIR, 'slide6_impact_clean.png'), bbox_inches='tight')
plt.close()


# ==============================================================================
# 6. SLIDE 7: Business Model & Sustainability (Flawless Spacing & No Overlap)
# ==============================================================================
fig, ax = plt.subplots(figsize=(7.5, 5.4), dpi=300)
ax.set_facecolor('#ffffff')
fig.patch.set_facecolor('#ffffff')
ax.set_xlim(0, 1)
ax.set_ylim(0, 1)
ax.axis('off')

# Center Core Box
center_box = patches.FancyBboxPatch((0.28, 0.38), 0.44, 0.24, boxstyle="round,pad=0.02",
                                   linewidth=2.5, edgecolor='#22543d', facecolor='#c6f6d5')
ax.add_patch(center_box)
ax.text(0.50, 0.53, "KRISHICLINIC", fontsize=15, fontweight='bold', color='#22543d', ha='center')
ax.text(0.50, 0.45, "100% Free for Farmers", fontsize=12, fontweight='bold', color='#276749', ha='center')

# 3 Stakeholder Revenue Blocks
blocks = [
    {
        "pos": (0.02, 0.70), "w": 0.46, "h": 0.27,
        "title": "B2B: Input Brands",
        "sub": "Verified Referral Margins",
        "desc": "Certified bio-pesticide partners pay margins for verified remedies.",
        "bg": "#ebf8ff", "border": "#3182ce"
    },
    {
        "pos": (0.52, 0.70), "w": 0.46, "h": 0.27,
        "title": "B2B: Crop Insurers",
        "sub": "Ground Damage Analytics",
        "desc": "PM Fasal Bima Yojana insurers license verified disease data.",
        "bg": "#faf5ff", "border": "#805ad5"
    },
    {
        "pos": (0.27, 0.04), "w": 0.46, "h": 0.27,
        "title": "B2G: State Agri Depts",
        "sub": "Epidemic Surveillance",
        "desc": "State departments & KVKs subscribe to real-time radar heatmaps.",
        "bg": "#fffaf0", "border": "#dd6b20"
    }
]

for b in blocks:
    bx, by = b["pos"]
    box = patches.FancyBboxPatch((bx, by), b["w"], b["h"], boxstyle="round,pad=0.02",
                                linewidth=1.8, edgecolor=b["border"], facecolor=b["bg"])
    ax.add_patch(box)
    ax.text(bx + b["w"]/2, by + b["h"] - 0.055, b["title"], fontsize=13.5, fontweight='bold', color=b["border"], ha='center')
    ax.text(bx + b["w"]/2, by + b["h"] - 0.105, b["sub"], fontsize=10.5, fontstyle='italic', color='#4a5568', ha='center')
    w_desc = textwrap.fill(b["desc"], width=27)
    ax.text(bx + b["w"]/2, by + b["h"] - 0.165, w_desc, fontsize=10.5, color='#2d3748', linespacing=1.2, ha='center', va='top')

# Connectors from center to blocks (cleanly separated)
ax.annotate('', xy=(0.25, 0.70), xytext=(0.35, 0.62),
            arrowprops=dict(arrowstyle="<->", color="#4a5568", lw=2.0))
ax.annotate('', xy=(0.75, 0.70), xytext=(0.65, 0.62),
            arrowprops=dict(arrowstyle="<->", color="#4a5568", lw=2.0))
ax.annotate('', xy=(0.50, 0.31), xytext=(0.50, 0.38),
            arrowprops=dict(arrowstyle="<->", color="#4a5568", lw=2.0))

plt.savefig(os.path.join(ASSETS_DIR, 'slide7_business_clean.png'), bbox_inches='tight')
plt.close()


# ==============================================================================
# 7. SLIDE 8: Research and References (Sleek 2-Line Layout, Zero Overlap)
# ==============================================================================
fig, ax = plt.subplots(figsize=(7.5, 5.4), dpi=300)
ax.set_facecolor('#ffffff')
fig.patch.set_facecolor('#ffffff')
ax.set_xlim(0, 1)
ax.set_ylim(0, 1)
ax.axis('off')

refs = [
    {
        "header": "ICAR (Govt. of India)  •  National Economic Survey",
        "fact": "Over ₹90,000 Cr lost annually in India to misdiagnosed crop pathogens.",
        "bg": "#f0f7ff", "border": "#2b6cb0"
    },
    {
        "header": "NSSO (Ministry of Statistics)  •  77th Round Household Survey",
        "fact": "60%+ of rural Indian farmers depend entirely on local shopkeeper advice.",
        "bg": "#f0fff4", "border": "#276749"
    },
    {
        "header": "PlantVillage Consortium  •  Deep Learning for Crop Pathology",
        "fact": "Mobile quantized vision models achieve 96%+ crop pathology accuracy.",
        "bg": "#faf5ff", "border": "#6b46c1"
    },
    {
        "header": "FAO (United Nations)  •  Integrated Pest Management Standards",
        "fact": "Targeted early IPM and surveillance cut chemical pesticide usage by up to 40%.",
        "bg": "#fffaf0", "border": "#c05621"
    }
]

start_y = 0.78
gap = 0.05
h = 0.17

for idx, ref in enumerate(refs):
    y = start_y - idx * (h + gap)
    box = patches.FancyBboxPatch((0.02, y), 0.96, h, boxstyle="round,pad=0.015",
                                linewidth=1.8, edgecolor=ref["border"], facecolor=ref["bg"])
    ax.add_patch(box)
    
    ax.text(0.04, y + h - 0.055, ref["header"], fontsize=12, fontweight='bold', color=ref["border"])
    ax.text(0.04, y + h - 0.115, "• Key Finding: " + ref["fact"], fontsize=9.8, color='#1a202c')

plt.savefig(os.path.join(ASSETS_DIR, 'slide8_references_clean.png'), bbox_inches='tight')
plt.close()

print("Slide 8 asset regenerated!")

