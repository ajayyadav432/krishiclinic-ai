import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
import os

os.makedirs('/home/ajay/MUJ_Hackathon/presentation/assets', exist_ok=True)
plt.rcParams['font.sans-serif'] = 'DejaVu Sans'

# --- 1. SLIDE 2: Problem Comparison (Ramesh Ji's Story vs KrishiClinic) ---
fig, ax = plt.subplots(figsize=(10, 5), dpi=200)
ax.set_facecolor('#ffffff')
fig.patch.set_facecolor('#ffffff')
ax.axis('off')

# Left Box: Traditional Trap (Red tint)
rect_left = patches.FancyBboxPatch((0.02, 0.08), 0.46, 0.84, boxstyle="round,pad=0.03",
                                  linewidth=2, edgecolor='#e53e3e', facecolor='#fff5f5')
ax.add_patch(rect_left)

ax.text(0.25, 0.85, "TRADITIONAL TRAP (Ramesh Ji's Loss)", fontsize=13, fontweight='bold',
        color='#9b2c2c', ha='center')
ax.text(0.25, 0.77, "The Costly Guesswork Cycle", fontsize=10, fontstyle='italic',
        color='#742a2a', ha='center')

left_points = [
    "• Unknown leaf spots spotted at 4 AM in tomato field",
    "• Panicked visit to local fertilizer & chemical shopkeeper",
    "• Seller pushes unverified ₹2,500 pesticide (Sales target)",
    "• Wrong chemical burns leaf tissue (Bacterial vs Fungal)",
    "• ₹80,000 crop loss in 72 hours + lender debt"
]
for i, pt in enumerate(left_points):
    ax.text(0.05, 0.65 - i*0.09, pt, fontsize=9.5, color='#4a1515', weight='500')

ax.text(0.25, 0.14, "National Cost: ₹90,000 Cr Annual Loss\n(Source: ICAR & ASSOCHAM Agri-Loss Report)",
        fontsize=8.5, color='#c53030', ha='center', weight='bold')

# Right Box: KrishiClinic AI (Green tint)
rect_right = patches.FancyBboxPatch((0.52, 0.08), 0.46, 0.84, boxstyle="round,pad=0.03",
                                   linewidth=2, edgecolor='#2f855a', facecolor='#f0fff4')
ax.add_patch(rect_right)

ax.text(0.75, 0.85, "KRISHICLINIC AI (Verified Cure)", fontsize=13, fontweight='bold',
        color='#22543d', ha='center')
ax.text(0.75, 0.77, "Intelligent, Doctor-Verified Guidance", fontsize=10, fontstyle='italic',
        color='#276749', ha='center')

right_points = [
    "• Instant 1-tap photo from low-cost Android phone",
    "• 2-Second AI dual-vision diagnosis (Hindi & 8 languages)",
    "• Agronomist Verification Gate prevents wrong medicine",
    "• Exact chemical salt name + affordable organic remedy",
    "• 25km Outbreak Radar alerts surrounding farmers"
]
for i, pt in enumerate(right_points):
    ax.text(0.55, 0.65 - i*0.09, pt, fontsize=9.5, color='#1c4532', weight='500')

ax.text(0.75, 0.14, "Benefit: ₹25,000-₹30,000 Saved / Acre\n(Source: Farm Economic Studies, NABARD)",
        fontsize=8.5, color='#276749', ha='center', weight='bold')

plt.tight_layout()
plt.savefig('/home/ajay/MUJ_Hackathon/presentation/assets/slide2_problem_comparison.png', bbox_inches='tight')
plt.close()

# --- 2. SLIDE 3: Technical Architecture Infographic ---
fig, ax = plt.subplots(figsize=(11, 4.8), dpi=200)
ax.set_facecolor('#ffffff')
fig.patch.set_facecolor('#ffffff')
ax.axis('off')

# 4 Core Pillars Pipeline
steps = [
    ("1. Input & Edge UI", "• Low-end Android App\n• Voice in 8+ Languages\n• Offline Image Cache\n• Zero-data Fallback", "#ebf8ff", "#3182ce"),
    ("2. Vision AI Engine", "• EfficientNetV2-S Edge\n• Gemini Multimodal API\n• 2s Multi-Crop Detection\n• Severity Scoring", "#faf5ff", "#805ad5"),
    ("3. Human Validation", "• Agronomist Portal Gate\n• Confidence Threshold (70%)\n• Low-Confidence Routing\n• Digital Advisory Stamp", "#fffaf0", "#dd6b20"),
    ("4. Outbreak Radar", "• Geospatial Clustering\n• 25km Threat Radius\n• Automated Farm Alerts\n• Epidemic Prevention", "#f0fff4", "#38a169")
]

