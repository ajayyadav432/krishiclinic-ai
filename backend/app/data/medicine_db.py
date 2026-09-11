"""
Crop Disease Treatment Database
Based on agronomist-verified stage-wise treatment protocols.
Covers 11 major crops across 3 growth stages: Sowing, Mid-Season, Pre-Harvest.
"""

from typing import Any

# Structure: disease → crop → stage → treatment details
# Also supports crop → disease → treatments for quick agronomist lookup

MEDICINE_DB: dict[str, Any] = {
    "Wheat": {
        "Yellow Rust": {
            "sowing": {
                "chemical": "Carbendazim 50% WP (2g/kg seed)",
                "fungicide": "Propiconazole 25% EC (1ml/L) as prophylactic spray",
                "organic": "Neem oil 3000 ppm (3ml/L), spray at tillering",
                "dose": "Seed treatment: Carbendazim 2g + Thiram 2g per kg seed",
                "frequency": "Once at sowing; foliar at 30-35 DAS",
                "notes": "Use certified disease-free seed. Treat seed with Vitavax-175 (2.5g/kg).",
            },
            "mid_season": {
                "chemical": "Propiconazole 25% EC (0.1%) OR Tebuconazole 25.9% EC (1ml/L)",
                "fungicide": "Hexaconazole 5% SC (2ml/L)",
                "organic": "Trichoderma viride (4g/L) + Neem extract",
                "dose": "500-600 L spray solution/ha",
                "frequency": "2 sprays at 10-day interval when 5% incidence",
                "notes": "Add Mancozeb 75% WP (2.5g/L) for broad-spectrum protection.",
            },
            "pre_harvest": {
                "chemical": "Tebuconazole 25.9% EC (1ml/L); stop 14 days before harvest",
                "fungicide": "Mancozeb 75% WP (2.5g/L); PHI 7 days",
                "organic": "Bordeaux mixture (1%) if organic certification required",
                "dose": "400-500 L spray solution/ha",
                "frequency": "Single spray at boot leaf stage",
                "notes": "Maintain PHI strictly. Avoid Triadimefon during grain filling.",
            },
        },
        "Leaf Blight": {
            "sowing": {
                "chemical": "Carboxin 37.5% + Thiram 37.5% DS (2.5g/kg seed)",
                "fungicide": "Iprodione 25% WP (2g/kg seed treatment)",
                "organic": "Pseudomonas fluorescens (10g/kg seed)",
                "dose": "Seed treatment only",
                "frequency": "Once at sowing",
                "notes": "Crop rotation with non-host crops recommended.",
            },
            "mid_season": {
                "chemical": "Mancozeb 75% WP (2g/L) + Zineb 75% WP (2g/L)",
                "fungicide": "Propiconazole 25% EC (1ml/L)",
                "organic": "Bordeaux mixture 1% (10g copper sulphate + 10g lime/L)",
                "dose": "600-750 L/ha",
                "frequency": "3 sprays at 15-day intervals from flag leaf emergence",
                "notes": "Ensure spray coverage on flag leaf.",
            },
            "pre_harvest": {
                "chemical": "Mancozeb 75% WP (2.5g/L); PHI 7 days",
                "fungicide": "Copper oxychloride 50% WP (3g/L); PHI 7 days",
                "organic": "Trichoderma harzianum (4g/L) soil drench",
                "dose": "400 L/ha",
                "frequency": "Once at milky grain stage",
                "notes": "Harvest at physiological maturity to reduce losses.",
            },
        },
        "Stem Rust": {
            "sowing": {
                "chemical": "Thiram 75% WS (2.5g/kg seed)",
                "fungicide": "Metalaxyl 35% WS (6g/kg seed)",
                "organic": "Trichoderma viride (4g/kg seed)",
                "dose": "Seed treatment",
                "frequency": "Once before sowing",
                "notes": "Plant resistant varieties (HD-2967, WH-1105).",
            },
            "mid_season": {
                "chemical": "Propiconazole 25% EC (1ml/L) OR Triadimefon 25% WP (1g/L)",
                "fungicide": "Tebuconazole + Triadimenol mixture (1ml/L)",
                "organic": "Neem oil 0.5% (5ml/L) + Pseudomonas suspension",
                "dose": "500-600 L/ha",
                "frequency": "2 sprays 10 days apart when pustules appear",
                "notes": "Apply early morning for better absorption.",
            },
            "pre_harvest": {
                "chemical": "Propiconazole 25% EC (0.1%); PHI 14 days",
                "fungicide": "Hexaconazole 5% SC (2ml/L); PHI 14 days",
                "organic": "Bordeaux mixture 0.5%",
                "dose": "400 L/ha",
                "frequency": "Once at heading stage",
                "notes": "Do not apply within 2 weeks of harvest.",
            },
        },
        "Powdery Mildew": {
            "sowing": {
                "chemical": "Sulfur 80% WDG (3kg/ha as soil application)",
                "fungicide": "Carboxin seed treatment (2g/kg seed)",
                "organic": "Wood ash dusting on foliage",
                "dose": "Seed treatment + foliar at tillering",
                "frequency": "Seed treatment once; foliar as needed",
                "notes": "Avoid dense planting. Maintain air circulation.",
            },
            "mid_season": {
                "chemical": "Wettable Sulfur 80% WP (3g/L) OR Tridemorph 75% EC (0.5ml/L)",
                "fungicide": "Difenoconazole 25% EC (0.05%)",
                "organic": "Potassium bicarbonate 5g/L solution",
                "dose": "500 L/ha",
                "frequency": "2-3 sprays at 10-day intervals from disease onset",
                "notes": "Sulfur is very effective; do not apply above 35°C.",
            },
            "pre_harvest": {
                "chemical": "Sulfur dust 325 mesh (20-25 kg/ha); PHI 7 days",
                "fungicide": "Myclobutanil 10% WP (1g/L); PHI 14 days",
                "organic": "Neem-based fungicide (3ml/L)",
                "dose": "400 L/ha",
                "frequency": "Once if needed",
                "notes": "Avoid in hot weather. PHI must be strictly followed.",
            },
        },
        "Karnal Bunt": {
            "sowing": {
                "chemical": "Carboxin + Thiram (Vitavax Power 75 WP) 2.5g/kg seed",
                "fungicide": "Tebuconazole 2% DS (1.5g/kg seed)",
                "organic": "Hot water treatment (52°C for 10 min) + Bioagent",
                "dose": "Seed treatment",
                "frequency": "Once before sowing",
                "notes": "Use disease-free certified seed. Quarantine restrictions apply.",
            },
            "mid_season": {
                "chemical": "Propiconazole 25% EC (1ml/L) at boot leaf stage",
                "fungicide": "Tricyclazole 75% WP (0.6g/L)",
                "organic": "Not effective for Karnal Bunt; chemical control mandatory",
                "dose": "500 L/ha",
                "frequency": "Once spray at 50% heading",
                "notes": "Critical window: 50% anthesis to 7 days after.",
            },
            "pre_harvest": {
                "chemical": "Avoid late-season fungicides; harvested grain must be tested",
                "fungicide": "None recommended post-heading",
                "organic": "None",
                "dose": "N/A",
                "frequency": "N/A",
                "notes": "Quarantine infected lots. Buntted grain unsafe for consumption.",
            },
        },
    },
    "Rice": {
        "Blast": {
            "sowing": {
                "chemical": "Tricyclazole 75% WP (2g/kg seed) OR Carbendazim (2g/kg)",
                "fungicide": "Iprobenfos 48% EC (1.5ml/L seed soak)",
                "organic": "Pseudomonas fluorescens (10g/kg seed coating)",
                "dose": "Seed treatment + nursery drench",
                "frequency": "Once at seed treatment; nursery spray at 15 DAS",
                "notes": "Avoid excess nitrogen. Use blast-resistant varieties.",
            },
            "mid_season": {
                "chemical": "Tricyclazole 75% WP (0.6g/L) OR Azoxystrobin 23% SC (1ml/L)",
                "fungicide": "Isoprothiolane 40% EC (1.5ml/L)",
                "organic": "Trichoderma asperellum (4g/L) + Pseudomonas",
                "dose": "500 L/ha",
                "frequency": "2 sprays: at tillering and booting stage",
                "notes": "Neck blast (panicle blast) spray at panicle initiation is critical.",
            },
            "pre_harvest": {
                "chemical": "Tricyclazole 75% WP (0.6g/L); PHI 21 days",
                "fungicide": "Propiconazole 25% EC (1ml/L); PHI 14 days",
                "organic": "None effective at this stage",
                "dose": "400 L/ha",
                "frequency": "Once at 50% heading",
                "notes": "Critical spray to prevent panicle/neck blast.",
            },
        },
        "Bacterial Leaf Blight": {
            "sowing": {
                "chemical": "Streptomycin sulfate 90% + Tetracycline hydrochloride 10% (Plantomycin) — seed soak",
                "fungicide": "Copper oxychloride seed priming (3g/L for 12 hrs)",
                "organic": "Pseudomonas fluorescens seed treatment (10g/kg)",
                "dose": "Seed soak 8-12 hrs; coat and dry before sowing",
                "frequency": "Once",
                "notes": "Avoid water-logging. Disease spread by flood water.",
            },
            "mid_season": {
                "chemical": "Streptomycin 200ppm + Copper oxychloride 0.25% spray",
                "fungicide": "Copper hydroxide 77% WP (3g/L)",
                "organic": "Pseudomonas fluorescens spray (5g/L)",
                "dose": "500-600 L/ha",
                "frequency": "2-3 sprays at 10-day intervals from early symptom",
                "notes": "Drain standing water when disease appears. Avoid high N.",
            },
            "pre_harvest": {
                "chemical": "Copper oxychloride 50% WP (3g/L); PHI 7 days",
                "fungicide": "Kasugamycin 3% SL (2ml/L); PHI 14 days",
                "organic": "Bordeaux mixture 1%",
                "dose": "400 L/ha",
                "frequency": "Once if needed",
                "notes": "Reduce nitrogen. Avoid overhead irrigation.",
            },
        },
        "Brown Spot": {
            "sowing": {
                "chemical": "Mancozeb 75% WP (3g/kg seed) + Carbendazim (2g/kg seed)",
                "fungicide": "Iprobenfos 48% EC (1.5ml/kg seed soak)",
                "organic": "Hot water treatment 54°C for 10 min + bioagent coat",
                "dose": "Seed treatment",
                "frequency": "Once",
                "notes": "Balanced nutrition (especially K and Si) reduces severity.",
            },
            "mid_season": {
                "chemical": "Mancozeb 75% WP (2.5g/L) OR Propiconazole 25% EC (1ml/L)",
                "fungicide": "Edifenphos 50% EC (1ml/L)",
                "organic": "Neem oil 0.5% + Trichoderma (4g/L)",
                "dose": "500 L/ha",
                "frequency": "2 sprays at 15-day intervals from tillering",
                "notes": "Improve nutrition—Brown Spot is often linked to potassium deficiency.",
            },
            "pre_harvest": {
                "chemical": "Mancozeb 75% WP (2.5g/L); PHI 7 days",
                "fungicide": "Propiconazole 25% EC (1ml/L); PHI 14 days",
                "organic": "Copper oxychloride 0.3%",
                "dose": "400 L/ha",
                "frequency": "Once at booting stage",
                "notes": "Ensure timely harvest to limit grain discoloration.",
            },
        },
        "Sheath Blight": {
            "sowing": {
                "chemical": "Carbendazim 50% WP (2g/kg seed)",
                "fungicide": "Validamycin A 3% L (2ml/L soil application in nursery)",
                "organic": "Trichoderma harzianum (4g/kg seed + soil mix)",
                "dose": "Seed + nursery bed treatment",
                "frequency": "Once at sowing + nursery bed",
                "notes": "Reduce transplanting density. Maintain optimal spacing.",
            },
            "mid_season": {
                "chemical": "Validamycin A 3% SL (2ml/L) OR Hexaconazole 5% SC (2ml/L)",
                "fungicide": "Propiconazole 25% EC (1ml/L)",
                "organic": "Trichoderma viride (4g/L) spray at water line",
                "dose": "500-600 L/ha; target water line and lower leaves",
                "frequency": "2 sprays at 15-day intervals from tillering",
                "notes": "Spray at lower canopy. Reduce standing water depth.",
            },
            "pre_harvest": {
                "chemical": "Hexaconazole 5% SC (2ml/L); PHI 21 days",
                "fungicide": "Propiconazole 25% EC (1ml/L); PHI 14 days",
                "organic": "Pseudomonas fluorescens spray (5g/L)",
                "dose": "400 L/ha",
                "frequency": "Once at panicle initiation if needed",
                "notes": "Target lower canopy. Late spray minimally effective.",
            },
        },
    },
    "Tomato": {
        "Early Blight": {
            "sowing": {
                "chemical": "Thiram 75% WS (3g/kg seed) + Carbendazim (2g/kg seed)",
                "fungicide": "Trichoderma viride seed coating (4g/kg)",
                "organic": "Hot water treatment 52°C 25 min, dry, Trichoderma coat",
                "dose": "Seed treatment",
                "frequency": "Once",
                "notes": "Use transplants from disease-free nursery. 3-yr crop rotation.",
            },
            "mid_season": {
                "chemical": "Mancozeb 75% WP (2g/L) OR Chlorothalonil 75% WP (2g/L)",
                "fungicide": "Iprodione 50% WP (2g/L) OR Tebuconazole 25.9% EC (1ml/L)",
                "organic": "Copper-based fungicide (Copper hydroxide 77% WP 2g/L)",
                "dose": "500-600 L/ha",
                "frequency": "Every 7-10 days from 30 DAS or first symptom",
                "notes": "Alternate fungicide groups to prevent resistance.",
            },
            "pre_harvest": {
                "chemical": "Mancozeb 75% WP (2g/L); PHI 5 days",
                "fungicide": "Azoxystrobin 23% SC (0.5ml/L); PHI 3 days",
                "organic": "Bicarbonate spray (5g/L potassium bicarbonate)",
                "dose": "400 L/ha",
                "frequency": "Every 7 days in severe infections",
                "notes": "Low PHI fungicides only. Harvest ripe fruit promptly.",
            },
        },
        "Late Blight": {
            "sowing": {
                "chemical": "Metalaxyl 35% WS (6g/kg seed) OR Mefenoxam 35% WS",
                "fungicide": "Mancozeb 75% WP (3g/kg seed treatment)",
                "organic": "Bacillus subtilis (10g/kg seed coating) + Trichoderma",
                "dose": "Seed treatment",
                "frequency": "Once",
                "notes": "Use certified disease-free transplants. Avoid overhead irrigation.",
            },
            "mid_season": {
                "chemical": "Metalaxyl + Mancozeb (Ridomil Gold MZ 68 WG 2.5g/L) OR Dimethomorph + Mancozeb",
                "fungicide": "Cymoxanil + Mancozeb (0.3%) OR Famoxadone + Cymoxanil",
                "organic": "Copper hydroxide 77% WP (2g/L); Bacillus amyloliquefaciens spray",
                "dose": "500-750 L/ha",
                "frequency": "Every 5-7 days during cool, humid weather (high risk)",
                "notes": "Late blight spreads very fast. Start preventive spray 30 DAS.",
            },
            "pre_harvest": {
                "chemical": "Cymoxanil 8% + Mancozeb 64% WP (2.5g/L); PHI 7 days",
                "fungicide": "Copper oxychloride 50% WP (3g/L); PHI 7 days",
                "organic": "Bordeaux mixture 1%; PHI 5 days",
                "dose": "400-500 L/ha",
                "frequency": "Every 7 days until 2 weeks pre-harvest",
                "notes": "Harvest at first color break if pressure is high.",
            },
        },
        "Fusarium Wilt": {
            "sowing": {
                "chemical": "Carbendazim 50% WP (2g/kg seed) soil drench at transplanting",
                "fungicide": "Propiconazole soil drench (0.1%) at transplanting",
                "organic": "Trichoderma harzianum (250g/kg FYM; incorporate into soil)",
                "dose": "Seed treatment + soil treatment at transplanting",
                "frequency": "Once each at sowing and transplanting",
                "notes": "Use Fusarium-resistant varieties. Raised beds improve drainage.",
            },
            "mid_season": {
                "chemical": "Carbendazim 50% WP (1g/L) soil drench at root zone",
                "fungicide": "Thiophanate-methyl 70% WP (1.5g/L) soil application",
                "organic": "Pseudomonas fluorescens drench (10g/L) at base of plant",
                "dose": "250ml drench per plant",
                "frequency": "2-3 drenches at 10-day intervals from first wilt symptom",
                "notes": "Remove and destroy wilted plants. Avoid water stress.",
            },
            "pre_harvest": {
                "chemical": "No effective chemical control post fruit-set if wilting",
                "fungicide": "Preventive drench: Carbendazim 1g/L up to 3 weeks before harvest",
                "organic": "Trichoderma drench (4g/L)",
                "dose": "250ml/plant",
                "frequency": "Once if needed",
                "notes": "Wilted plants cannot be saved. Focus on next-season prevention.",
            },
        },
        "Leaf Curl Virus": {
            "sowing": {
                "chemical": "Imidacloprid 70% WS (5g/kg seed) for vector (whitefly) control",
                "fungicide": "No fungicide — viral disease. Control vector whitefly.",
                "organic": "Yellow sticky traps + Neem oil 3ml/L spray on seedlings",
                "dose": "Insecticide seed treatment; traps at 10/acre",
                "frequency": "Once at sowing + weekly monitoring",
                "notes": "TLCV is spread by Bemisia tabaci. Remove infected plants immediately.",
            },
            "mid_season": {
                "chemical": "Thiamethoxam 25% WG (0.3g/L) OR Acetamiprid 20% SP (0.3g/L) for whitefly",
                "fungicide": "No fungicide. Antiviral not commercially available.",
                "organic": "Neem oil 3ml/L + Pyrethrin spray; silver mulch for repellence",
                "dose": "500 L/ha; alternate chemicals",
                "frequency": "Every 7 days for whitefly management",
                "notes": "Rogue out infected plants. Apply mineral oil (1%) to slow virus spread.",
            },
            "pre_harvest": {
                "chemical": "Spiromesifen 22.9% SC (0.75ml/L) for whitefly; PHI 7 days",
                "fungicide": "None",
                "organic": "Soap solution 1% + Neem oil",
                "dose": "400 L/ha",
                "frequency": "As needed for whitefly control",
                "notes": "Infected fruit yield is reduced. Focus on next crop management.",
            },
        },
    },
    "Corn": {
        "Northern Leaf Blight": {
            "sowing": {
                "chemical": "Thiram 75% WS (3g/kg seed) + Metalaxyl 35% WS (6g/kg seed)",
                "fungicide": "Carboxin + Thiram mixture (Vitavax 2.5g/kg seed)",
                "organic": "Trichoderma harzianum (4g/kg seed)",
                "dose": "Seed treatment",
                "frequency": "Once",
                "notes": "Plant resistant hybrids. Crop rotation breaks disease cycle.",
            },
            "mid_season": {
                "chemical": "Propiconazole 25% EC (1ml/L) OR Azoxystrobin 23% SC (1ml/L)",
                "fungicide": "Tebuconazole 25.9% EC (1ml/L) OR Mancozeb 75% WP (2g/L)",
                "organic": "Copper-based spray (Copper oxychloride 3g/L)",
                "dose": "500-600 L/ha",
                "frequency": "2 sprays at tasseling and silking stages",
                "notes": "Spray at first appearance of lesions (elongated, tan-colored).",
            },
            "pre_harvest": {
                "chemical": "Mancozeb 75% WP (2.5g/L); PHI 7 days",
                "fungicide": "Propiconazole 25% EC (1ml/L); PHI 14 days",
                "organic": "Bordeaux mixture 1%",
                "dose": "400 L/ha",
                "frequency": "Once if needed at dough stage",
                "notes": "Late-season control has limited economic value.",
            },
        },
        "Common Rust": {
            "sowing": {
                "chemical": "Thiram 75% WS (3g/kg seed)",
                "fungicide": "Metalaxyl seed treatment (6g/kg seed)",
                "organic": "Trichoderma viride (4g/kg seed)",
                "dose": "Seed treatment",
                "frequency": "Once",
                "notes": "Plant resistant hybrids. Rust spores are airborne.",
            },
            "mid_season": {
                "chemical": "Propiconazole 25% EC (1ml/L) OR Tebuconazole 25.9% EC (1ml/L)",
                "fungicide": "Mancozeb 75% WP (2g/L) + Zineb 75% WP (2g/L)",
                "organic": "Sulfur dust (fine mesh) or wettable sulfur (3g/L)",
                "dose": "500 L/ha",
                "frequency": "2 sprays at 10-day intervals from pustule appearance",
                "notes": "Economic threshold: 5% leaf area infected before tasseling.",
            },
            "pre_harvest": {
                "chemical": "Propiconazole 25% EC (1ml/L); PHI 14 days",
                "fungicide": "Tebuconazole 25.9% EC (1ml/L); PHI 14 days",
                "organic": "Neem oil 0.5% + copper-based spray",
                "dose": "400 L/ha",
                "frequency": "Once if needed",
                "notes": "Control before dent stage for maximum benefit.",
            },
        },
        "Stalk Rot": {
            "sowing": {
                "chemical": "Carbendazim 50% WP (2g/kg seed) + Thiram 75% WS (3g/kg seed)",
                "fungicide": "Metalaxyl 35% WS (6g/kg seed) for Pythium component",
                "organic": "Trichoderma harzianum (4g/kg seed) soil incorporation",
                "dose": "Seed treatment + soil enrichment",
                "frequency": "Once",
                "notes": "Avoid waterlogging. Balanced N-P-K (especially K) crucial.",
            },
            "mid_season": {
                "chemical": "Carbendazim 1g/L soil drench at stalk base; Propiconazole foliar",
                "fungicide": "Thiophanate-methyl 70% WP (1.5g/L) soil drench",
                "organic": "Pseudomonas fluorescens soil drench (10g/L)",
                "dose": "250ml drench per plant",
                "frequency": "2 drenches at 10-day intervals from symptom onset",
                "notes": "Potassium top-dress (60 kg/ha MOP) improves stalk strength.",
            },
            "pre_harvest": {
                "chemical": "No effective control. Harvest early if >10% stalk rot",
                "fungicide": "Preventive: Carbendazim drench (1g/L) at green stage",
                "organic": "None effective",
                "dose": "250ml/plant",
                "frequency": "Preventive once",
                "notes": "Timely harvest prevents total loss from stalk lodging.",
            },
        },
        "Gray Leaf Spot": {
            "sowing": {
                "chemical": "Carbendazim 50% WP (2g/kg seed) + Mancozeb (2g/kg seed)",
                "fungicide": "Thiram 75% WS (3g/kg seed)",
                "organic": "Trichoderma viride (4g/kg seed coating)",
                "dose": "Seed treatment",
                "frequency": "Once",
                "notes": "Resistant hybrids are most cost-effective management strategy.",
            },
            "mid_season": {
                "chemical": "Azoxystrobin 23% SC (1ml/L) OR Propiconazole 25% EC (1ml/L)",
                "fungicide": "Trifloxystrobin + Propiconazole (0.5+0.5 ml/L)",
                "organic": "Copper oxychloride 50% WP (3g/L)",
                "dose": "500 L/ha",
                "frequency": "2 sprays: V8 stage and tasseling",
                "notes": "GLS thrives in humid, low-light conditions. Improve row spacing.",
            },
            "pre_harvest": {
                "chemical": "Propiconazole 25% EC (1ml/L); PHI 14 days",
                "fungicide": "Tebuconazole 25.9% EC (1ml/L); PHI 14 days",
                "organic": "Bordeaux mixture 1%",
                "dose": "400 L/ha",
                "frequency": "Once if needed",
                "notes": "Late-season sprays may not be economically justified.",
            },
        },
    },
    "Potato": {
        "Late Blight": {
            "sowing": {
                "chemical": "Mancozeb 75% WP (3g/kg seed) tuber treatment OR Metalaxyl 35% WS",
                "fungicide": "Cymoxanil + Mancozeb (Curzate M8 2.5g/L) foliage 20 DAS",
                "organic": "Trichoderma harzianum (soil incorporation 2.5kg/acre)",
                "dose": "Tuber dip + soil treatment",
                "frequency": "Once at planting + early spray",
                "notes": "Use certified disease-free seed potato. Avoid infected seed lots.",
            },
            "mid_season": {
                "chemical": "Metalaxyl + Mancozeb (Ridomil Gold MZ 2.5g/L) OR Dimethomorph + Mancozeb",
                "fungicide": "Ametoctradin + Dimethomorph (Zampro 0.6ml/L) alternating",
                "organic": "Copper hydroxide 77% WP (2g/L) + Bacillus amyloliquefaciens",
                "dose": "750 L/ha",
                "frequency": "Every 5-7 days during cool (<20°C) wet weather (high risk)",
                "notes": "Late blight spreads very rapidly. Preventive calendar spray in risk areas.",
            },
            "pre_harvest": {
                "chemical": "Copper oxychloride 50% WP (3g/L); PHI 7 days",
                "fungicide": "Cymoxanil 8% + Mancozeb 64% (2.5g/L); PHI 7 days",
                "organic": "Bordeaux mixture 1%; PHI 5 days",
                "dose": "500 L/ha",
                "frequency": "Last spray 7-10 days before vine killing",
                "notes": "Kill vines (haulms) 2-3 weeks before harvest to harden skins.",
            },
        },
        "Common Scab": {
            "sowing": {
                "chemical": "Fludioxonil 2.5% FS (40ml/100L water; tuber dip 5 min)",
                "fungicide": "PCNB 20% EC (tuber dip 10 min)",
                "organic": "Acidify soil pH to 5.0-5.4 with sulfur (500g/sq m)",
                "dose": "Tuber dip treatment",
                "frequency": "Once at planting",
                "notes": "pH below 5.5 greatly reduces scab. Certified seed mandatory.",
            },
            "mid_season": {
                "chemical": "No foliar spray effective. Soil drenching with Thiophanate-methyl",
                "fungicide": "Fludioxonil soil application (early tuberization stage)",
                "organic": "Gypsum application (400kg/ha) + green manure incorporation",
                "dose": "Soil treatment",
                "frequency": "Once at tuberization",
                "notes": "Maintain even soil moisture during tuber initiation and bulking.",
            },
            "pre_harvest": {
                "chemical": "No effective chemical at this stage",
                "fungicide": "None",
                "organic": "None",
                "dose": "N/A",
                "frequency": "N/A",
                "notes": "Scab is a cosmetic issue. Controlled atmosphere storage reduces severity.",
            },
        },
        "Black Scurf": {
            "sowing": {
                "chemical": "Pencycuron 25% WP (2g/kg seed potato) OR Flutolanil 17.5% + Pencycuron 12.5%",
                "fungicide": "Thiram 75% WS seed dip (5g/L for 5 min)",
                "organic": "Trichoderma harzianum 4g/kg seed potato + soil incorporation",
                "dose": "Seed treatment",
                "frequency": "Once",
                "notes": "Tuber-borne disease. Use disease-free seed from certified sources.",
            },
            "mid_season": {
                "chemical": "Pencycuron soil drench (1.5g/L at hilling-up)",
                "fungicide": "Flutolanil 17.5% WP (2g/L) soil drench",
                "organic": "Trichoderma harzianum soil drench (4g/L)",
                "dose": "Drench 250ml per plant base",
                "frequency": "Once at hilling/earthing-up",
                "notes": "Avoid excessive irrigation. Proper earthing-up prevents spread.",
            },
            "pre_harvest": {
                "chemical": "No effective control late season",
                "fungicide": "None",
                "organic": "None",
                "dose": "N/A",
                "frequency": "N/A",
                "notes": "Harvest at the right maturity. Dry tubers properly before storage.",
            },
        },
        "Early Blight": {
            "sowing": {
                "chemical": "Mancozeb 75% WP (3g/kg seed) + Carbendazim (2g/kg seed)",
                "fungicide": "Metalaxyl 35% WS tuber dip (1g/L for 10 min)",
                "organic": "Trichoderma viride seed coating (4g/kg seed)",
                "dose": "Seed treatment + early spray",
                "frequency": "Once at planting; first foliar at 20 DAS",
                "notes": "Healthy plants more tolerant. Balanced nutrition helps.",
            },
            "mid_season": {
                "chemical": "Mancozeb 75% WP (2g/L) OR Chlorothalonil 75% WP (2g/L)",
                "fungicide": "Difenoconazole 25% EC (0.05%) alternating with Mancozeb",
                "organic": "Copper oxychloride 0.3% + Neem oil 0.5%",
                "dose": "500-750 L/ha",
                "frequency": "Every 10-14 days from 30 DAS",
                "notes": "Alternate fungicide groups every 2 sprays to prevent resistance.",
            },
            "pre_harvest": {
                "chemical": "Mancozeb 75% WP (2g/L); PHI 5 days",
                "fungicide": "Azoxystrobin 23% SC (0.5ml/L); PHI 3 days",
                "organic": "Bordeaux mixture 1%",
                "dose": "400 L/ha",
                "frequency": "Once if needed",
                "notes": "Late-season spray protects leaf area for tuber filling.",
            },
        },
    },
    "Cotton": {
        "Bacterial Blight": {
            "sowing": {
                "chemical": "Streptomycin 90% + Tetracycline 10% seed treatment (Plantomycin 1g/kg seed)",
                "fungicide": "Copper oxychloride seed priming (3g/L 12 hr soak)",
                "organic": "Pseudomonas fluorescens (10g/kg seed)",
                "dose": "Seed treatment + early foliar",
                "frequency": "Once at sowing; foliar from 30 DAS",
                "notes": "Use Angular Leaf Spot resistant varieties. Acid-delinted seed preferred.",
            },
            "mid_season": {
                "chemical": "Streptomycin sulfate (200ppm) + Copper oxychloride 0.25%",
                "fungicide": "Copper hydroxide 77% WP (3g/L)",
                "organic": "Pseudomonas fluorescens spray (5g/L)",
                "dose": "600-750 L/ha",
                "frequency": "3 sprays at 10-day intervals from boll initiation",
                "notes": "Disease spreads fast in wet weather. Avoid overhead irrigation.",
            },
            "pre_harvest": {
                "chemical": "Copper oxychloride 50% WP (3g/L); PHI 7 days",
                "fungicide": "Kasugamycin 3% SL (2ml/L); PHI 14 days",
                "organic": "Bordeaux mixture 1%",
                "dose": "400 L/ha",
                "frequency": "Once before boll opening",
                "notes": "Reduce boll rot risk by avoiding irrigation in late season.",
            },
        },
        "Cotton Leaf Curl Virus": {
            "sowing": {
                "chemical": "Imidacloprid 70% WS (5g/kg seed) for thrips/whitefly control",
                "fungicide": "No fungicide — viral disease",
                "organic": "Yellow sticky traps at 20/ha + Neem oil spray (3ml/L)",
                "dose": "Insecticide seed coat",
                "frequency": "Once at sowing + weekly monitoring",
                "notes": "CLCuV spread by Bemisia tabaci. Use CLCuV-tolerant varieties.",
            },
            "mid_season": {
                "chemical": "Thiamethoxam 25% WG (0.3g/L) OR Spiromesifen 22.9% SC (0.75ml/L) for whitefly",
                "fungicide": "None. Antiviral compounds not registered.",
                "organic": "Neem oil 5ml/L + Pyrethrin 0.1% alternating sprays",
                "dose": "500-600 L/ha",
                "frequency": "Every 10 days for whitefly pressure",
                "notes": "Rogue out heavily infected plants. Avoid monoculture.",
            },
            "pre_harvest": {
                "chemical": "Pyriproxyfen 10% EC (1ml/L) for whitefly; PHI 7 days",
                "fungicide": "None",
                "organic": "Soap spray 1% + Neem oil",
                "dose": "400 L/ha",
                "frequency": "As needed",
                "notes": "Viral infection reduces lint quality. Timely harvest minimizes loss.",
            },
        },
        "Alternaria Leaf Spot": {
            "sowing": {
                "chemical": "Thiram 75% WS (3g/kg seed) + Carbendazim (2g/kg seed)",
                "fungicide": "Iprodione 50% WP seed dip (2g/L for 10 min)",
                "organic": "Trichoderma viride seed coating (4g/kg seed)",
                "dose": "Seed treatment",
                "frequency": "Once",
                "notes": "Crop rotation and field sanitation reduce inoculum.",
            },
            "mid_season": {
                "chemical": "Mancozeb 75% WP (2.5g/L) OR Iprodione 50% WP (2g/L)",
                "fungicide": "Propiconazole 25% EC (1ml/L)",
                "organic": "Copper oxychloride 3g/L",
                "dose": "500 L/ha",
                "frequency": "2-3 sprays at 10-day intervals",
                "notes": "Improves canopy air circulation by avoiding dense planting.",
            },
            "pre_harvest": {
                "chemical": "Mancozeb 75% WP (2.5g/L); PHI 7 days",
                "fungicide": "Chlorothalonil 75% WP (2g/L); PHI 7 days",
                "organic": "Bordeaux mixture 1%",
                "dose": "400 L/ha",
                "frequency": "Once if needed",
                "notes": "Late-season sprays protect boll development.",
            },
        },
    },
    "Sugarcane": {
        "Red Rot": {
            "sowing": {
                "chemical": "Carbendazim 50% WP (1g/L sett soak for 10-15 min)",
                "fungicide": "Propiconazole 25% EC (1ml/L sett soak)",
                "organic": "Trichoderma viride suspension (4g/L sett soak)",
                "dose": "Sett treatment; soak 10-15 min before planting",
                "frequency": "Once at planting",
                "notes": "Use disease-free setts from certified seed cane. Avoid ratoon cropping in infected fields.",
            },
            "mid_season": {
                "chemical": "Propiconazole 25% EC (1ml/L) foliar spray",
                "fungicide": "Carbendazim 50% WP (1g/L) stem base drench",
                "organic": "Pseudomonas fluorescens (10g/L) drenching",
                "dose": "500 L/ha foliar or 250ml/plant drench",
                "frequency": "2-3 sprays at monthly intervals from symptom appearance",
                "notes": "Remove and destroy infected stalks. Do not leave them in field.",
            },
            "pre_harvest": {
                "chemical": "Propiconazole 25% EC (1ml/L); PHI 21 days",
                "fungicide": "Carbendazim 50% WP (1g/L); PHI 14 days",
                "organic": "None effective",
                "dose": "400 L/ha",
                "frequency": "Once if needed; harvest promptly if >30% incidence",
                "notes": "Infected cane loses sucrose content rapidly. Harvest ASAP.",
            },
        },
        "Smut": {
            "sowing": {
                "chemical": "Carboxin 75% WP (2g/kg sett) hot water treatment (50°C, 2 hrs) + fungicide dip",
                "fungicide": "Triadimefon 25% WP (2g/L sett soak) + hot water",
                "organic": "Hot water treatment (50°C for 2 hrs) — highly effective",
                "dose": "Hot water treatment mandatory; fungicide dip as additional measure",
                "frequency": "Once at planting",
                "notes": "Plant resistant varieties (Co 86032, CoS 8436). Only disease-free ratoons.",
            },
            "mid_season": {
                "chemical": "Triadimefon 25% WP (1g/L) foliar spray",
                "fungicide": "Propiconazole 25% EC (1ml/L) when whip (black sorus) appears",
                "organic": "Remove smutted whips before spore release; bag and destroy",
                "dose": "Roguing + foliar",
                "frequency": "Remove smutted whips weekly; foliar 2 times at 30-day intervals",
                "notes": "Smut whip = entire stalk converted to black fungal mass. Remove immediately.",
            },
            "pre_harvest": {
                "chemical": "Propiconazole 25% EC (1ml/L); PHI 21 days",
                "fungicide": "Carboxin 75% WP (2g/L); PHI 21 days",
                "organic": "None effective",
                "dose": "500 L/ha",
                "frequency": "Once if needed",
                "notes": "Do not use infected ratoon. Test new seed cane for smut.",
            },
        },
        "Grassy Shoot Disease": {
            "sowing": {
                "chemical": "Hot water treatment (50°C for 2.5 hrs) only — caused by phytoplasma",
                "fungicide": "No fungicide effective (phytoplasma disease)",
                "organic": "Tetracycline injection (200mg/L) in sett via injection method",
                "dose": "Heat treatment mandatory",
                "frequency": "Once at planting",
                "notes": "Vector: Leafhopper (Pyrilla perpusilla). Insecticide for vector control.",
            },
            "mid_season": {
                "chemical": "Oxytetracycline 3% in water (100ppm) injection into stalk",
                "fungicide": "Not applicable",
                "organic": "Roguing affected plants. Insecticide for leafhopper vector (Chlorpyrifos)",
                "dose": "Injection method",
                "frequency": "Remove affected plants immediately; insecticide monthly",
                "notes": "No cure available. Rogue and destroy affected stools.",
            },
            "pre_harvest": {
                "chemical": "Vector control: Imidacloprid 17.8% SL (0.5ml/L); PHI 21 days",
                "fungicide": "None",
                "organic": "Light traps for leafhopper",
                "dose": "500 L/ha",
                "frequency": "As needed for leafhopper",
                "notes": "Affected cane worthless. Harvest early if heavily infected.",
            },
        },
    },
    "Soybean": {
        "Soybean Rust": {
            "sowing": {
                "chemical": "Thiram 75% WS (3g/kg seed) + Carbendazim (2g/kg seed)",
                "fungicide": "Metalaxyl 35% WS (6g/kg seed)",
                "organic": "Trichoderma viride (4g/kg seed)",
                "dose": "Seed treatment",
                "frequency": "Once",
                "notes": "Plant early (before June 30 for Kharif). Avoid late planting.",
            },
            "mid_season": {
                "chemical": "Trifloxystrobin 25% + Tebuconazole 50% WG (0.5g/L) OR Azoxystrobin + Propiconazole",
                "fungicide": "Hexaconazole 5% SC (2ml/L) OR Propiconazole 25% EC (1ml/L)",
                "organic": "Copper-based spray (Copper hydroxide 2g/L)",
                "dose": "500 L/ha",
                "frequency": "2 sprays: R1 stage and R3 stage (40 & 60 DAS approx.)",
                "notes": "Key window: Sprays at R1 (beginning bloom) and R3 (beginning pod) stages.",
            },
            "pre_harvest": {
                "chemical": "Tebuconazole 25.9% EC (1ml/L); PHI 21 days",
                "fungicide": "Propiconazole 25% EC (1ml/L); PHI 14 days",
                "organic": "Copper oxychloride 0.3%",
                "dose": "400 L/ha",
                "frequency": "Once at R5 (seed fill) if needed",
                "notes": "Late rust reduces seed weight and protein content significantly.",
            },
        },
        "Frogeye Leaf Spot": {
            "sowing": {
                "chemical": "Carbendazim 50% WP (2g/kg seed) + Thiram 75% WS (2.5g/kg seed)",
                "fungicide": "Fludioxonil 2.5% FS (5ml/kg seed)",
                "organic": "Pseudomonas fluorescens (10g/kg seed)",
                "dose": "Seed treatment",
                "frequency": "Once",
                "notes": "Crop rotation. Remove crop debris to reduce inoculum.",
            },
            "mid_season": {
                "chemical": "Thiophanate-methyl 70% WP (1.5g/L) OR Carbendazim 50% WP (1g/L)",
                "fungicide": "Azoxystrobin 23% SC (1ml/L)",
                "organic": "Copper oxychloride 3g/L",
                "dose": "500 L/ha",
                "frequency": "2 sprays at 15-day intervals from pod filling",
                "notes": "Strobilurin resistance reported in USA. Rotate fungicide classes.",
            },
            "pre_harvest": {
                "chemical": "Thiophanate-methyl 70% WP (1.5g/L); PHI 14 days",
                "fungicide": "Propiconazole 25% EC (1ml/L); PHI 14 days",
                "organic": "None effective",
                "dose": "400 L/ha",
                "frequency": "Once if needed at seed fill",
                "notes": "Late-season infections reduce seed germination quality.",
            },
        },
        "Charcoal Rot": {
            "sowing": {
                "chemical": "Fludioxonil 2.5% FS (5ml/kg seed) + Metalaxyl 35% WS (6g/kg seed)",
                "fungicide": "Thiram + Carbendazim (Vitavax Power 2.5g/kg seed)",
                "organic": "Trichoderma harzianum (250g/acre, soil incorporation in FYM)",
                "dose": "Seed treatment + soil enrichment",
                "frequency": "Once",
                "notes": "Charcoal rot worsens under drought stress. Maintain adequate moisture.",
            },
            "mid_season": {
                "chemical": "No effective foliar fungicide. Irrigation is the key management tool.",
                "fungicide": "Thiophanate-methyl 70% WP (1.5g/L) soil drench at stem base",
                "organic": "Trichoderma harzianum drench (4g/L) at stem base",
                "dose": "250ml/plant drench",
                "frequency": "2 drenches at 10-day intervals",
                "notes": "Avoid drought stress. Balanced K and P nutrition critical.",
            },
            "pre_harvest": {
                "chemical": "No effective control. Early harvest if >15% incidence",
                "fungicide": "None",
                "organic": "None",
                "dose": "N/A",
                "frequency": "N/A",
                "notes": "Infected fields show silvery-grey bark at stem base. Harvest promptly.",
            },
        },
        "Target Spot": {
            "sowing": {
                "chemical": "Carbendazim 50% WP (2g/kg seed)",
                "fungicide": "Thiram 75% WS (2.5g/kg seed)",
                "organic": "Trichoderma viride (4g/kg seed)",
                "dose": "Seed treatment",
                "frequency": "Once",
                "notes": "Avoid dense planting. Field sanitation reduces inoculum.",
            },
            "mid_season": {
                "chemical": "Azoxystrobin 23% SC (1ml/L) OR Carbendazim 50% WP (1g/L)",
                "fungicide": "Propiconazole 25% EC (1ml/L) OR Fluxapyroxad + Pyraclostrobin",
                "organic": "Copper oxychloride 0.3% spray",
                "dose": "500 L/ha",
                "frequency": "2-3 sprays at 14-day intervals from R3 stage",
                "notes": "Target spot = concentric zonate lesions. Distinguish from rust.",
            },
            "pre_harvest": {
                "chemical": "Propiconazole 25% EC (1ml/L); PHI 14 days",
                "fungicide": "Azoxystrobin 23% SC (1ml/L); PHI 14 days",
                "organic": "None",
                "dose": "400 L/ha",
                "frequency": "Once at R5 if needed",
                "notes": "Late infections reduce seed quality more than yield.",
            },
        },
    },
    "Mustard": {
        "White Rust": {
            "sowing": {
                "chemical": "Metalaxyl 35% WS (6g/kg seed) OR Ridomil Gold seed treatment",
                "fungicide": "Mancozeb 75% WP (3g/kg seed) + Metalaxyl",
                "organic": "Trichoderma harzianum (4g/kg seed)",
                "dose": "Seed treatment",
                "frequency": "Once",
                "notes": "White rust (Albugo candida) is very common in Mustard. Use tolerant varieties.",
            },
            "mid_season": {
                "chemical": "Metalaxyl + Mancozeb (Ridomil MZ 2.5g/L) OR Fosetyl Aluminum (3g/L)",
                "fungicide": "Mancozeb 75% WP (2.5g/L) + Zineb (2g/L)",
                "organic": "Copper oxychloride 3g/L",
                "dose": "500-600 L/ha",
                "frequency": "2 sprays at 15-day intervals from 30-35 DAS",
                "notes": "White rust pustules appear on underside of leaves. Control early.",
            },
            "pre_harvest": {
                "chemical": "Copper oxychloride 50% WP (3g/L); PHI 7 days",
                "fungicide": "Mancozeb 75% WP (2.5g/L); PHI 7 days",
                "organic": "Bordeaux mixture 1%",
                "dose": "400 L/ha",
                "frequency": "Once if needed at siliqua (pod) filling",
                "notes": "Systemic infection of siliqua causes major yield loss.",
            },
        },
        "Alternaria Blight": {
            "sowing": {
                "chemical": "Thiram 75% WS (3g/kg seed) + Iprodione 50% WP (2g/kg seed)",
                "fungicide": "Carbendazim 50% WP (2g/kg seed)",
                "organic": "Hot water treatment (50°C 30 min) + Trichoderma coat",
                "dose": "Seed treatment",
                "frequency": "Once",
                "notes": "Alternaria is the most damaging Mustard disease in India. Certified seed critical.",
            },
            "mid_season": {
                "chemical": "Iprodione 50% WP (2g/L) OR Propiconazole 25% EC (1ml/L)",
                "fungicide": "Mancozeb 75% WP (2.5g/L) alternating with Iprodione",
                "organic": "Bordeaux mixture 1% OR Copper oxychloride 3g/L",
                "dose": "500-600 L/ha",
                "frequency": "2-3 sprays at 10-15 day intervals from 30 DAS",
                "notes": "Spray at flowering stage is critical. Alternaria blight causes severe defoliation.",
            },
            "pre_harvest": {
                "chemical": "Propiconazole 25% EC (1ml/L); PHI 14 days",
                "fungicide": "Iprodione 50% WP (2g/L); PHI 7 days",
                "organic": "Copper-based fungicide (Copper hydroxide 2g/L)",
                "dose": "400 L/ha",
                "frequency": "Once at siliqua stage if needed",
                "notes": "Siliqua infection causes shriveled seeds. Act quickly at first sign.",
            },
        },
        "Downy Mildew": {
            "sowing": {
                "chemical": "Metalaxyl 35% WS (6g/kg seed)",
                "fungicide": "Mefenoxam 35% WS (6g/kg seed)",
                "organic": "Trichoderma viride (4g/kg seed coating)",
                "dose": "Seed treatment",
                "frequency": "Once",
                "notes": "Downy mildew (Peronospora parasitica) thrives in cool, humid conditions.",
            },
            "mid_season": {
                "chemical": "Metalaxyl + Mancozeb (Ridomil MZ 2.5g/L) OR Dimethomorph (1g/L)",
                "fungicide": "Fosetyl Aluminum 80% WP (3g/L)",
                "organic": "Copper hydroxide 2g/L",
                "dose": "500 L/ha",
                "frequency": "2-3 sprays at 15-day intervals from onset",
                "notes": "White cottony growth on underside of leaves is diagnostic. Spray undersides.",
            },
            "pre_harvest": {
                "chemical": "Copper oxychloride 50% WP (3g/L); PHI 7 days",
                "fungicide": "Mancozeb 75% WP (2.5g/L); PHI 7 days",
                "organic": "Bordeaux mixture 0.5%",
                "dose": "400 L/ha",
                "frequency": "Once if needed",
                "notes": "High humidity at siliqua stage increases risk. Ventilation helps.",
            },
        },
    },
    "Groundnut": {
        "Tikka Disease": {
            "sowing": {
                "chemical": "Carbendazim 50% WP (2g/kg seed) + Thiram 75% WS (3g/kg seed)",
                "fungicide": "Tebuconazole 2% DS (1.5g/kg seed)",
                "organic": "Trichoderma viride (4g/kg seed) + Pseudomonas fluorescens",
                "dose": "Seed treatment (dry coating)",
                "frequency": "Once",
                "notes": "Tikka (Early leaf spot + Late leaf spot) is most important Groundnut disease.",
            },
            "mid_season": {
                "chemical": "Chlorothalonil 75% WP (2g/L) OR Mancozeb 75% WP (2g/L)",
                "fungicide": "Propiconazole 25% EC (1ml/L) OR Tebuconazole 25.9% EC (1ml/L)",
                "organic": "Copper oxychloride 3g/L",
                "dose": "500-600 L/ha",
                "frequency": "3-4 sprays at 10-day intervals from 30 DAS",
                "notes": "Economic threshold: 5-6 lesions per leaflet. Early and regular spraying important.",
            },
            "pre_harvest": {
                "chemical": "Propiconazole 25% EC (1ml/L); PHI 14 days",
                "fungicide": "Tebuconazole 25.9% EC (1ml/L); PHI 14 days",
                "organic": "Copper-based fungicide 0.3%",
                "dose": "400 L/ha",
                "frequency": "Once at 60-70 DAS if needed",
                "notes": "Late-season sprays protect last flush of leaves for pod filling.",
            },
        },
        "Rust": {
            "sowing": {
                "chemical": "Thiram 75% WS (3g/kg seed) + Carbendazim (2g/kg seed)",
                "fungicide": "Metalaxyl 35% WS (6g/kg seed)",
                "organic": "Trichoderma harzianum (4g/kg seed)",
                "dose": "Seed treatment",
                "frequency": "Once",
                "notes": "Groundnut rust (Puccinia arachidis) — select resistant varieties.",
            },
            "mid_season": {
                "chemical": "Mancozeb 75% WP (2g/L) + Chlorothalonil 75% WP (2g/L)",
                "fungicide": "Propiconazole 25% EC (1ml/L) OR Triadimefon 25% WP (1g/L)",
                "organic": "Sulfur 80% WDG (3g/L) — highly effective",
                "dose": "500 L/ha",
                "frequency": "3 sprays at 10-day intervals from 40 DAS",
                "notes": "Rust appears orange-yellow on undersurface. Combination sprays work best.",
            },
            "pre_harvest": {
                "chemical": "Propiconazole 25% EC (1ml/L); PHI 14 days",
                "fungicide": "Tebuconazole 25.9% EC (1ml/L); PHI 14 days",
                "organic": "Wettable sulfur 3g/L",
                "dose": "400 L/ha",
                "frequency": "Once at 60-70 DAS",
                "notes": "Protect leaves for pod filling. Rust causes premature defoliation.",
            },
        },
        "Collar Rot": {
            "sowing": {
                "chemical": "Thiram 75% WS (3g/kg seed) + Carbendazim (2g/kg seed)",
                "fungicide": "Captan 75% WS (3g/kg seed) + Metalaxyl",
                "organic": "Trichoderma harzianum (250g/acre in FYM, soil incorporation)",
                "dose": "Seed treatment + soil treatment",
                "frequency": "Once at sowing + pre-sowing soil treatment",
                "notes": "Collar rot (Aspergillus niger) — worst in dry, sandy soils.",
            },
            "mid_season": {
                "chemical": "Carbendazim 50% WP (1g/L) soil drench at stem base",
                "fungicide": "Propiconazole 25% EC (1ml/L) soil drench",
                "organic": "Pseudomonas fluorescens (10g/L) drenching",
                "dose": "250ml drench per plant at stem base",
                "frequency": "2 drenches at 10-day intervals",
                "notes": "Maintain soil moisture. Avoid high soil temperature in early season.",
            },
            "pre_harvest": {
                "chemical": "No effective late control",
                "fungicide": "None",
                "organic": "None",
                "dose": "N/A",
                "frequency": "N/A",
                "notes": "Prevention is the only strategy. Focus on seed and soil treatment.",
            },
        },
    },
    "Chilli": {
        "Anthracnose": {
            "sowing": {
                "chemical": "Thiram 75% WS (3g/kg seed) + Carbendazim (2g/kg seed)",
                "fungicide": "Iprodione 50% WP (2g/kg seed)",
                "organic": "Hot water treatment (50°C for 30 min) + Trichoderma coat",
                "dose": "Seed treatment",
                "frequency": "Once",
                "notes": "Use disease-free certified seed. 3-yr crop rotation with non-Solanaceae.",
            },
            "mid_season": {
                "chemical": "Mancozeb 75% WP (2g/L) OR Chlorothalonil 75% WP (2g/L)",
                "fungicide": "Difenoconazole 25% EC (0.05%) OR Propiconazole 25% EC (1ml/L)",
                "organic": "Copper oxychloride 3g/L + Neem oil 0.5%",
                "dose": "500-600 L/ha",
                "frequency": "Every 7-10 days during fruiting stage",
                "notes": "Anthracnose is fruit-stage disease. Spray coverage on fruits essential.",
            },
            "pre_harvest": {
                "chemical": "Azoxystrobin 23% SC (0.5ml/L); PHI 3 days",
                "fungicide": "Difenoconazole 25% EC (0.05%); PHI 7 days",
                "organic": "Copper oxychloride 3g/L; PHI 7 days",
                "dose": "400-500 L/ha",
                "frequency": "Every 7 days until last spray 3-7 days before harvest",
                "notes": "Frequent harvesting of ripe fruits reduces anthracnose spread.",
            },
        },
        "Leaf Curl Virus": {
            "sowing": {
                "chemical": "Imidacloprid 70% WS (5g/kg seed) — for thrips/mite vector control",
                "fungicide": "No fungicide — viral disease",
                "organic": "Yellow sticky traps + Neem oil spray (3ml/L) on seedlings",
                "dose": "Insecticide seed coat + traps at 20/ha",
                "frequency": "Once at sowing; monitoring weekly",
                "notes": "Chilli Leaf Curl is transmitted by thrips and mites. Use tolerant varieties.",
            },
            "mid_season": {
                "chemical": "Spiromesifen 22.9% SC (0.75ml/L) OR Abamectin 1.8% EC (0.5ml/L) for mites/thrips",
                "fungicide": "None. No antiviral chemical registered.",
                "organic": "Neem oil 5ml/L + Verticillium lecanii (bioagent) spray for thrips",
                "dose": "500 L/ha",
                "frequency": "Every 7 days for vector control",
                "notes": "Remove infected plants. Silicon spray (1g/L) reduces vector feeding.",
            },
            "pre_harvest": {
                "chemical": "Pyriproxyfen 10% EC (1ml/L) for thrips/whitefly; PHI 7 days",
                "fungicide": "None",
                "organic": "Soap + Neem oil solution",
                "dose": "400 L/ha",
                "frequency": "As needed for vector pressure",
                "notes": "Infected plants produce deformed, low-quality fruit.",
            },
        },
        "Downy Mildew": {
            "sowing": {
                "chemical": "Metalaxyl 35% WS (6g/kg seed)",
                "fungicide": "Ridomil Gold (Metalaxyl-M) seed treatment",
                "organic": "Trichoderma viride (4g/kg seed)",
                "dose": "Seed treatment",
                "frequency": "Once",
                "notes": "Cool, moist conditions favor Downy Mildew. Proper nursery ventilation key.",
            },
            "mid_season": {
                "chemical": "Metalaxyl + Mancozeb (Ridomil MZ 2.5g/L) OR Fosetyl-Al 80% WP (3g/L)",
                "fungicide": "Dimethomorph 50% WG (1g/L) alternating with Metalaxyl + Mancozeb",
                "organic": "Copper hydroxide 77% WP (2g/L)",
                "dose": "500 L/ha",
                "frequency": "Every 7-10 days during cool weather",
                "notes": "Spray undersides of leaves thoroughly. Downy mildew develops there.",
            },
            "pre_harvest": {
                "chemical": "Copper oxychloride 50% WP (3g/L); PHI 7 days",
                "fungicide": "Fosetyl-Al 80% WP (3g/L); PHI 14 days",
                "organic": "Bordeaux mixture 1%",
                "dose": "400 L/ha",
                "frequency": "Once if needed",
                "notes": "Improve field drainage. Avoid over-irrigation.",
            },
        },
    },
}

