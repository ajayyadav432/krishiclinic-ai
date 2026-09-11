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
C_BORDER = RGBColor(226, 232, 240)

def replace_picture_shape(slide, shape_name, new_image_path, left, top, width, height):
    target = None
    for s in slide.shapes:
        if s.name == shape_name and s.shape_type == 13:
            target = s
            break
    if target is not None:
        sp = target._element
        sp.getparent().remove(sp)
    return slide.shapes.add_picture(new_image_path, left, top, width=width, height=height)

def format_card_bullets(shape, title_text, bullets):
    tf = shape.text_frame
    tf.clear()
    tf.word_wrap = True
    tf.margin_left = Inches(0.25)
    tf.margin_right = Inches(0.25)
    tf.margin_top = Inches(0.22)
    tf.margin_bottom = Inches(0.22)
    
    # Title
    p0 = tf.paragraphs[0]
    p0.text = title_text
    p0.font.size = Pt(15.5)
    p0.font.bold = True
    p0.font.color.rgb = C_DARK_GREEN
    p0.space_after = Pt(12)
    
    for b_title, b_desc in bullets:
        p = tf.add_paragraph()
        p.text = f"{b_title}: "
        p.font.size = Pt(12.0)
        p.font.bold = True
        p.font.color.rgb = C_NAVY
        p.space_before = Pt(8)
        p.space_after = Pt(2)
        
        run = p.add_run()
        run.text = b_desc
        run.font.bold = False
        run.font.size = Pt(10.5)
        run.font.color.rgb = C_MED_GRAY

# ==========================================
# SLIDE 2: Solution Title
# ==========================================
slide2 = prs.slides[1]
# Update card text to ensure ₹ symbols and perfect spacing
for s in slide2.shapes:
    if s.name == "Rounded Rectangle 16":
        format_card_bullets(
            s,
            "THE PROBLEM & OUR SOLUTION",
            [
                ("The Ground Reality", "Over 60% of Indian farmers have no access to plant doctors and rely entirely on pesticide shopkeepers for advice. (Source: NSSO 77th Round)."),
                ("The National Crisis", "India loses over ₹90,000 Crores annually to misdiagnosed diseases and ineffective chemical sprays. (Source: ICAR & ASSOCHAM)."),
                ("The KrishiClinic Solution", "A 1-tap mobile app giving 2-second AI diagnosis, certified Agronomist verification, and exact medicine dosage to prevent catastrophic losses.")
            ]
        )
    elif s.name == "Rounded Rectangle 15":
        tf = s.text_frame
        tf.clear()
        p0 = tf.paragraphs[0]
        p0.text = "Ramesh Ji's Tomato Field Loss"
        p0.font.size = Pt(11.5)
        p0.font.bold = True
        p0.font.color.rgb = RGBColor(155, 44, 44)
        p1 = tf.add_paragraph()
        p1.text = "Lost ₹80,000 in 72 hours when a shopkeeper sold him the wrong ₹2,500 spray."
        p1.font.size = Pt(10.0)
        p1.font.color.rgb = RGBColor(116, 42, 42)

# ==========================================
# SLIDE 3: Technical Approach
# ==========================================
slide3 = prs.slides[2]
replace_picture_shape(
    slide3, "Picture 10",
    os.path.join(ASSETS_DIR, "slide3_tech_clean.png"),
    Inches(0.80), Inches(2.02), Inches(6.80), Inches(4.88)
)
for s in slide3.shapes:
    if s.name == "Rounded Rectangle 11":
        format_card_bullets(
            s,
            "CORE ARCHITECTURE",
            [
                ("Dual-Engine Vision AI", "Combines high-speed local EfficientNetV2-S for edge devices with Gemini Vision cloud fallback for complex leaves."),
                ("Agronomist Safety Gate", "Predictions with confidence ≥ 70% auto-approve; low-confidence cases route to accredited agronomists."),
                ("100% Offline Edge Mode", "Model weights bundled on device for zero-network fields, syncing metadata when back in coverage."),
                ("Outbreak Radar (25 km)", "Aggregates anonymized cases to flag geospatial outbreak clusters and alert neighboring farms.")
            ]
        )