for idx, (title, text, bg, border) in enumerate(steps):
    x = 0.02 + idx * 0.245
    w = 0.22
    box = patches.FancyBboxPatch((x, 0.12), w, 0.76, boxstyle="round,pad=0.02",
                                linewidth=2, edgecolor=border, facecolor=bg)
    ax.add_patch(box)
    ax.text(x + w/2, 0.80, title, fontsize=11, fontweight='bold', color=border, ha='center')
    ax.text(x + 0.02, 0.52, text, fontsize=9.5, color='#2d3748', va='center', linespacing=1.6)
    
    # Arrow between boxes
    if idx < 3:
        ax.annotate('', xy=(x + w + 0.025, 0.5), xytext=(x + w, 0.5),
                    arrowprops=dict(arrowstyle="->", color="#718096", lw=2.5))

ax.text(0.5, 0.04, "High Reliability: Zero-network edge execution + Cloud AI fallback + Human Expert Safety Net",
        fontsize=9, color='#4a5568', ha='center', weight='bold')

plt.tight_layout()
plt.savefig('/home/ajay/MUJ_Hackathon/presentation/assets/slide3_tech_architecture.png', bbox_inches='tight')
plt.close()

# --- 3. SLIDE 4: User Experience Infographic ---
fig, ax = plt.subplots(figsize=(10.5, 4.8), dpi=200)
ax.set_facecolor('#ffffff')
fig.patch.set_facecolor('#ffffff')
ax.axis('off')

ux_cards = [
    ("Step 1: Snap or Speak", "Farmer taps one big button\nor speaks: 'Tamatar me daag hai'\nAudio in Hindi, Marathi, Telugu,\nPunjabi, Tamil & English.", "#f7fafc", "#4a5568", "#e2e8f0"),
    ("Step 2: Instant 2s Diagnosis", "Clear visual disease name\nwith Simple Color Traffic Light:\n• Green: Early / Minor\n• Orange: Moderate Damage\n• Red: High Severity Risk", "#f0fff4", "#22543d", "#9ae6b4"),
    ("Step 3: Actionable Cure", "Zero chemical confusion:\n• Exact active chemical & ratio\n• Eco-friendly organic alternative\n• Speech button reads cure aloud\n• Agronomist verified badge", "#ebf8ff", "#2b6cb0", "#bee3f8")
]

for idx, (title, desc, bg, text_c, border_c) in enumerate(ux_cards):
    x = 0.03 + idx * 0.32
    w = 0.29
    box = patches.FancyBboxPatch((x, 0.15), w, 0.70, boxstyle="round,pad=0.02",
                                linewidth=2, edgecolor=border_c, facecolor=bg)
    ax.add_patch(box)
    ax.text(x + w/2, 0.75, title, fontsize=12, fontweight='bold', color=text_c, ha='center')
    ax.text(x + w/2, 0.45, desc, fontsize=10, color='#2d3748', ha='center', va='center', linespacing=1.6)

ax.text(0.5, 0.05, "Accessible to every Indian farmer regardless of formal education or digital literacy",
        fontsize=9.5, color='#4a5568', ha='center', weight='bold')

plt.tight_layout()
plt.savefig('/home/ajay/MUJ_Hackathon/presentation/assets/slide4_ux_flow.png', bbox_inches='tight')
plt.close()

# --- 4. SLIDE 6: Impact & Benefits Chart ---
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10.5, 4.6), dpi=200)
fig.patch.set_facecolor('#ffffff')

# Left Plot: Cost per acre comparison
categories = ['Traditional\nGuesswork', 'With KrishiClinic\nAI Advisory']
costs = [8000, 2400] # chemical + damage expenses per acre
colors = ['#e53e3e', '#38a169']

bars = ax1.bar(categories, costs, color=colors, width=0.5, edgecolor='#2d3748', linewidth=1.2)
ax1.set_ylabel('Agri-Input & Damage Cost (₹ / Acre)', fontsize=10, fontweight='bold')
ax1.set_title('Farmer Input Costs & Losses Saved', fontsize=11, fontweight='bold', color='#1a202c')
ax1.grid(axis='y', linestyle='--', alpha=0.5)
ax1.set_ylim(0, 10000)

