import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE

PPT_PATH = "/home/ajay/MUJ_Hackathon/presentation/KrishiClinic_AI_Pitch_Deck.pptx"
ASSETS_DIR = "/home/ajay/MUJ_Hackathon/presentation/assets"

prs = Presentation(PPT_PATH)

# Common styling palette
C_NAVY = RGBColor(26, 32, 44)
C_DARK_GREEN = RGBColor(34, 84, 61)
C_MED_GRAY = RGBColor(74, 85, 104)
C_LIGHT_BG = RGBColor(247, 250, 252)
C_BORDER = RGBColor(203, 213, 224) # sleek slate border
C_WHITE = RGBColor(255, 255, 255)

# Standard layout geometry across all slides 2-8
IMG_LEFT = Inches(0.80)
IMG_TOP = Inches(2.02)
IMG_W = Inches(6.80)
IMG_H = Inches(4.88)

CARD_LEFT = Inches(7.80)
CARD_TOP = Inches(2.02)
CARD_W = Inches(4.73)
CARD_H = Inches(4.88)

# ==========================================
# SLIDE 1: COVER SLIDE
# ==========================================
slide1 = prs.slides[0]
for shape in slide1.shapes:
    if shape.has_text_frame and shape.name == "Subtitle 2":
        shape.top = Inches(4.70)
        shape.height = Inches(2.40)
        tf = shape.text_frame
        tf.clear()
        
        p0 = tf.paragraphs[0]
        p0.text = "Team Name: Codies"
        p0.font.size = Pt(25)
        p0.font.bold = True
        p0.font.color.rgb = RGBColor(255, 255, 255)
        p0.alignment = PP_ALIGN.CENTER
        p0.space_after = Pt(6)
        
        p1 = tf.add_paragraph()
        p1.text = "Team ID: [Registration ID]"
        p1.font.size = Pt(20)
        p1.font.color.rgb = RGBColor(220, 220, 245)
        p1.alignment = PP_ALIGN.CENTER
        p1.space_after = Pt(8)
        
        p2 = tf.add_paragraph()
        p2.text = "Problem Statement: PS #1 - AI Crop Disease Detection"
        p2.font.size = Pt(23)
        p2.font.bold = True
        p2.font.color.rgb = RGBColor(255, 225, 100) # gold
        p2.alignment = PP_ALIGN.CENTER
        p2.space_after = Pt(6)
        
        p3 = tf.add_paragraph()
        p3.text = "Theme: AgriTech"
        p3.font.size = Pt(20)
        p3.font.color.rgb = RGBColor(200, 245, 200)
        p3.alignment = PP_ALIGN.CENTER
        p3.space_after = Pt(8)
        
        p4 = tf.add_paragraph()
        p4.text = "Project: KrishiClinic AI - Intelligent Crop Diagnosis & Outbreak Radar"
        p4.font.size = Pt(22)
        p4.font.bold = True
        p4.font.color.rgb = RGBColor(255, 255, 255)
        p4.alignment = PP_ALIGN.CENTER

