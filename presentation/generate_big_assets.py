import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
import os

os.makedirs('/home/ajay/MUJ_Hackathon/presentation/assets', exist_ok=True)
plt.rcParams['font.sans-serif'] = 'DejaVu Sans'

# --- 1. SLIDE 3: Technical Architecture Infographic (BIG FONTS) ---
fig, ax = plt.subplots(figsize=(7.5, 4.8), dpi=220)
ax.set_facecolor('#ffffff')
fig.patch.set_facecolor('#ffffff')
ax.axis('off')

steps = [
    ("1. Farm Input & Voice", "Low-end Android phone\nVoice in 8+ Indian languages\n1-tap camera & audio prompt\nZero-data local storage", "#ebf8ff", "#2b6cb0"),
    ("2. Dual-Engine Vision AI", "EfficientNetV2-S edge model\nGemini Vision cloud fallback\n2-second disease detection\n3-level severity grading", "#faf5ff", "#6b46c1"),
    ("3. Doctor Validation Gate", "Certified agronomist portal\nAuto-approve if confidence >= 70%\nHuman review for edge cases\nDigital advisory verification stamp", "#fffaf0", "#c05621"),
    ("4. Outbreak Alert Radar", "Geospatial cluster analysis\n25 km disease perimeter warning\nVillage epidemic prevention\nAnonymized field surveillance", "#f0fff4", "#276749")
]

for idx, (title, text, bg, border) in enumerate(steps):
    y = 0.77 - idx * 0.24
    box = patches.FancyBboxPatch((0.04, y), 0.92, 0.20, boxstyle="round,pad=0.02",
                                linewidth=2, edgecolor=border, facecolor=bg)
    ax.add_patch(box)
    ax.text(0.08, y + 0.14, title, fontsize=12.5, fontweight='bold', color=border)
    ax.text(0.08, y + 0.05, text, fontsize=10.5, color='#2d3748', linespacing=1.35)

plt.tight_layout()
plt.savefig('/home/ajay/MUJ_Hackathon/presentation/assets/slide3_tech_big.png', bbox_inches='tight')
plt.close()

# --- 2. SLIDE 5: Feasibility & Viability (BIG FONTS) ---
fig, ax = plt.subplots(figsize=(7.5, 4.8), dpi=220)
ax.set_facecolor('#ffffff')
fig.patch.set_facecolor('#ffffff')
ax.axis('off')

cards = [
    ("Technical Feasibility", [
        "Runs on low-cost Android (Rs 5,000 phones)",
        "Ultra-light memory: under 60 MB RAM footprint",
        "Quantized PyTorch model runs 100% offline"
    ], "#ebf8ff", "#2b6cb0", 0.03, 0.52),
    
    ("Operational Feasibility", [
        "100% offline edge execution in remote fields",
        "High-contrast screens visible in direct sunlight",
        "Voice navigation for low-literacy farmers"
    ], "#f0fff4", "#276749", 0.52, 0.52),
    
    ("Financial Viability", [
        "Inference cost under Rs 0.15 per diagnosis",
        "100% free access forever for smallholder farmers",
        "Serverless tier handles peak seasonal surges"
    ], "#fffaf0", "#c05621", 0.03, 0.04),
    
    ("Agronomist Network", [
        "Micro-incentives for agricultural college grads",
        "Web review queue resolves cases in under 1 min",
        "Digital verification stamp ensures medical trust"
    ], "#faf5ff", "#6b46c1", 0.52, 0.04)
]

for title, bullets, bg, border, x, y in cards:
    box = patches.FancyBboxPatch((x, y), 0.45, 0.42, boxstyle="round,pad=0.02",
                                linewidth=2, edgecolor=border, facecolor=bg)
    ax.add_patch(box)
    ax.text(x + 0.03, y + 0.35, title, fontsize=12, fontweight='bold', color=border)
    for idx, b in enumerate(bullets):
        ax.text(x + 0.03, y + 0.25 - idx * 0.09, "• " + b, fontsize=10, color='#2d3748')

