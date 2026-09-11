"""Comprehensive multilingual translation dictionaries for agricultural advisory texts.

Covers crops, diseases, severity, statuses, advisories, and dynamic reasons
across Hindi (hi), Telugu (te), Marathi (mr), and Spanish (es).
"""

import re
from typing import Optional

CROP_TRANSLATIONS: dict[str, dict[str, str]] = {
    "wheat": {"hi": "गेहूं", "te": "గోధుమ", "mr": "गहू", "es": "Trigo"},
    "rice": {"hi": "चावल", "te": "వరి", "mr": "तांदूळ", "es": "Arroz"},
    "tomato": {"hi": "टमाटर", "te": "టమోటా", "mr": "टोमॅटो", "es": "Tomate"},
    "corn": {"hi": "मक्का", "te": "మొక్కజొన్న", "mr": "मका", "es": "Maíz"},
    "potato": {"hi": "आलू", "te": "బంగాళాదుంప", "mr": "बटाटा", "es": "Papa"},
    "cotton": {"hi": "कपास", "te": "పత్తి", "mr": "कापूस", "es": "Algodón"},
    "sugarcane": {"hi": "गन्ना", "te": "చెరకు", "mr": "ऊस", "es": "Caña de azúcar"},
    "soybean": {"hi": "सोयाबीन", "te": "సోయాబీన్", "mr": "सोयाबीन", "es": "Soja"},
    "mustard": {"hi": "सरसों", "te": "ఆవాలు", "mr": "मोहरी", "es": "Mostaza"},
    "groundnut": {"hi": "मूंगफली", "te": "వేరుశనగ", "mr": "भुईमूग", "es": "Maní"},
    "chilli": {"hi": "मिर्च", "te": "మిరపకాయ", "mr": "मिरची", "es": "Chile"},
}

SEVERITY_TRANSLATIONS: dict[str, dict[str, str]] = {
    "high": {"hi": "उच्च", "te": "ఎక్కువ", "mr": "जास्त", "es": "Alto"},
    "medium": {"hi": "मध्यम", "te": "మధ్యస్థం", "mr": "मध्यम", "es": "Medio"},
    "low": {"hi": "निम्न", "te": "తక్కువ", "mr": "कमी", "es": "Bajo"},
}