def setup_clean_slide(slide, title_text, subtitle_text, image_filename, card_title, bullets):
    # 1. Clean existing content shapes (keep title & subtitle textbox)
    to_remove = []
    for s in slide.shapes:
        # Keep title shape
        if s.name == "Subtitle 2":
            continue
        # Keep subtitle textbox if top < 2.0 inches
        if s.has_text_frame and s.top < Inches(1.9):
            continue
        # Everything else in content area gets cleaned up
        to_remove.append(s)
        
    for s in to_remove:
        sp = s._element
        sp.getparent().remove(sp)
        
    # 2. Update Title
    for s in slide.shapes:
        if s.name == "Subtitle 2":
            s.text_frame.word_wrap = True
            p = s.text_frame.paragraphs[0]
            p.text = title_text
            p.font.size = Pt(26)
            p.font.bold = True
            p.font.color.rgb = C_NAVY
            p.alignment = PP_ALIGN.CENTER
            
    # 3. Update or Add Subtitle
    sub_found = False
    for s in slide.shapes:
        if s.has_text_frame and s.name != "Subtitle 2" and s.top < Inches(1.9):
            sub_found = True
            s.text_frame.word_wrap = True
            p = s.text_frame.paragraphs[0]
            p.text = subtitle_text
            p.font.size = Pt(15.5)
            p.font.bold = True
            p.font.color.rgb = C_DARK_GREEN
            p.alignment = PP_ALIGN.CENTER
            
    if not sub_found:
        tb = slide.shapes.add_textbox(Inches(0.80), Inches(1.50), Inches(11.73), Inches(0.42))
        p = tb.text_frame.paragraphs[0]
        p.text = subtitle_text
        p.font.size = Pt(15.5)
        p.font.bold = True
        p.font.color.rgb = C_DARK_GREEN
        p.alignment = PP_ALIGN.CENTER

    # 4. Add Visual Picture on Left
    img_path = os.path.join(ASSETS_DIR, image_filename)
    slide.shapes.add_picture(img_path, IMG_LEFT, IMG_TOP, width=IMG_W, height=IMG_H)
    
    # 5. Add Single Clean Card on Right
    card_shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, CARD_LEFT, CARD_TOP, CARD_W, CARD_H)
    card_shape.fill.solid()
    card_shape.fill.fore_color.rgb = C_LIGHT_BG
    card_shape.line.color.rgb = C_BORDER
    card_shape.line.width = Pt(1.5)
    
    tf = card_shape.text_frame
    tf.clear()
    tf.word_wrap = True
    tf.margin_left = Inches(0.28)
    tf.margin_right = Inches(0.28)
    tf.margin_top = Inches(0.28)
    tf.margin_bottom = Inches(0.28)
    
    # Card Title
    p0 = tf.paragraphs[0]
    p0.text = card_title
    p0.font.size = Pt(17.5)
    p0.font.bold = True
    p0.font.color.rgb = C_DARK_GREEN
    p0.space_after = Pt(14)
    
    # 3 High-Impact Bullets
    for b_title, b_desc in bullets:
        p = tf.add_paragraph()
        p.text = f"{b_title}: "
        p.font.size = Pt(14)
        p.font.bold = True
        p.font.color.rgb = C_NAVY
        p.space_before = Pt(12)
        p.space_after = Pt(4)
        
        run = p.add_run()
        run.text = b_desc
        run.font.bold = False
        run.font.size = Pt(12.5)
        run.font.color.rgb = C_MED_GRAY

# ==========================================
# SLIDE 2: Solution Title
# ==========================================
setup_clean_slide(
    slide=prs.slides[1],
    title_text="IDEA / SOLUTION TITLE: KRISHICLINIC AI",
    subtitle_text="Empowering Smallholder Farmers with Doctor-Verified AI Crop Pathology",
    image_filename="slide2_problem_clean.png",
    card_title="KEY TAKEAWAYS",
    bullets=[
        ("The Rural Crisis", "60%+ of Indian farmers lack agronomist access, relying solely on pesticide shopkeeper quotas."),
        ("National Damage", "India loses over ₹90,000 Crores every year to misdiagnosed diseases & ineffective sprays."),
        ("The KrishiClinic Cure", "2-second on-device AI diagnosis backed by certified doctor verification & exact remedies.")
    ]
)

# ==========================================
# SLIDE 3: Technical Approach
# ==========================================
setup_clean_slide(
    slide=prs.slides[2],
    title_text="TECHNICAL APPROACH",
    subtitle_text="Production-Grade Dual-Engine Vision Pipeline with Offline Rural Resilience",
    image_filename="slide3_tech_clean.png",
    card_title="ARCHITECTURE PILLARS",
    bullets=[
        ("Dual-Engine AI", "Local EfficientNetV2-S on edge + Gemini Vision cloud fallback for complex multi-disease leaves."),
        ("Doctor Safety Gate", "Confidence ≥ 70% auto-approves; rare cases route to accredited agronomists for review."),
        ("25km Outbreak Radar", "Geospatial DBSCAN clustering flags regional pathogen hotspots to stop village epidemics.")
    ]
)