# ==========================================
# SLIDE 4: UX & Design
# ==========================================
slide4 = prs.slides[3]
for s in slide4.shapes:
    if s.name == "Rounded Rectangle 12":
        format_card_bullets(
            s,
            "SIMPLE 3-STEP FARMER JOURNEY",
            [
                ("Step 1: Snap or Speak", "Farmer taps one big button or speaks query in their native mother tongue (Hindi, Marathi, Telugu, Punjabi, English)."),
                ("Step 2: Instant 2-Second Severity", "Clear color-coded badges (Green = Low, Orange = Moderate, Red = Severe) eliminate confusing scientific jargon."),
                ("Step 3: Actionable Cure & Audio Readout", "Gives exact active chemical dosage (e.g. 2 ml/liter), organic alternatives, and voice player reading the cure aloud."),
                ("Agronomist Web Portal", "Certified experts verify edge cases with 1-click approval and digital certification stamp.")
            ]
        )
    elif s.name == "Rounded Rectangle 11":
        tf = s.text_frame
        tf.clear()
        p0 = tf.paragraphs[0]
        p0.text = "In-Field Rural Usability"
        p0.font.size = Pt(11.5)
        p0.font.bold = True
        p0.font.color.rgb = RGBColor(34, 84, 61)
        p1 = tf.add_paragraph()
        p1.text = "1-Tap Camera & Native Voice Guidance in Hindi, Marathi, Telugu & 8+ Indian Languages."
        p1.font.size = Pt(10.0)
        p1.font.color.rgb = RGBColor(47, 133, 90)

# ==========================================
# SLIDE 5: Feasibility & Viability
# ==========================================
slide5 = prs.slides[4]
replace_picture_shape(
    slide5, "Picture 11",
    os.path.join(ASSETS_DIR, "slide5_feasibility_clean.png"),
    Inches(0.80), Inches(2.02), Inches(6.80), Inches(4.88)
)
for s in slide5.shapes:
    if s.name == "Rounded Rectangle 12":
        format_card_bullets(
            s,
            "REAL-WORLD VIABILITY",
            [
                ("Low-Cost Android Support", "Tested and optimized for entry-level ₹5,000 smartphones (Android 8.0+) with memory usage under 60 MB RAM."),
                ("True Field Independence", "Edge model works 100% offline with zero cellular coverage in remote agricultural fields."),
                ("Unit Cost Under ₹0.15", "Lightweight quantized architecture avoids expensive API calls, keeping diagnosis 100% free for farmers."),
                ("Expert Network Incentives", "Micro-incentives for agricultural college graduates to review and stamp cases in under 1 minute.")
            ]
        )

# ==========================================
# SLIDE 6: Impact & Benefits
# ==========================================
slide6 = prs.slides[5]
replace_picture_shape(
    slide6, "Picture 12",
    os.path.join(ASSETS_DIR, "slide6_impact_clean.png"),
    Inches(5.40), Inches(2.02), Inches(7.10), Inches(4.88)
)
for s in slide6.shapes:
    if s.name == "Rounded Rectangle 11":
        tf = s.text_frame
        tf.clear()
        p0 = tf.paragraphs[0]
        p0.text = "Empowered, Prosperous Farmer"
        p0.font.size = Pt(11.5)
        p0.font.bold = True
        p0.font.color.rgb = RGBColor(34, 84, 61)
        p1 = tf.add_paragraph()
        p1.text = "Saves ₹25,000 to ₹30,000 per acre in prevented crop loss and wasted chemicals."
        p1.font.size = Pt(10.0)
        p1.font.color.rgb = RGBColor(47, 133, 90)

# ==========================================
# SLIDE 7: Business Model & Sustainability
# ==========================================
slide7 = prs.slides[6]
replace_picture_shape(
    slide7, "Picture 10",
    os.path.join(ASSETS_DIR, "slide7_business_clean.png"),
    Inches(0.80), Inches(2.02), Inches(6.80), Inches(4.88)
)
for s in slide7.shapes:
    if s.name == "Rounded Rectangle 11":
        format_card_bullets(
            s,
            "FINANCIAL SUSTAINABILITY",
            [
                ("100% Free for Farmers", "No subscription or diagnostic fees for smallholders, ensuring universal adoption across rural India."),
                ("Verified Agri-Inputs (B2B)", "Certified bio-pesticide and seed manufacturers pay referral margins when farmers purchase vetted products."),
                ("Crop Insurers (B2B)", "PM Fasal Bima underwriters license anonymized field disease loss data for fast and objective claim settlements."),
                ("State Agriculture Boards (B2G)", "Government departments and KVKs subscribe to regional outbreak maps for epidemic containment.")
            ]
        )

# ==========================================
# SLIDE 8: Research and References
# ==========================================
slide8 = prs.slides[7]
replace_picture_shape(
    slide8, "Picture 10",
    os.path.join(ASSETS_DIR, "slide8_references_clean.png"),
    Inches(0.80), Inches(2.02), Inches(11.73), Inches(4.88)
)

prs.save(PPT_PATH)
print("PPTX successfully updated!")