DISEASE_TRANSLATIONS: dict[str, dict[str, str]] = {
    "yellow rust": {
        "hi": "पीला रतुआ (Yellow Rust)",
        "te": "పసుపు కుంకుమ తెగులు (Yellow Rust)",
        "mr": "तांबेरा रोग (Yellow Rust)",
        "es": "Roya amarilla (Yellow Rust)",
    },
    "leaf blight": {
        "hi": "पत्ता झुलसा (Leaf Blight)",
        "te": "ఆకు ఎండు తెగులు (Leaf Blight)",
        "mr": "पानांवरील करपा (Leaf Blight)",
        "es": "Tizón foliar (Leaf Blight)",
    },
    "stem rust": {
        "hi": "तना रतुआ (Stem Rust)",
        "te": "కాండం కుంకుమ తెగులు (Stem Rust)",
        "mr": "खोडावरील तांबेरा (Stem Rust)",
        "es": "Roya del tallo (Stem Rust)",
    },
    "powdery mildew": {
        "hi": "चूर्णिल आसिता (Powdery Mildew)",
        "te": "బూడిద తెగులు (Powdery Mildew)",
        "mr": "भुरी रोग (Powdery Mildew)",
        "es": "Oídio (Powdery Mildew)",
    },
    "karnal bunt": {
        "hi": "करनाल बंट (Karnal Bunt)",
        "te": "కర్నాల్ బంట్ (Karnal Bunt)",
        "mr": "कर्नाल बंट (Karnal Bunt)",
        "es": "Carbón parcial (Karnal Bunt)",
    },
    "blast": {
        "hi": "झोंका रोग (Blast)",
        "te": "అగ్గి తెగులు (Blast)",
        "mr": "करपा रोग (Blast)",
        "es": "Añublo (Blast)",
    },
    "brown spot": {
        "hi": "भूरा धब्बा (Brown Spot)",
        "te": "గోధుమ రంగు మచ్చ తెగులు (Brown Spot)",
        "mr": "तपकिरी ठिपके (Brown Spot)",
        "es": "Mancha marrón (Brown Spot)",
    },
    "bacterial leaf blight": {
        "hi": "जीवाणु झुलसा (Bacterial Leaf Blight)",
        "te": "బ్యాక్టీరియా ఆకు ఎండు తెగులు (Bacterial Leaf Blight)",
        "mr": "जिवाणूजन्य पानांवरील करपा (Bacterial Leaf Blight)",
        "es": "Tizón bacteriano de la hoja (Bacterial Leaf Blight)",
    },
    "sheath blight": {
        "hi": "शीथ ब्लाइट (Sheath Blight)",
        "te": "మట్ట కుళ్లు తెగులు (Sheath Blight)",
        "mr": "खोडावरील करपा (Sheath Blight)",
        "es": "Tizón de la vaina (Sheath Blight)",
    },
    "early blight": {
        "hi": "अगेती झुलसा (Early Blight)",
        "te": "ఆకు మచ్చ తెగులు (Early Blight)",
        "mr": "लवकर येणारा करपा (Early Blight)",
        "es": "Tizón temprano (Early Blight)",
    },
    "late blight": {
        "hi": "पछेती झुलसा (Late Blight)",
        "te": "మలిదశ ఆకుమచ్చ తెగులు (Late Blight)",
        "mr": "उशिरा येणारा करपा (Late Blight)",
        "es": "Tizón tardío (Late Blight)",
    },
    "fusarium wilt": {
        "hi": "फ्यूजेरियम म्लानि (Fusarium Wilt)",
        "te": "ఫ్యుసేరియం ఎండు తెగులు (Fusarium Wilt)",
        "mr": "फ्युजेरियम मर रोग (Fusarium Wilt)",
        "es": "Marchitez por Fusarium (Fusarium Wilt)",
    },
    "leaf curl virus": {
        "hi": "पर्ण कुंचन विषाणु (Leaf Curl Virus)",
        "te": "ఆకు ముడుత వైరస్ (Leaf Curl Virus)",
        "mr": "चुरडा-मुरडा रोग (Leaf Curl Virus)",
        "es": "Virus del enrollamiento de la hoja (Leaf Curl Virus)",
    },
    "northern leaf blight": {
        "hi": "उत्तरी पत्ता झुलसा (Northern Leaf Blight)",
        "te": "ఉత్తర ఆకు ఎండు తెగులు (Northern Leaf Blight)",
        "mr": "उत्तरी पानांवरील करपा (Northern Leaf Blight)",
        "es": "Tizón foliar del norte (Northern Leaf Blight)",
    },
    "gray leaf spot": {
        "hi": "सलेटी पत्ता धब्बा (Gray Leaf Spot)",
        "te": "బూడిద రంగు ఆకుమచ్చ తెగులు (Gray Leaf Spot)",
        "mr": "राखाडी पानांवरील ठिपके (Gray Leaf Spot)",
        "es": "Mancha foliar gris (Gray Leaf Spot)",
    },
    "common rust": {
        "hi": "सामान्य रतुआ (Common Rust)",
        "te": "సాధారణ కుంకుమ తెగులు (Common Rust)",
        "mr": "सामान्य तांबेरा (Common Rust)",
        "es": "Roya común (Common Rust)",
    },
    "stalk rot": {
        "hi": "तना सड़न (Stalk Rot)",
        "te": "కాండం కుళ్లు తెగులు (Stalk Rot)",
        "mr": "खोड कुजणे (Stalk Rot)",
        "es": "Pudrición del tallo (Stalk Rot)",
    },
    "common scab": {
        "hi": "सामान्य पपड़ी (Common Scab)",
        "te": "సాధారణ స్కాబ్ (Common Scab)",
        "mr": "खवले रोग (Common Scab)",
        "es": "Sarna común (Common Scab)",
    },
    "black scurf": {
        "hi": "काली रूसी (Black Scurf)",
        "te": "నల్ల పొలుసు తెగులు (Black Scurf)",
        "mr": "काळी खपली (Black Scurf)",
        "es": "Costra negra (Black Scurf)",
    },
    "bacterial blight": {
        "hi": "जीवाणु जनित झुलसा (Bacterial Blight)",
        "te": "బ్యాక్టీరియా ఎండు తెగులు (Bacterial Blight)",
        "mr": "जिवाणूजन्य करपा (Bacterial Blight)",
        "es": "Tizón bacteriano (Bacterial Blight)",
    },
    "cotton leaf curl virus": {
        "hi": "कपास पर्ण कुंचन विषाणु (Cotton Leaf Curl Virus)",
        "te": "పత్తి ఆకు ముడుత వైరస్ (Cotton Leaf Curl Virus)",
        "mr": "कापूस चुरडा-मुरडा विषाणू (Cotton Leaf Curl Virus)",
        "es": "Virus del rizado de la hoja del algodón (Cotton Leaf Curl Virus)",
    },
    "alternaria leaf spot": {
        "hi": "अल्टरनेरिया पत्ता धब्बा (Alternaria Leaf Spot)",
        "te": "ఆల్టర్నేరియా ఆకుమచ్చ తెగులు (Alternaria Leaf Spot)",
        "mr": "अल्टरनेरिया पानांवरील ठिपके (Alternaria Leaf Spot)",
        "es": "Mancha foliar por Alternaria (Alternaria Leaf Spot)",
    },
    "red rot": {
        "hi": "लाल सड़न रोग (Red Rot)",
        "te": "ఎర్ర కుళ్లు తెగులు (Red Rot)",
        "mr": "ऊस तांबेरा / लाल कुजव्या (Red Rot)",
        "es": "Pudrición roja (Red Rot)",
    },
    "smut": {
        "hi": "कंडुआ रोग (Smut)",
        "te": "కాటుక తెగులు (Smut)",
        "mr": "काजळी रोग (Smut)",
        "es": "Carbón (Smut)",
    },
    "grassy shoot disease": {
        "hi": "घासी प्ररोह रोग (Grassy Shoot)",
        "te": "గడ్డి పిలకల తెగులు (Grassy Shoot)",
        "mr": "गवती वाढ रोग (Grassy Shoot)",
        "es": "Enfermedad de los brotes herbáceos (Grassy Shoot)",
    },
    "rust": {
        "hi": "रतुआ रोग (Rust)",
        "te": "కుంకుమ తెగులు (Rust)",
        "mr": "तांबेरा (Rust)",
        "es": "Roya (Rust)",
    },
    "cercospora leaf blight": {
        "hi": "सर्कोस्पोरा पत्ता झुलसा (Cercospora Leaf Blight)",
        "te": "సెర్కోస్పోరా ఆకుమచ్చ తెగులు (Cercospora Leaf Blight)",
        "mr": "सर्कोस्पोरा पानांवरील करपा (Cercospora Leaf Blight)",
        "es": "Tizón foliar por Cercospora (Cercospora Leaf Blight)",
    },
    "charcoal rot": {
        "hi": "चारकोल सड़न (Charcoal Rot)",
        "te": "బొగ్గు కుళ్లు తెగులు (Charcoal Rot)",
        "mr": "चारकोल सड (Charcoal Rot)",
        "es": "Pudrición carbonosa (Charcoal Rot)",
    },
    "white rust": {
        "hi": "सफेद रतुआ (White Rust)",
        "te": "తెల్ల కుంకుమ తెగులు (White Rust)",
        "mr": "पांढरा तांबेरा (White Rust)",
        "es": "Roya blanca (White Rust)",
    },
    "alternaria blight": {
        "hi": "अल्टरनेरिया झुलसा (Alternaria Blight)",
        "te": "ఆల్టర్నేరియా బ్లైట్ (Alternaria Blight)",
        "mr": "अल्टरनेरिया करपा (Alternaria Blight)",
        "es": "Tizón por Alternaria (Alternaria Blight)",
    },
    "tikka disease": {
        "hi": "टिक्का रोग (Tikka Disease)",
        "te": "టిక్కా తెగులు (Tikka Disease)",
        "mr": "टिक्का रोग (Tikka Disease)",
        "es": "Enfermedad de Tikka (Tikka Disease)",
    },
    "collar rot": {
        "hi": "कॉलर सड़न (Collar Rot)",
        "te": "మొక్క మొదలు కుళ్లు (Collar Rot)",
        "mr": "कॉलर कुजव्या (Collar Rot)",
        "es": "Pudrición del cuello (Collar Rot)",
    },
    "anthracnose": {
        "hi": "एंथ्रेक्नोज (Anthracnose)",
        "te": "ఆంత్రాక్నోస్ (Anthracnose)",
        "mr": "अँथ्रॅक्नोज (Anthracnose)",
        "es": "Antracnosis (Anthracnose)",
    },
    "downy mildew": {
        "hi": "मृदुरोमिल आसिता (Downy Mildew)",
        "te": "డౌనీ బూజు తెగులు (Downy Mildew)",
        "mr": "केवडा रोग (Downy Mildew)",
        "es": "Mildiu velloso (Downy Mildew)",
    },
    "downey mildew": {
        "hi": "मृदुरोमिल आसिता (Downy Mildew)",
        "te": "డౌనీ బూజు తెగులు (Downy Mildew)",
        "mr": "केवडा रोग (Downy Mildew)",
        "es": "Mildiu velloso (Downy Mildew)",
    },
    "frogeye": {
        "hi": "मेंढक आंख पत्ता धब्बा (Frogeye Leaf Spot)",
        "te": "కప్ప కన్ను ఆకుమచ్చ తెగులు (Frogeye Leaf Spot)",
        "mr": "फ्रॉगआय पानांवरील ठिपके (Frogeye Leaf Spot)",
        "es": "Mancha ojo de rana (Frogeye Leaf Spot)",
    },
    "frogeye leaf spot": {
        "hi": "मेंढक आंख पत्ता धब्बा (Frogeye Leaf Spot)",
        "te": "కప్ప కన్ను ఆకుమచ్చ తెగులు (Frogeye Leaf Spot)",
        "mr": "फ्रॉगआय पानांवरील ठिपके (Frogeye Leaf Spot)",
        "es": "Mancha ojo de rana (Frogeye Leaf Spot)",
    },
    "potassium deficiency": {
        "hi": "पोटेशियम की कमी (Potassium Deficiency)",
        "te": "పొటాషియం లోపం (Potassium Deficiency)",
        "mr": "पोटॅशियमची कमतरता (Potassium Deficiency)",
        "es": "Deficiencia de potasio (Potassium Deficiency)",
    },
    "soybean rust": {
        "hi": "सोयाबीन रतुआ (Soybean Rust)",
        "te": "సోయాబీన్ కుంకుమ తెగులు (Soybean Rust)",
        "mr": "सोयाबीन तांबेरा (Soybean Rust)",
        "es": "Roya de la soja (Soybean Rust)",
    },
    "target spot": {
        "hi": "टारगेट स्पॉट (Target Spot)",
        "te": "టార్గెట్ స్పాట్ (Target Spot)",
        "mr": "टार्गेट स्पॉट (Target Spot)",
        "es": "Mancha diana (Target Spot)",
    },
    "healthy": {
        "hi": "स्वस्थ (Healthy)",
        "te": "ఆరోగ్యకరమైనది (Healthy)",
        "mr": "निरोगी (Healthy)",
        "es": "Saludable (Healthy)",
    },
}