# Quick lookup by disease name across all crops
DISEASE_TO_CROPS: dict[str, list[str]] = {}
for crop_name, crop_data in MEDICINE_DB.items():
    for disease_name in crop_data.keys():
        if disease_name not in DISEASE_TO_CROPS:
            DISEASE_TO_CROPS[disease_name] = []
        DISEASE_TO_CROPS[disease_name].append(crop_name)


def get_treatment(crop: str, disease: str, stage: str = "mid_season") -> dict | None:
    """
    Get treatment recommendation for a crop/disease combination.
    stage: 'sowing' | 'mid_season' | 'pre_harvest'
    Returns the treatment dict or None if not found.
    """
    crop_key = crop.strip().title()
    disease_key = disease.strip().title()

    crop_data = MEDICINE_DB.get(crop_key)
    if not crop_data:
        # Fuzzy match crop
        for k in MEDICINE_DB:
            if k.lower() == crop.strip().lower():
                crop_data = MEDICINE_DB[k]
                break

    if not crop_data:
        return None

    disease_data = crop_data.get(disease_key)
    if not disease_data:
        # Try case-insensitive match
        for k in crop_data:
            if k.lower() == disease.strip().lower():
                disease_data = crop_data[k]
                break

    if not disease_data:
        return None

    return disease_data.get(stage)


def get_all_treatments_for_disease(crop: str, disease: str) -> dict | None:
    """Return all stage treatments for a crop+disease pair."""
    crop_key = crop.strip().title()
    disease_key = disease.strip().title()

    crop_data = MEDICINE_DB.get(crop_key)
    if not crop_data:
        for k in MEDICINE_DB:
            if k.lower() == crop.strip().lower():
                crop_data = MEDICINE_DB[k]
                break
    if not crop_data:
        return None

    disease_data = crop_data.get(disease_key)
    if not disease_data:
        for k in crop_data:
            if k.lower() == disease.strip().lower():
                disease_data = crop_data[k]
                break

    return disease_data


def list_diseases_for_crop(crop: str) -> list[str]:
    """Return list of diseases for a given crop."""
    crop_key = crop.strip().title()
    crop_data = MEDICINE_DB.get(crop_key, {})
    if not crop_data:
        for k in MEDICINE_DB:
            if k.lower() == crop.strip().lower():
                crop_data = MEDICINE_DB[k]
                break
    return list(crop_data.keys())