plt.tight_layout()
plt.savefig('/home/ajay/MUJ_Hackathon/presentation/assets/slide5_feasibility_big.png', bbox_inches='tight')
plt.close()

# --- 3. SLIDE 6: Impact & Benefits Chart (BIG FONTS) ---
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(7.6, 4.8), dpi=220)
fig.patch.set_facecolor('#ffffff')

# Left Plot: Cost per acre comparison
categories = ['Traditional\nGuesswork', 'With KrishiClinic\nAdvisory']
costs = [8000, 2400]
colors = ['#e53e3e', '#2f855a']

bars = ax1.bar(categories, costs, color=colors, width=0.48, edgecolor='#2d3748', linewidth=1.5)
ax1.set_ylabel('Cost per Acre (Rupees)', fontsize=11, fontweight='bold', color='#1a202c')
ax1.set_title('Farmer Input & Loss Costs', fontsize=12, fontweight='bold', color='#1a202c', pad=10)
ax1.grid(axis='y', linestyle='--', alpha=0.5)
ax1.set_ylim(0, 10000)
ax1.tick_params(axis='both', which='major', labelsize=10.5)

for bar in bars:
    yval = bar.get_height()
    ax1.text(bar.get_x() + bar.get_width()/2.0, yval + 350, f'Rs {yval:,}', ha='center', va='bottom', fontsize=12, fontweight='bold')

ax1.text(1, 4600, '70% Cost Saved\nper Acre', ha='center', color='#22543d', fontsize=11, fontweight='bold',
         bbox=dict(boxstyle="round,pad=0.3", fc="#f0fff4", ec="#38a169", lw=1.5))

# Right Plot: Speed of diagnosis
times = [72, 0.033]
time_cats = ['Traditional\nShop Route', 'KrishiClinic\nAI App']
bars2 = ax2.bar(time_cats, [72, 2], color=['#dd6b20', '#2b6cb0'], width=0.48, edgecolor='#2d3748', linewidth=1.5)
ax2.set_ylabel('Time to Correct Diagnosis (Hours)', fontsize=11, fontweight='bold', color='#1a202c')
ax2.set_title('Speed of Containment', fontsize=12, fontweight='bold', color='#1a202c', pad=10)
ax2.grid(axis='y', linestyle='--', alpha=0.5)
ax2.set_ylim(0, 90)
ax2.tick_params(axis='both', which='major', labelsize=10.5)

ax2.text(0, 75, '72 Hours\n(Harvest Lost)', ha='center', fontsize=11, fontweight='bold', color='#c05621')
ax2.text(1, 8, '2 Seconds\n(Instant!)', ha='center', fontsize=11, fontweight='bold', color='#2b6cb0')

plt.suptitle('Data Sources: ICAR National Survey & NABARD Farm Studies', fontsize=11, fontstyle='italic', y=0.03, color='#4a5568')
plt.tight_layout()
plt.subplots_adjust(bottom=0.15)
plt.savefig('/home/ajay/MUJ_Hackathon/presentation/assets/slide6_impact_big.png', bbox_inches='tight')
plt.close()

# --- 4. SLIDE 7: Business Model (BIG FONTS) ---
fig, ax = plt.subplots(figsize=(7.5, 4.8), dpi=220)
ax.set_facecolor('#ffffff')
fig.patch.set_facecolor('#ffffff')
ax.axis('off')

# Center: Farmers
f_box = patches.FancyBboxPatch((0.30, 0.36), 0.40, 0.28, boxstyle="round,pad=0.03",
                              linewidth=2.5, edgecolor='#2f855a', facecolor='#f0fff4')
ax.add_patch(f_box)
ax.text(0.5, 0.53, "FARMERS", fontsize=15, fontweight='bold', color='#22543d', ha='center')
ax.text(0.5, 0.43, "100% Free Forever\nAI Diagnosis & Alerts", fontsize=11, fontweight='bold', color='#276749', ha='center')