STATUS_AND_UI_TRANSLATIONS: dict[str, dict[str, str]] = {
    "pending": {"hi": "लंबित", "te": "పెండింగ్", "mr": "प्रलंबित", "es": "PENDIENTE"},
    "pending_review": {"hi": "समीक्षा लंबित", "te": "సమీక్ష పెండింగ్", "mr": "पुनरावलोकन प्रलंबित", "es": "REVISIÓN PENDIENTE"},
    "reviewed": {"hi": "सत्यापित", "te": "ధృవీకరించబడింది", "mr": "सत्यापित", "es": "VERIFICADO"},
    "pending review": {"hi": "समीक्षा लंबित है", "te": "సమీక్ష పెండింగ్‌లో ఉంది", "mr": "पुनरावलोकन प्रलंबित", "es": "Revisión pendiente"},
    "verified": {"hi": "सत्यापित", "te": "ధృవీకరించబడింది", "mr": "सत्यापित", "es": "Verificado"},
    "pending agronomist review": {
        "hi": "कृषि विज्ञानी समीक्षा लंबित है",
        "te": "వ్యవసాయ నిపుణుల సమీక్ష పెండింగ్‌లో ఉంది",
        "mr": "कृषी तज्ज्ञांचे पुनरावलोकन प्रलंबित आहे",
        "es": "Revisión del agrónomo pendiente",
    },
    "pending review by our agricultural expert.": {
        "hi": "हमारे कृषि विशेषज्ञ द्वारा समीक्षा की प्रतीक्षा की जा रही है।",
        "te": "మా వ్యవసాయ నిపుణుల సమీక్ష కోసం వేచి ఉంది.",
        "mr": "आमच्या कृषी तज्ज्ञांच्या पुनरावलोकनाची प्रतीक्षा आहे.",
        "es": "Pendiente de revisión por nuestro experto agrícola.",
    },
    "our agricultural expert is currently reviewing this prediction. you will receive the advice once verified.": {
        "hi": "हमारे कृषि विशेषज्ञ वर्तमान में इस निदान की समीक्षा कर रहे हैं। पुष्टि के बाद आपको सलाह प्राप्त होगी।",
        "te": "మా వ్యవసాయ నిపుణులు ప్రస్తుతం ఈ అంచనాను సమీక్షిస్తున్నారు. ధృవీకరించిన తర్వాత మీకు సలహా అందుతుంది.",
        "mr": "आमचे कृषी तज्ज्ञ सध्या या अंदाजाचे पुनरावलोकन करत आहेत. पडताळणीनंतर तुम्हाला सल्ला मिळेल.",
        "es": "Nuestro experto agrícola está revisando actualmente esta predicción. Recibirá el asesoramiento una vez verificado.",
    },
    "our agronomist is currently reviewing this prediction. the diagnosis below is locked until verified.": {
        "hi": "हमारे कृषि विज्ञानी वर्तमान में इस निदान की समीक्षा कर रहे हैं। सत्यापन तक नीचे का विवरण सुरक्षित है।",
        "te": "మా వ్యవసాయ నిపుణులు ప్రస్తుతం ఈ అంచనాను సమీక్షిస్తున్నారు. ధృవీకరించబడే వరకు క్రింది రోగ నిర్ధారణ లాక్ చేయబడింది.",
        "mr": "आमचे कृषी तज्ज्ञ सध्या या अंदाजाचे पुनरावलोकन करत आहेत. पडताळणी होईपर्यंत खालील निदान सुरक्षित आहे.",
        "es": "Nuestro agrónomo está revisando actualmente esta predicción. El diagnóstico a continuación está bloqueado hasta su verificación.",
    },
    "ai is analyzing your crop image. results will appear shortly.": {
        "hi": "एआई आपकी फसल की तस्वीर का विश्लेषण कर रहा है। परिणाम शीघ्र ही उपलब्ध होंगे।",
        "te": "AI మీ పంట చిత్రాన్ని విశ్లేషిస్తోంది. ఫలితాలు త్వరలో కనిపిస్తాయి.",
        "mr": "AI आपल्या पिकाच्या प्रतिमेचे विश्लेषण करत आहे. निकाल लवकरच उपलब्ध होतील.",
        "es": "La IA está analizando la imagen de su cultivo. Los resultados aparecerán en breve.",
    },
    "the prediction you're looking for doesn't exist.": {
        "hi": "आप जिस पूर्वानुमान की तलाश कर रहे हैं वह मौजूद नहीं है।",
        "te": "మీరు వెతుకుతున్న అంచనా ఫలితం అందుబాటులో లేదు.",
        "mr": "आपण शोधत असलेली नोंद अस्तित्वात नाही.",
        "es": "La predicción que busca no existe.",
    },
    "prediction not found": {
        "hi": "पूर्वानुमान नहीं मिला",
        "te": "అంచనా కనుగొనబడలేదు",
        "mr": "निदान सापडले नाही",
        "es": "Predicción no encontrada",
    },
    "outbreak radar": {
        "hi": "प्रकोप रडार (Outbreak Radar)",
        "te": "తెగుళ్ల రాడార్ (Outbreak Radar)",
        "mr": "रोग प्रादुर्भाव रडार (Outbreak Radar)",
        "es": "Radar de Brotes (Outbreak Radar)",
    },
    "active disease clusters": {
        "hi": "सक्रिय रोग क्लस्टर",
        "te": "క్రియాశీల తెగులు క్లస్టర్లు",
        "mr": "सक्रिय रोग क्लस्टर",
        "es": "Grupos activos de enfermedades",
    },
    "high risk areas": {
        "hi": "उच्च जोखिम वाले क्षेत्र",
        "te": "అధిక ప్రమాద ప్రాంతాలు",
        "mr": "अति धोक्याचे क्षेत्र",
        "es": "Áreas de alto riesgo",
    },
    "monitored field cases": {
        "hi": "निगरानी किए गए मामले",
        "te": "పర్యవేక్షించబడుతున్న కేసులు",
        "mr": "निरीक्षणातील प्रकरणे",
        "es": "Casos de campo monitoreados",
    },
    "early warning protocol": {
        "hi": "प्रारंभिक चेतावनी प्रोटोकॉल",
        "te": "ముందస్తు హెచ్చరిక ప్రోటోకాల్",
        "mr": "पूर्व चेतावणी प्रोटोकॉल",
        "es": "Protocolo de alerta temprana",
    },
}