for bar in bars:
    yval = bar.get_height()
    ax1.text(bar.get_x() + bar.get_width()/2.0, yval + 300, f'₹{yval:,}', ha='center', va='bottom', fontsize=10, fontweight='bold')

ax1.text(1, 4000, '▼ 70% Cost\nSaved per Acre', ha='center', color='#22543d', fontsize=10, fontweight='bold',
         bbox=dict(boxstyle="round,pad=0.3", fc="#f0fff4", ec="#38a169", lw=1))

# Right Plot: Time to Diagnosis
times = [72, 0.033] # hours
time_cats = ['Traditional\nShop Route', 'KrishiClinic\nAI App']
bars2 = ax2.bar(time_cats, [72, 2], color=['#dd6b20', '#3182ce'], width=0.5, edgecolor='#2d3748', linewidth=1.2)
ax2.set_ylabel('Time to Correct Diagnosis (Hours)', fontsize=10, fontweight='bold')
ax2.set_title('Speed of Containment', fontsize=11, fontweight='bold', color='#1a202c')
ax2.grid(axis='y', linestyle='--', alpha=0.5)
ax2.set_ylim(0, 90)

ax2.text(0, 75, '72 hrs\n(Too late!)', ha='center', fontsize=9.5, fontweight='bold', color='#c05621')
ax2.text(1, 6, '2 Seconds\n(Instant!)', ha='center', fontsize=9.5, fontweight='bold', color='#2b6cb0')

plt.suptitle('Data-Backed Impact on Smallholder Livelihoods (Sources: ICAR & NABARD)', fontsize=12, fontweight='bold', y=0.98)
plt.tight_layout()
plt.savefig('/home/ajay/MUJ_Hackathon/presentation/assets/slide6_impact_chart.png', bbox_inches='tight')
plt.close()

# --- 5. SLIDE 7: Business Model Infographic ---
fig, ax = plt.subplots(figsize=(10.5, 4.8), dpi=200)
ax.set_facecolor('#ffffff')
fig.patch.set_facecolor('#ffffff')
ax.axis('off')

# Farmer Core (Center)
farmer_box = patches.FancyBboxPatch((0.36, 0.35), 0.28, 0.30, boxstyle="round,pad=0.03",
                                   linewidth=2.5, edgecolor='#38a169', facecolor='#f0fff4')
ax.add_patch(farmer_box)
ax.text(0.5, 0.54, "FARMERS", fontsize=14, fontweight='bold', color='#22543d', ha='center')
ax.text(0.5, 0.44, "100% Free Forever\nAI Diagnosis & Outbreak Alerts", fontsize=10, color='#276749', ha='center')

# Revenue Pillars
pillars = [
    ("B2B Verified Agri-Inputs", "Certified seed & bio-pesticide\nbrands pay referral fee for\ngenuine verified recommendations.", 0.05, 0.55, "#3182ce", "#ebf8ff"),
    ("B2B Crop Insurers", "PM Fasal Bima underwriters\nlicense ground outbreak\ndata for instant claim verification.", 0.05, 0.12, "#805ad5", "#faf5ff"),
    ("B2G Agricultural Bodies", "State agri-departments & KVKs\nsubscribe to regional disease radar\nfor epidemic containment.", 0.67, 0.55, "#dd6b20", "#fffaf0"),
    ("Micro-Incentive Agronomists", "Agri-science grads earn micro-bounties\nper verified referral, creating rural\nwhite-collar gig employment.", 0.67, 0.12, "#319795", "#e6fffa")
]

for title, desc, px, py, color, bg in pillars:
    box = patches.FancyBboxPatch((px, py), 0.28, 0.32, boxstyle="round,pad=0.02",
                                linewidth=1.8, edgecolor=color, facecolor=bg)
    ax.add_patch(box)
    ax.text(px + 0.14, py + 0.24, title, fontsize=10.5, fontweight='bold', color=color, ha='center')
    ax.text(px + 0.14, py + 0.11, desc, fontsize=8.8, color='#2d3748', ha='center', va='center')

ax.text(0.5, 0.03, "Sustainable Ecosystem: Free farmer utility subsidized by institutional value",
        fontsize=9.5, color='#4a5568', ha='center', weight='bold')

plt.tight_layout()
plt.savefig('/home/ajay/MUJ_Hackathon/presentation/assets/slide7_business_flywheel.png', bbox_inches='tight')
plt.close()

print("All presentation asset graphics generated successfully!")