# ==========================================
# SLIDE 4: UX & Design
# ==========================================
setup_clean_slide(
    slide=prs.slides[3],
    title_text="USER EXPERIENCE & DESIGN",
    subtitle_text="Farmer-Centric Usability: Voice Navigation & Zero-Literacy Barriers",
    image_filename="slide4_ux_clean.png",
    card_title="FARMER JOURNEY",
    bullets=[
        ("Voice-First Design", "Farmers can speak queries in Hindi, Marathi, Telugu, Punjabi, Tamil & English with audio cures."),
        ("3-Tap Simplicity", "Snap photo → View color-coded severity (Green/Orange/Red) → Listen to spoken medicine dosage."),
        ("Agronomist Portal", "Fast web dashboard with 1-click case approval, dosage adjustments, and digital certification.")
    ]
)

# ==========================================
# SLIDE 5: Feasibility & Viability
# ==========================================
setup_clean_slide(
    slide=prs.slides[4],
    title_text="FEASIBILITY AND VIABILITY",
    subtitle_text="Low-Cost Engineering Built for Entry-Level Devices & Remote Farms",
    image_filename="slide5_feasibility_clean.png",
    card_title="FEASIBILITY HIGHLIGHTS",
    bullets=[
        ("Runs on ₹5,000 Phones", "Optimized memory footprint under 60 MB RAM for Android 8.0+ entry smartphones."),
        ("100% Offline Diagnosis", "Operates entirely in remote farm fields without cellular network connectivity."),
        ("Under ₹0.15 Unit Cost", "Edge AI compute offloads servers, ensuring 100% free access for marginal farmers.")
    ]
)

# ==========================================
# SLIDE 6: Impact & Benefits
# ==========================================
setup_clean_slide(
    slide=prs.slides[5],
    title_text="IMPACT AND BENEFITS",
    subtitle_text="Protecting Livelihoods, Restoring Soil Health & Preventing Epidemics",
    image_filename="slide6_impact_clean.png",
    card_title="MEASURED IMPACT",
    bullets=[
        ("70% Cost Reduction", "Saves ₹25,000 - ₹30,000 per acre by stopping crop loss and unnecessary pesticide purchases."),
        ("40% Less Toxic Spray", "Precision active salt ratios and verified organic remedies restore long-term soil biology."),
        ("2-Sec Rapid Containment", "Cuts diagnostic delay from 72 hours of shopkeeper guesswork down to 2 seconds.")
    ]
)

# ==========================================
# SLIDE 7: Business Model & Sustainability
# ==========================================
setup_clean_slide(
    slide=prs.slides[6],
    title_text="BUSINESS MODEL & SUSTAINABILITY",
    subtitle_text="100% Free for Smallholder Farmers, Sustained by Verified Institutional Partners",
    image_filename="slide7_business_clean.png",
    card_title="REVENUE FLYWHEEL",
    bullets=[
        ("Free for Marginal Farmers", "Zero fees for diagnosis, audio advisories, and outbreak alerts, removing all financial barriers."),
        ("B2B Input Partners", "Certified bio-pesticide and seed suppliers pay referral margins for doctor-verified recommendations."),
        ("B2B/B2G Analytics", "Crop insurers & State Agri departments license real-time epidemiology data for risk management.")
    ]
)

# ==========================================
# SLIDE 8: Research and References
# ==========================================
setup_clean_slide(
    slide=prs.slides[7],
    title_text="RESEARCH AND REFERENCES",
    subtitle_text="Grounded in Scientific Literature, Government Studies & Field Benchmarks",
    image_filename="slide8_references_clean.png",
    card_title="KEY CITATIONS",
    bullets=[
        ("ICAR Economic Survey", "Documents ₹90,000+ Crores annual crop loss to misdiagnosed plant pathogens across India."),
        ("NSSO 77th Round", "Confirms 60%+ Indian farmers depend solely on local chemical shopkeepers for advice."),
        ("PlantVillage Benchmarks", "Validates 96%+ mobile accuracy using lightweight quantized vision architectures.")
    ]
)

prs.save(PPT_PATH)
print("Updated PowerPoint presentation saved successfully at:", PPT_PATH)