ADVISORY_SENTENCE_TRANSLATIONS: dict[str, dict[str, str]] = {
    # Healthy reason
    "good agricultural practices and favorable weather conditions.": {
        "hi": "उचित कृषि पद्धतियां और अनुकूल मौसम की स्थिति।",
        "te": "మంచి వ్యవసాయ పద్ధతులు మరియు అనుకూలమైన వాతావరణ పరిస్థితులు.",
        "mr": "उत्तम शेती पद्धती आणि अनुकूल हवामान.",
        "es": "Buenas prácticas agrícolas y condiciones climáticas favorables.",
    },
    "favorable growing conditions, proper nutrition, and robust crop resistance.": {
        "hi": "अनुकूल विकास की स्थिति, उचित पोषण और मजबूत फसल प्रतिरोधक क्षमता।",
        "te": "అనుకూలమైన ఎదుగుదల పరిస్థితులు, సరైన పోషణ మరియు బలమైన పంట నిరోధకత.",
        "mr": "अनुकूल वाढीची परिस्थिती, योग्य पोषण आणि पिकाची मजबूत प्रतिकारशक्ती.",
        "es": "Condiciones de crecimiento favorables, nutrición adecuada y robusta resistencia del cultivo.",
    },
    # Common reasons
    "high leaf wetness, persistent warm temperatures, splashing rain, or use of infected seeds.": {
        "hi": "पत्तियों पर अत्यधिक नमी, लगातार गर्म तापमान, बारिश की बूंदों के छींटे, या संक्रमित बीजों का उपयोग।",
        "te": "ఆకులపై అధిక తేమ, నిరంతర వెచ్చని ఉష్ణోగ్రతలు, వర్షపు తుంపర్లు లేదా సోకిన విత్తనాల వాడకం.",
        "mr": "पानांवर जास्त ओलावा, सतत उष्ण तापमान, पावसाचे थेंब किंवा संक्रमित बियाण्यांचा वापर.",
        "es": "Alta humedad en las hojas, temperaturas cálidas persistentes, lluvia salpicada o uso de semillas infectadas.",
    },
    "warm weather (25-30°c) combined with high relative humidity and extended periods of dew.": {
        "hi": "गर्म मौसम (25-30°C) के साथ उच्च सापेक्ष आर्द्रता और लंबे समय तक ओस रहना।",
        "te": "వెచ్చని వాతావరణం (25-30°C) తో పాటు అధిక సాపేక్ష ఆర్ద్రత మరియు సుదీర్ఘ మంచు కాలం.",
        "mr": "उष्ण हवामान (२५-३०°C) सोबत उच्च सापेक्ष आर्द्रता आणि दीर्घकाळ दव पडणे.",
        "es": "Clima cálido (25-30°C) combinado con alta humedad relativa y períodos prolongados de rocío.",
    },
    "cool, humid weather conditions and persistent leaf wetness.": {
        "hi": "ठंडा व आर्द्र मौसम और पत्तियों पर लगातार गीलापन।",
        "te": "చల్లని, తేమతో కూడిన వాతావరణ పరిస్థితులు మరియు నిరంతర ఆకు తేమ.",
        "mr": "थंड, दमट हवामान आणि पानांवर सतत ओलावा.",
        "es": "Condiciones climáticas frescas y húmedas y humedad foliar persistente.",
    },
    "warm, humid weather conditions (25-30°c) and infected crop residues left on the soil surface.": {
        "hi": "गर्म और आर्द्र मौसम (25-30°C) तथा मिट्टी की सतह पर छोड़े गए संक्रमित फसल अवशेष।",
        "te": "వెచ్చని, తేమతో కూడిన వాతావరణ పరిస్థితులు (25-30°C) మరియు నేల ఉపరితలంపై మిగిలి ఉన్న సోకిన పంట వ్యర్థాలు.",
        "mr": "उष्ण, दमट हवामान (२५-३०°C) आणि जमिनीच्या पृष्ठभागावर राहिलेले रोगट पिकांचे अवशेष.",
        "es": "Condiciones cálidas y húmedas (25-30°C) y residuos de cultivos infectados dejados en la superficie del suelo.",
    },
    "low soil potassium levels, poor root development due to soil compaction, or dry soil conditions limiting nutrient uptake.": {
        "hi": "मिट्टी में पोटेशियम का निम्न स्तर, मिट्टी के संघनन के कारण जड़ों का कमजोर विकास, या शुष्क मिट्टी के कारण पोषक तत्वों के अवशोषण में कमी।",
        "te": "నేలలో పొటాషియం తక్కువగా ఉండటం, నేల గట్టిపడటం వల్ల వేర్ల ఎదుగుదల లోపించడం లేదా పోషకాల శోషణను పరిమితం చేసే పొడి నేల పరిస్థితులు.",
        "mr": "मातीत पोटॅशियमची कमी पातळी, मातीच्या घट्टपणामुळे मुळांची कमजोर वाढ किंवा कोरड्या जमिनीमुळे अन्नद्रव्ये शोषून घेण्यास मर्यादा.",
        "es": "Bajos niveles de potasio en el suelo, desarrollo deficiente de raíces debido a la compactación del suelo o suelo seco que limita la absorción de nutrientes.",
    },
    "prolonged leaf wetness (6-12 hours), moderate temperatures (15-28°c), and airborne spores carried from infected regions.": {
        "hi": "पत्तियों पर लंबे समय तक गीलापन (6-12 घंटे), मध्यम तापमान (15-28°C), और संक्रमित क्षेत्रों से हवा द्वारा आने वाले बीजाणु।",
        "te": "దీర్ఘకాలిక ఆకు తేమ (6-12 గంటలు), మితమైన ఉష్ణోగ్రతలు (15-28°C), మరియు సోకిన ప్రాంతాల నుండి గాలి ద్వారా వ్యాపించే బీజాంశాలు.",
        "mr": "पानांवर दीर्घकाळ ओलावा (६-१२ तास), मध्यम तापमान (१५-२८°C), आणि हवेद्वारे येणारे बुरशीचे बीजाणू.",
        "es": "Humedad foliar prolongada (6-12 horas), temperaturas moderadas (15-28°C) y esporas transportadas por el aire desde regiones infectadas.",
    },
    "high humidity (>80%) and warm temperatures (25-33°c) combined with susceptible crop varieties.": {
        "hi": "अत्यधिक आर्द्रता (>80%) और गर्म तापमान (25-33°C) के साथ संवेदनशील फसल किस्मों का होना।",
        "te": "అధిక తేమ (>80%) మరియు వెచ్చని ఉష్ణోగ్రతలు (25-33°C) తో పాటు వ్యాధి త్వరగా సోకే రకాలు ఉండటం.",
        "mr": "जास्त आर्द्रता (>८०%) आणि उष्ण तापमान (२५-३३°C) सोबत संवेदनशील पिकांच्या जाती.",
        "es": "Alta humedad (>80%) y temperaturas cálidas (25-33°C) combinadas con variedades de cultivos susceptibles.",
    },

    # Recommendations
    "no disease detected. continue normal agronomic practices: ensure proper irrigation, balanced n-p-k fertilization, and conduct regular field scouting.": {
        "hi": "कोई रोग नहीं पाया गया। सामान्य कृषि कार्य जारी रखें: उचित सिंचाई, संतुलित एन-पी-के उर्वरक और नियमित खेत निरीक्षण सुनिश्चित करें।",
        "te": "ఎటువంటి తెగులు గుర్తించబడలేదు. సాధారణ వ్యవసాయ పద్ధతులను కొనసాగించండి: సరైన నీటిపారుదల, సమతుల్య ఎరువులు మరియు సాధారణ తనిఖీలను నిర్ధారించుకోండి.",
        "mr": "कोणताही रोग आढळला नाही. सामान्य कृषी पद्धती सुरू ठेवा: योग्य सिंचन, संतुलित खते आणि नियमित शेत निरीक्षण करा.",
        "es": "No se detectó ninguna enfermedad. Continúe con las prácticas agronómicas normales: asegure un riego adecuado, fertilización N-P-K equilibrada y monitoreo regular.",
    },
    "continue current agricultural practices. monitor regularly for early signs of pest or disease pressure.": {
        "hi": "वर्तमान कृषि पद्धतियां जारी रखें। कीट या रोग के शुरुआती लक्षणों के लिए नियमित निगरानी करें।",
        "te": "ప్రస్తుత వ్యవసాయ పద్ధతులను కొనసాగించండి. తెగుళ్లు లేదా వ్యాధుల సంకేతాల కోసం క్రమం తప్పకుండా పర్యవేక్షించండి.",
        "mr": "सध्याच्या कृषी पद्धती सुरू ठेवा. कीड किंवा रोगाच्या सुरुवातीच्या लक्षणांसाठी नियमित निरीक्षण करा.",
        "es": "Continúe con las prácticas agrícolas actuales. Monitoree regularmente para detectar signos tempranos de plagas o enfermedades.",
    },
    "apply propiconazole fungicide at 0.1% concentration. monitor field edges where infection typically initiates.": {
        "hi": "0.1% की सांद्रता पर प्रोपिकोनाज़ोल कवकनाशी का छिड़काव करें। खेत के किनारों की निगरानी करें जहाँ से संक्रमण आमतौर पर शुरू होता है।",
        "te": "0.1% గాఢతతో ప్రొపికొనజోల్ శిలీంద్ర సంహారిణిని పిచికారీ చేయండి. సంక్రమణ ప్రారంభమయ్యే పొలం అంచులను గమనించండి.",
        "mr": "०.१% तीव्रतेने प्रोपिकोनाझोल बुरशीनाशकाची फवारणी करा. जिथून प्रादुर्भाव सुरू होतो अशा बांधांची पाहणी करा.",
        "es": "Aplique fungicida propiconazol al 0.1% de concentración. Monitoree los bordes del campo donde suele iniciar la infección.",
    },
    "remove and destroy infected plant debris. apply mancozeb 75% wp at 2.5g/l as preventive spray.": {
        "hi": "संक्रमित पौधों के अवशेषों को हटाकर नष्ट करें। निवारक छिड़काव के रूप में 2.5 ग्राम/लीटर मैंकोज़ेब 75% डब्ल्यूपी का प्रयोग करें।",
        "te": "సోకిన మొక్కల వ్యర్థాలను తొలగించి నాశనం చేయండి. నివారణ పిచికారీగా మాంకోజెబ్ 75% WPని లీటరుకు 2.5 గ్రాముల చొప్పున వాడండి.",
        "mr": "रोगग्रस्त झाडांचे अवशेष गोळा करून नष्ट करा. प्रतिबंधात्मक फवारणी म्हणून मॅन्कोझेब ७५% डब्ल्यूपी २.५ ग्रॅम/लिटर फवारा.",
        "es": "Retire y destruya los restos de plantas infectadas. Aplique mancozeb 75% WP a 2.5g/L como aspersión preventiva.",
    },
    "plant rust-resistant varieties like hd-2967 or pbw-550. apply tebuconazole fungicide at onset of pustule formation.": {
        "hi": "एचडी-2967 या पीबीडब्ल्यू-550 जैसी रतुआ-प्रतिरोधी किस्में लगाएं। फफोले बनते ही टेबुकोनाज़ोल कवकनाशी का छिड़काव करें।",
        "te": "HD-2967 లేదా PBW-550 వంటి కుంకుమ తెగులు నిరోధక రకాలను సాగు చేయండి. తెగులు లక్షణాలు కనిపించిన వెంటనే టెబుకోనాజోల్ పిచికారీ చేయండి.",
        "mr": "HD-२९६७ किंवा PBW-५५० सारख्या तांबेरा-प्रतिरोधक वाणांची लागवड करा. लक्षणे दिसू लागताच टेबुकोनाझोल बुरशीनाशकाची फवारणी करा.",
        "es": "Siembre variedades resistentes a la roya como HD-2967 o PBW-550. Aplique fungicida tebuconazol al inicio de la formación de pústulas.",
    },
    "apply sulfur-based fungicide at 3g/l. avoid dense planting to improve air circulation.": {
        "hi": "3 ग्राम/लीटर की दर से गंधक-आधारित कवकनाशी का छिड़काव करें। वायु संचार बेहतर करने के लिए सघन बुवाई से बचें।",
        "te": "లీటరుకు 3 గ్రాముల చొప్పున గంధకం ఆధారిత శిలీంద్ర సంహారిణిని వాడండి. గాలి ప్రసరణను మెరుగుపరచడానికి దట్టమైన నాటడం నివారించండి.",
        "mr": "३ ग्रॅम/लिटर दराने गंधकयुक्त बुरशीनाशक फवारा. हवेचे खेळते प्रमाण वाढवण्यासाठी दाट लागवड टाळा.",
        "es": "Aplique fungicida a base de azufre a 3g/L. Evite la siembra densa para mejorar la circulación del aire.",
    },
    "apply tricyclazole 75% wp at 0.6g/l. avoid excess nitrogen fertilization and ensure proper spacing.": {
        "hi": "0.6 ग्राम/लीटर की दर से ट्राइसाइक्लाज़ोल 75% डब्ल्यूपी का छिड़काव करें। अधिक नाइट्रोजन उर्वरक से बचें और उचित दूरी बनाए रखें।",
        "te": "ట్రైసైక్లాజోల్ 75% WPని లీటరుకు 0.6 గ్రాముల చొప్పున పిచికారీ చేయండి. అధిక నత్రజని ఎరువులను నివారించండి మరియు సరైన అంతరాన్ని పాటించండి.",
        "mr": "०.६ ग्रॅम/लिटर दराने ट्रायसायक्लॅझोल ७५% डब्ल्यूपी फवारा. जास्त नायट्रोजन खते टाळा आणि योग्य अंतर ठेवा.",
        "es": "Aplique triciclazol 75% WP a 0.6g/L. Evite el exceso de fertilización nitrogenada y asegure un espaciamiento adecuado.",
    },
    "apply chlorothalonil or copper-based fungicide. ensure proper plant spacing for air circulation.": {
        "hi": "क्लोरोथालोनिल या कॉपर-आधारित कवकनाशी का छिड़काव करें। वायु संचार के लिए पौधों के बीच उचित दूरी सुनिश्चित करें।",
        "te": "క్లోరోథలోనిల్ లేదా రాగి ఆధారిత శిలీంద్ర సంహారిణిని వాడండి. గాలి ప్రసరణ కోసం మొక్కల మధ్య సరైన స్థలాన్ని ఉంచండి.",
        "mr": "क्लोरोथॅलोनिल किंवा कॉपरयुक्त बुरशीनाशकाची फवारणी करा. हवेच्या हालचालीसाठी रोपांमध्ये योग्य अंतर ठेवा.",
        "es": "Aplique clorotalonil o fungicida a base de cobre. Asegure el espaciamiento adecuado para la circulación del aire.",
    },
    "remove and destroy affected plants immediately. apply metalaxyl + mancozeb combination spray.": {
        "hi": "प्रभावित पौधों को तुरंत उखाड़कर नष्ट करें। मेटालेक्सिल + मैंकोज़ेब के संयुक्त घोल का छिड़काव करें।",
        "te": "సోకిన మొక్కలను వెంటనే తొలగించి నాశనం చేయండి. మెటలాక్సిల్ + మాంకోజెబ్ కలయికతో పిచికారీ చేయండి.",
        "mr": "बाधित झाडे तात्काळ काढून नष्ट करा. मेटालाक्सिल + मॅन्कोझेब मिश्रणाची फवारणी करा.",
        "es": "Retire y destruya las plantas afectadas de inmediato. Aplique aspersión combinada de metalaxil + mancozeb.",
    },
    "avoid overhead irrigation to reduce humidity. spray copper oxychloride at 2g/l or streptocycline at 100ppm if infection is severe. implement crop rotation with non-legumes next season.": {
        "hi": "नमी कम करने के लिए फव्वारा सिंचाई से बचें। कॉपर ऑक्सीक्लोराइड 2 ग्राम/लीटर या संक्रमण अधिक होने पर स्ट्रेप्टोसाइक्लिन 100 पीपीएम का छिड़काव करें। अगली फसल में गैर-दलहनी फसलों के साथ फसल चक्र अपनाएं।",
        "te": "తేమను తగ్గించడానికి పైనుండి నీరు చిలకరించే పద్ధతిని నివారించండి. ఇన్ఫెక్షన్ తీవ్రంగా ఉంటే కాపర్ ఆక్సిక్లోరైడ్ 2 గ్రా/లీ లేదా స్ట్రెప్టోసైక్లిన్ 100 ppm పిచికారీ చేయండి. వచ్చే సీజన్లో పప్పుధాన్యాలు కాని పంటలతో పంట మార్పిడి చేయండి.",
        "mr": "आर्द्रता कमी करण्यासाठी स्प्रिंकलर सिंचन टाळा. संसर्ग तीव्र असल्यास कॉपर ऑक्सिक्लोराईड २ ग्रॅम/लिटर किंवा स्ट्रेप्टोमायसीन १०० पीपीएम फवारा. पुढच्या हंगामात कडधान्येतर पिकांचे फेरपालट करा.",
        "es": "Evite el riego por aspersión para reducir la humedad. Rocíe oxicloruro de cobre a 2g/L o estreptociclina a 100ppm si la infección es grave. Aplique rotación de cultivos con no leguminosas la próxima temporada.",
    },
    "apply foliar fungicides such as strobilurins (e.g. pyraclostrobin) or triazoles at early bloom (r1-r3 stage). use certified disease-free seeds and plow under crop residue.": {
        "hi": "शुरुआती फूल आने की अवस्था (R1-R3) में स्ट्रोबिल्यूरिन या ट्रायज़ोल जैसे पर्ण कवकनाशी का प्रयोग करें। प्रमाणित रोगमुक्त बीजों का उपयोग करें और फसल अवशेषों को मिट्टी में दबा दें।",
        "te": "మొదటి పూత దశలో (R1-R3) స్ట్రోబిలురిన్లు లేదా ట్రయాజోల్స్ వంటి శిలీంద్ర సంహారిణులను పిచికారీ చేయండి. ధృవీకరించబడిన విత్తనాలను వాడండి.",
        "mr": "सुरुवातीच्या फुलधारणेच्या अवस्थेत (R1-R3) स्ट्रोबिल्यूरिन किंवा ट्रायझोल बुरशीनाशक फवारा. प्रमाणित रोगमुक्त बियाणे वापरा आणि पिकाचे अवशेष जमिनीत गाडून टाका.",
        "es": "Aplique fungicidas foliares como estrobirulinas o triazoles en floración temprana. Use semillas certificadas libres de enfermedades.",
    },
    "maintain wider row spacing to improve air circulation. apply metalaxyl or mancozeb fungicide at 2g/l if infection spreads rapidly. plant resistant varieties.": {
        "hi": "वायु संचार बेहतर करने के लिए पंक्तियों के बीच अधिक दूरी रखें। संक्रमण तेजी से फैलने पर 2 ग्राम/लीटर की दर से मेटालेक्सिल या मैंकोज़ेब का छिड़काव करें। प्रतिरोधी किस्में लगाएं।",
        "te": "గాలి ప్రసరణ మెరుగుపరచడానికి ఎక్కువ వరుసల అంతరాన్ని పాటించండి. తెగులు వేగంగా వ్యాపిస్తే 2 గ్రా/లీ మెటలాక్సిల్ లేదా మాంకోజెబ్ పిచికారీ చేయండి.",
        "mr": "हवेचा वावर चांगला राहण्यासाठी ओळींमध्ये योग्य अंतर ठेवा. प्रादुर्भाव वाढल्यास २ ग्रॅम/लिटर दराने मेटालाक्सिल किंवा मॅन्कोझेब फवारा. रोगप्रतिकारक वाण लावा.",
        "es": "Mantenga mayor separación entre hileras para mejorar la circulación del aire. Aplique metalaxil o mancozeb a 2g/L si la infección se propaga rápidamente.",
    },
    "apply quinone outside inhibitor (qoi) or methyl benzimidazole carbamate (mbc) fungicides. plant resistant cultivars and practice crop rotation.": {
        "hi": "QoI या MBC कवकनाशी का छिड़काव करें। रोग प्रतिरोधी किस्मों की बुवाई करें और फसल चक्र का पालन करें।",
        "te": "QoI లేదా MBC ఆధారిత శిలీంద్ర సంహారిణులను వాడండి. తెగులు నిరోధక రకాలను నాటండి మరియు పంట మార్పిడి చేయండి.",
        "mr": "योग्य बुरशीनाशकाची फवारणी करा. रोगप्रतिकारक वाणांची लागवड करा आणि पिकांची फेरपालट करा.",
        "es": "Aplique fungicidas inhibidores de quinonas (QoI) o carbamatos. Siembre cultivares resistentes y practique la rotación de cultivos.",
    },
    "apply potassium-rich fertilizers (such as muriate of potash, k2o) based on soil test recommendations. ensure soil compaction is minimized to promote root health.": {
        "hi": "मिट्टी परीक्षण की सिफारिशों के आधार पर पोटाश युक्त उर्वरक (जैसे MOP, K2O) डालें। जड़ों के विकास के लिए मिट्टी के कड़ेपन को कम करें।",
        "te": "నేల పరీక్ష సిఫార్సుల ఆధారంగా పొటాష్ ఎరువులను వేయండి. వేళ్ల ఆరోగ్యానికి నేల గట్టిపడకుండా చూసుకోండి.",
        "mr": "माती परीक्षणानुसार पोटॅशयुक्त खते (उदा. म्युरिएट ऑफ पोटॅश) द्या. मुळांच्या वाढीसाठी माती भुसभुशीत ठेवा.",
        "es": "Aplique fertilizantes ricos en potasio (como muriato de potasio) según el análisis de suelo. Minimice la compactación para favorecer las raíces.",
    },
    "immediately spray triazole or strobilurin-based fungicides (e.g., tebuconazole at 1ml/l or propiconazole). monitor field daily as the disease spreads rapidly.": {
        "hi": "तुरंत ट्रायज़ोल या स्ट्रोबिल्यूरिन आधारित कवकनाशी (जैसे टेबुकोनाज़ोल 1 मिली/लीटर या प्रोपिकोनाज़ोल) का छिड़काव करें। रोग तेजी से फैलता है, इसलिए खेत की दैनिक निगरानी करें।",
        "te": "వెంటనే టెబుకోనాజోల్ (1 మి.లీ/లీ) లేదా ప్రొపికొనజోల్ వంటి శిలీంద్ర సంహారిణులను పిచికారీ చేయండి. తెగులు వేగంగా వ్యాపిస్తుంది కాబట్టి రోజూ పర్యవేక్షించండి.",
        "mr": "तात्काळ ट्रायझोल किंवा स्ट्रोबिल्यूरिनयुक्त बुरशीनाशक (उदा. टेबुकोनाझोल १ मिली/लिटर) फवारा. रोग झपाट्याने पसरत असल्याने रोज शेतीची पाहणी करा.",
        "es": "Rocíe de inmediato fungicidas a base de triazol o estrobirulina (ej. tebuconazol a 1ml/L o propiconazol). Monitoree el campo a diario.",
    },
    "apply fluxapyroxad or prothioconazole fungicides if disease reaches lower canopy early. practice crop rotation with corn or wheat, and manage weeds.": {
        "hi": "यदि रोग जल्दी निचली पत्तियों तक पहुँच जाए तो फ्लुक्सापाइरोक्सैड या प्रोथियोकोनाज़ोल कवकनाशी का छिड़काव करें। मक्का या गेहूं के साथ फसल चक्र अपनाएं और खरपतवार नियंत्रण करें।",
        "te": "రోగం ప్రారంభ దశలోనే దిగువ ఆకులకు చేరితే తగిన శిలీంద్ర సంహారిణులను పిచिकారీ చేయండి. మొక్కజొన్న లేదా గోధుమలతో పంట మార్పిడి చేయండి.",
        "mr": "रोग खालच्या पानांवर लवकर आल्यास योग्य बुरशीनाशकाची फवारणी करा. मका किंवा गव्हाबरोबर पिकांची फेरपालट करा आणि तण नियंत्रण करा.",
        "es": "Aplique fungicidas si la enfermedad alcanza el dosel inferior tempranamente. Practique rotación de cultivos con maíz o trigo.",
    },
}