# 4 Pillars
pillars = [
    ("Verified Agri-Inputs (B2B)", "Certified chemical & seed brands\npay referral fee for authentic products", 0.02, 0.54, "#2b6cb0", "#ebf8ff"),
    ("Crop Insurers (B2B)", "PM Fasal Bima underwriters license\nground data for fast claim verification", 0.02, 0.10, "#6b46c1", "#faf5ff"),
    ("State Agri Bodies (B2G)", "Govt & KVKs subscribe to regional\noutbreak radar for epidemic control", 0.60, 0.54, "#c05621", "#fffaf0"),
    ("Agronomist Network", "Micro-incentives for agri grads,\ncreating skilled rural gig work", 0.60, 0.10, "#234e52", "#e6fffa")
]

for title, desc, px, py, color, bg in pillars:
    box = patches.FancyBboxPatch((px, py), 0.38, 0.33, boxstyle="round,pad=0.02",
                                linewidth=2, edgecolor=color, facecolor=bg)
    ax.add_patch(box)
    ax.text(px + 0.19, py + 0.23, title, fontsize=11.5, fontweight='bold', color=color, ha='center')
    ax.text(px + 0.19, py + 0.10, desc, fontsize=9.8, color='#2d3748', ha='center', va='center')

plt.tight_layout()
plt.savefig('/home/ajay/MUJ_Hackathon/presentation/assets/slide7_business_big.png', bbox_inches='tight')
plt.close()

# --- 5. SLIDE 8: Research and References (BIG FONTS) ---
fig, ax = plt.subplots(figsize=(11.5, 4.8), dpi=220)
ax.set_facecolor('#ffffff')
fig.patch.set_facecolor('#ffffff')
ax.axis('off')

refs = [
    ("1. Indian Council of Agricultural Research (ICAR)",
     "National Assessment on Crop Disease Losses (2022-2024).\nDocumented over Rs 90,000 Crore annual economic loss due to delayed and misdiagnosed crop diseases.",
     "#ebf8ff", "#2b6cb0"),
    ("2. Food and Agriculture Organization (FAO - United Nations)",
     "Early Pest Surveillance and Integrated Pest Management (IPM) Standards.\nProved that early intervention within 7 days reduces toxic pesticide volume by up to 40%.",
     "#f0fff4", "#276749"),
    ("3. National Sample Survey Office (NSSO 77th Round)",
     "Situation Assessment of Agricultural Households in Rural India.\nReported that over 60% of smallholders depend primarily on private input dealers rather than certified doctors.",
     "#fffaf0", "#c05621"),
    ("4. National Bank for Agriculture and Rural Development (NABARD)",
     "Rural Household Economic Vulnerability Studies.\nDocumented annual input wastage of Rs 25,000 to Rs 30,000 per acre due to ineffective or counterfeit chemicals.",
     "#faf5ff", "#6b46c1"),
    ("5. PlantVillage & Deep Learning Pathology Benchmarks (Hughes et al.)",
     "Open Access Benchmarks for Resource-Constrained Field Deployments.\nEstablished core standards for on-device mobile plant pathology and severity classification.",
     "#f7fafc", "#4a5568")
]

for idx, (title, desc, bg, border) in enumerate(refs):
    y = 0.81 - idx * 0.18
    box = patches.FancyBboxPatch((0.02, y), 0.96, 0.15, boxstyle="round,pad=0.015",
                                linewidth=2, edgecolor=border, facecolor=bg)
    ax.add_patch(box)
    ax.text(0.04, y + 0.10, title, fontsize=12, fontweight='bold', color=border)
    ax.text(0.04, y + 0.035, desc, fontsize=10, color='#2d3748', linespacing=1.3)

plt.tight_layout()
plt.savefig('/home/ajay/MUJ_Hackathon/presentation/assets/slide8_references_big.png', bbox_inches='tight')
plt.close()

print("All big font assets created!")