def normalize_key(text: str) -> str:
    """Normalize text by lowercasing, stripping, and collapsing whitespace."""
    return re.sub(r"\s+", " ", text.strip().lower())

def translate_template_reason(text: str, target_lang: str) -> Optional[str]:
    """Translate dynamic mock reasons such as:
    'Fungal spore transmission, high relative humidity (above 85%), and prolonged wetness on the leaves of the {crop} crop.'
    """
    pattern = re.compile(
        r"fungal spore transmission,\s*high relative humidity\s*\(above 85%\),\s*and prolonged wetness on the leaves of the\s+(.+?)\s+crop\.?",
        re.IGNORECASE,
    )
    match = pattern.search(text.strip())
    if not match:
        return None

    crop_raw = match.group(1).strip().lower()
    crop_name = CROP_TRANSLATIONS.get(crop_raw, {}).get(target_lang, crop_raw.capitalize())

    if target_lang == "hi":
        return f"कवक बीजाणु संचरण, उच्च सापेक्ष आर्द्रता (85% से अधिक), और {crop_name} फसल की पत्तियों पर लंबे समय तक गीलापन।"
    elif target_lang == "te":
        return f"శిలీంద్ర బీజాల వ్యాప్తి, అధిక సాపేక్ష ఆర్ద్రత (85% కంటే ఎక్కువ), మరియు {crop_name} పంట ఆకులపై దీర్ఘకాలిక తేమ."
    elif target_lang == "mr":
        return f"बुरशीजन्य बीजाणूंचा प्रसार, उच्च सापेक्ष आर्द्रता (८५% पेक्षा जास्त), आणि {crop_name} पिकाच्या पानांवर दीर्घकाळ ओलावा."
    elif target_lang == "es":
        return f"Transmisión de esporas fúngicas, alta humedad relativa (superior al 85%) y humedad prolongada en las hojas del cultivo de {crop_name}."

    return None

def get_dictionary_translation(text: str, target_lang: str) -> Optional[str]:
    """Check fast domain-specific dictionary lookups."""
    if target_lang not in {"hi", "te", "mr", "es"}:
        return None

    norm = normalize_key(text)

    # 1. Crops
    if norm in CROP_TRANSLATIONS and target_lang in CROP_TRANSLATIONS[norm]:
        return CROP_TRANSLATIONS[norm][target_lang]

    # 2. Severities
    if norm in SEVERITY_TRANSLATIONS and target_lang in SEVERITY_TRANSLATIONS[norm]:
        return SEVERITY_TRANSLATIONS[norm][target_lang]

    # 3. Diseases
    if norm in DISEASE_TRANSLATIONS and target_lang in DISEASE_TRANSLATIONS[norm]:
        return DISEASE_TRANSLATIONS[norm][target_lang]

    # 4. Status and UI strings
    if norm in STATUS_AND_UI_TRANSLATIONS and target_lang in STATUS_AND_UI_TRANSLATIONS[norm]:
        return STATUS_AND_UI_TRANSLATIONS[norm][target_lang]

    # 5. Full Advisory Sentences & Reasons
    if norm in ADVISORY_SENTENCE_TRANSLATIONS and target_lang in ADVISORY_SENTENCE_TRANSLATIONS[norm]:
        return ADVISORY_SENTENCE_TRANSLATIONS[norm][target_lang]

    # 6. Check dynamic template reasons
    template_res = translate_template_reason(text, target_lang)
    if template_res:
        return template_res

    return None
