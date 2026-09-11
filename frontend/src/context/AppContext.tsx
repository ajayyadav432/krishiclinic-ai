"use client";

import React, { createContext, useContext, useState, useEffect } from "react";

export interface UserProfile {
  id: string;
  username: string;
  role: "FARMER" | "AGRONOMIST" | "ADMIN";
  token: string;
}

interface AppContextType {
  user: UserProfile | null;
  language: string;
  isInitialized: boolean;
  t: (key: string) => string;
  translateDynamic: (text: string) => Promise<string>;
  login: (token: string) => void;
  logout: () => void;
  setLanguage: (lang: string) => void;
}

const AppContext = createContext<AppContextType | undefined>(undefined);

const COMMON_DISEASES: Record<string, Record<string, string>> = {
  "Yellow Rust": {
    hi: "पीला रतुआ (Yellow Rust)",
    te: "పసుపు కుంకుమ తెగులు (Yellow Rust)",
    mr: "तांबेरा रोग (Yellow Rust)",
    es: "Roya amarilla (Yellow Rust)",
  },
  "Leaf Blight": {
    hi: "पत्ता झुलसा (Leaf Blight)",
    te: "ఆకు ఎండు తెగులు (Leaf Blight)",
    mr: "पानांवरील करपा (Leaf Blight)",
    es: "Tizón foliar (Leaf Blight)",
  },
  "Stem Rust": {
    hi: "तना रतुआ (Stem Rust)",
    te: "కాండం కుంకుమ తెగులు (Stem Rust)",
    mr: "खोडावरील तांबेरा (Stem Rust)",
    es: "Roya del tallo (Stem Rust)",
  },
  "Powdery Mildew": {
    hi: "चूर्णिल आसिता (Powdery Mildew)",
    te: "బూడిద తెగులు (Powdery Mildew)",
    mr: "भुरी रोग (Powdery Mildew)",
    es: "Oídio (Powdery Mildew)",
  },
  "Karnal Bunt": {
    hi: "करनाल बंट (Karnal Bunt)",
    te: "కర్నాల్ బంట్ (Karnal Bunt)",
    mr: "कर्नाल बंट (Karnal Bunt)",
    es: "Carbón parcial (Karnal Bunt)",
  },
  "Blast": {
    hi: "झोंका रोग (Blast)",
    te: "అగ్గి తెగులు (Blast)",
    mr: "करपा रोग (Blast)",
    es: "Añublo (Blast)",
  },
  "Brown Spot": {
    hi: "भूरा धब्बा (Brown Spot)",
    te: "గోధుమ రంగు మచ్చ తెగులు (Brown Spot)",
    mr: "तपकिरी ठिपके (Brown Spot)",
    es: "Mancha marrón (Brown Spot)",
  },
  "Bacterial Leaf Blight": {
    hi: "जीवाणु झुलसा (Bacterial Leaf Blight)",
    te: "బ్యాక్టీరియా ఆకు ఎండు తెగులు (Bacterial Leaf Blight)",
    mr: "जिवाणूजन्य पानांवरील करपा (Bacterial Leaf Blight)",
    es: "Tizón bacteriano de la hoja (Bacterial Leaf Blight)",
  },
  "Sheath Blight": {
    hi: "शीथ ब्लाइट (Sheath Blight)",
    te: "మట్ట కుళ్లు తెగులు (Sheath Blight)",
    mr: "खोडावरील करपा (Sheath Blight)",
    es: "Tizón de la vaina (Sheath Blight)",
  },
  "Early Blight": {
    hi: "अगेती झुलसा (Early Blight)",
    te: "ఆకు మచ్చ తెగులు (Early Blight)",
    mr: "लवकर येणारा करपा (Early Blight)",
    es: "Tizón temprano (Early Blight)",
  },
  "Late Blight": {
    hi: "पछेती झुलसा (Late Blight)",
    te: "మలిదశ ఆకుమచ్చ తెగులు (Late Blight)",
    mr: "उशिरा येणारा करपा (Late Blight)",
    es: "Tizón tardío (Late Blight)",
  },
  "Fusarium Wilt": {
    hi: "फ्यूजेरियम म्लानि (Fusarium Wilt)",
    te: "ఫ్యుసేరియం ఎండు తెగులు (Fusarium Wilt)",
    mr: "फ्युजेरियम मर रोग (Fusarium Wilt)",
    es: "Marchitez por Fusarium (Fusarium Wilt)",
  },
  "Leaf Curl Virus": {
    hi: "पर्ण कुंचन विषाणु (Leaf Curl Virus)",
    te: "ఆకు ముడుత వైరస్ (Leaf Curl Virus)",
    mr: "चुरडा-मुरडा रोग (Leaf Curl Virus)",
    es: "Virus del enrollamiento de la hoja (Leaf Curl Virus)",
  },
  "Northern Leaf Blight": {
    hi: "उत्तरी पत्ता झुलसा (Northern Leaf Blight)",
    te: "ఉత్తర ఆకు ఎండు తెగులు (Northern Leaf Blight)",
    mr: "उत्तरी पानांवरील करपा (Northern Leaf Blight)",
    es: "Tizón foliar del norte (Northern Leaf Blight)",
  },
  "Gray Leaf Spot": {
    hi: "सलेटी पत्ता धब्बा (Gray Leaf Spot)",
    te: "బూడిద రంగు ఆకుమచ్చ తెగులు (Gray Leaf Spot)",
    mr: "राखाडी पानांवरील ठिपके (Gray Leaf Spot)",
    es: "Mancha foliar gris (Gray Leaf Spot)",
  },
  "Common Rust": {
    hi: "सामान्य रतुआ (Common Rust)",
    te: "సాధారణ కుంకుమ తెగులు (Common Rust)",
    mr: "सामान्य तांबेरा (Common Rust)",
    es: "Roya común (Common Rust)",
  },
  "Stalk Rot": {
    hi: "तना सड़न (Stalk Rot)",
    te: "కాండం కుళ్లు తెగులు (Stalk Rot)",
    mr: "खोड कुजणे (Stalk Rot)",
    es: "Pudrición del tallo (Stalk Rot)",
  },
  "Common Scab": {
    hi: "सामान्य पपड़ी (Common Scab)",
    te: "సాధారణ స్కాబ్ (Common Scab)",
    mr: "खवले रोग (Common Scab)",
    es: "Sarna común (Common Scab)",
  },
  "Black Scurf": {
    hi: "काली रूसी (Black Scurf)",
    te: "నల్ల పొలుసు తెగులు (Black Scurf)",
    mr: "काळी खपली (Black Scurf)",
    es: "Costra negra (Black Scurf)",
  },
  "Bacterial Blight": {
    hi: "जीवाणु जनित झुलसा (Bacterial Blight)",
    te: "బ్యాక్టీరియా ఎండు తెగులు (Bacterial Blight)",
    mr: "जिवाणूजन्य करपा (Bacterial Blight)",
    es: "Tizón bacteriano (Bacterial Blight)",
  },
  "Cotton Leaf Curl Virus": {
    hi: "कपास पर्ण कुंचन विषाणु (Cotton Leaf Curl Virus)",
    te: "పత్తి ఆకు ముడుత వైరస్ (Cotton Leaf Curl Virus)",
    mr: "कापूस चुरडा-मुरडा विषाणू (Cotton Leaf Curl Virus)",
    es: "Virus del rizado del algodón (Cotton Leaf Curl Virus)",
  },
  "Alternaria Leaf Spot": {
    hi: "अल्टरनेरिया पत्ता धब्बा (Alternaria Leaf Spot)",
    te: "ఆల్టర్నేరియా ఆకుమచ్చ తెగులు (Alternaria Leaf Spot)",
    mr: "अल्टरनेरिया पानांवरील ठिपके (Alternaria Leaf Spot)",
    es: "Mancha foliar por Alternaria (Alternaria Leaf Spot)",
  },
  "Red Rot": {
    hi: "लाल सड़न रोग (Red Rot)",
    te: "ఎర్ర కుళ్లు తెగులు (Red Rot)",
    mr: "ऊस तांबेरा / लाल कुजव्या (Red Rot)",
    es: "Pudrición roja (Red Rot)",
  },
  "Smut": {
    hi: "कंडुआ रोग (Smut)",
    te: "కాటుక తెగులు (Smut)",
    mr: "काजळी रोग (Smut)",
    es: "Carbón (Smut)",
  },
  "Grassy Shoot Disease": {
    hi: "घासी प्ररोह रोग (Grassy Shoot)",
    te: "గడ్డి పిలకల తెగులు (Grassy Shoot)",
    mr: "गवती वाढ रोग (Grassy Shoot)",
    es: "Enfermedad de los brotes herbáceos (Grassy Shoot)",
  },
  "Rust": {
    hi: "रतुआ रोग (Rust)",
    te: "కుంకుమ తెగులు (Rust)",
    mr: "तांबेरा (Rust)",
    es: "Roya (Rust)",
  },
  "Cercospora Leaf Blight": {
    hi: "सर्कोस्पोरा पत्ता झुलसा (Cercospora Leaf Blight)",
    te: "సెర్కోస్పోరా ఆకుమచ్చ తెగులు (Cercospora Leaf Blight)",
    mr: "सर्कोस्पोरा पानांवरील करपा (Cercospora Leaf Blight)",
    es: "Tizón foliar por Cercospora (Cercospora Leaf Blight)",
  },
  "Charcoal Rot": {
    hi: "चारकोल सड़न (Charcoal Rot)",
    te: "బొగ్గు కుళ్లు తెగులు (Charcoal Rot)",
    mr: "चारकोल सड (Charcoal Rot)",
    es: "Pudrición carbonosa (Charcoal Rot)",
  },
  "White Rust": {
    hi: "सफेद रतुआ (White Rust)",
    te: "తెల్ల కుంకుమ తెగులు (White Rust)",
    mr: "पांढरा तांबेरा (White Rust)",
    es: "Roya blanca (White Rust)",
  },
  "Alternaria Blight": {
    hi: "अल्टरनेरिया झुलसा (Alternaria Blight)",
    te: "ఆల్టర్నేరియా బ్లైట్ (Alternaria Blight)",
    mr: "अल्टरनेरिया करपा (Alternaria Blight)",
    es: "Tizón por Alternaria (Alternaria Blight)",
  },
  "Tikka Disease": {
    hi: "टिक्का रोग (Tikka Disease)",
    te: "టిక్కా తెగులు (Tikka Disease)",
    mr: "टिक्का रोग (Tikka Disease)",
    es: "Enfermedad de Tikka (Tikka Disease)",
  },
  "Collar Rot": {
    hi: "कॉलर सड़न (Collar Rot)",
    te: "మొక్క మొదలు కుళ్లు (Collar Rot)",
    mr: "कॉलर कुजव्या (Collar Rot)",
    es: "Pudrición del cuello (Collar Rot)",
  },
  "Anthracnose": {
    hi: "एंथ्रेक्नोज (Anthracnose)",
    te: "ఆంత్రాక్నోస్ (Anthracnose)",
    mr: "अँथ्रॅक्नोज (Anthracnose)",
    es: "Antracnosis (Anthracnose)",
  },
  "Downy Mildew": {
    hi: "मृदुरोमिल आसिता (Downy Mildew)",
    te: "డౌనీ బూజు తెగులు (Downy Mildew)",
    mr: "केवडा रोग (Downy Mildew)",
    es: "Mildiu velloso (Downy Mildew)",
  },
  "Downey Mildew": {
    hi: "मृदुरोमिल आसिता (Downy Mildew)",
    te: "డౌనీ బూజు తెగులు (Downy Mildew)",
    mr: "केवडा रोग (Downy Mildew)",
    es: "Mildiu velloso (Downy Mildew)",
  },
  "Frogeye": {
    hi: "मेंढक आंख पत्ता धब्बा (Frogeye Leaf Spot)",
    te: "కప్ప కన్ను ఆకుమచ్చ తెగులు (Frogeye Leaf Spot)",
    mr: "फ्रॉगआय पानांवरील ठिपके (Frogeye Leaf Spot)",
    es: "Mancha ojo de rana (Frogeye Leaf Spot)",
  },
  "Frogeye Leaf Spot": {
    hi: "मेंढक आंख पत्ता धब्बा (Frogeye Leaf Spot)",
    te: "కప్ప కన్ను ఆకుమచ్చ తెగులు (Frogeye Leaf Spot)",
    mr: "फ्रॉगआय पानांवरील ठिपके (Frogeye Leaf Spot)",
    es: "Mancha ojo de rana (Frogeye Leaf Spot)",
  },
  "Potassium Deficiency": {
    hi: "पोटेशियम की कमी (Potassium Deficiency)",
    te: "పొటాషియం లోపం (Potassium Deficiency)",
    mr: "पोटॅशियमची कमतरता (Potassium Deficiency)",
    es: "Deficiencia de potasio (Potassium Deficiency)",
  },
  "Soybean Rust": {
    hi: "सोयाबीन रतुआ (Soybean Rust)",
    te: "సోయాబీన్ కుంకుమ తెగులు (Soybean Rust)",
    mr: "सोयाबीन तांबेरा (Soybean Rust)",
    es: "Roya de la soja (Soybean Rust)",
  },
  "Target Spot": {
    hi: "टारगेट स्पॉट (Target Spot)",
    te: "టార్గెట్ స్పాట్ (Target Spot)",
    mr: "टार्गेट स्पॉट (Target Spot)",
    es: "Mancha diana (Target Spot)",
  },
};

const BASE_STATIC_TRANSLATIONS: Record<string, Record<string, string>> = {
  hi: {
    "Upload": "अपलोड करें",
    "History": "इतिहास",
    "Analytics": "विश्लेषण",
    "Outbreak Radar": "प्रकोप रडार",
    "Crop Disease Diagnosis": "फसल रोग निदान",
    "Upload a photo of your crop and our AI will analyze it for potential diseases, providing severity assessment and treatment recommendations.":
      "अपनी फसल की एक तस्वीर अपलोड करें और हमारी एआई संभावित बीमारियों के लिए इसका विश्लेषण करेगी, जिससे तीव्रता का आकलन और उपचार की सिफारिशें मिलेंगी।",
    "Secure file handling": "सुरक्षित फ़ाइल हैंडलिंग",
    "Instant AI analysis": "त्वरित एआई विश्लेषण",
    "8+ crop types": "8+ फसल प्रकार",
    "Crop Type": "फसल का प्रकार",
    "Select a crop": "फसल चुनें",
    "Farmer Notes": "किसान की टिप्पणियां",
    "Describe what you see (e.g., yellow spots, wilting)": "बताएं कि आप क्या देख रहे हैं (जैसे पीले धब्बे, मुरझाना)",
    "AI Model": "एआई मॉडल",
    "Upload Image": "तस्वीर अपलोड करें",
    "Analyzing...": "विश्लेषण किया जा रहा है...",
    "Diagnosis Result": "निदान का परिणाम",
    "Confidence": "विश्वास स्तर",
    "Severity": "तीव्रता",
    "Treatment Recommendation": "उपचार की सिफारिश",
    "Verified Advisory": "सत्यापित उपचार सलाह",
    "Pending Review": "समीक्षा लंबित है",
    "Verified": "सत्यापित",
    "Logout": "लॉगआउट",
    "Login": "लॉगिन",
    "Username": "उपयोगकर्ता नाम",
    "Password": "पासवर्ड",
    "Register": "पंजीकरण",
    "Agronomist Portal": "कृषि विज्ञानी पोर्टल",
    "Pending Requests": "समीक्षा के लिए लंबित अनुरोध",
    "Submit Review": "समीक्षा जमा करें",
    "Confirm Diagnosis": "निदान की पुष्टि करें",
    "Verified Disease Name": "सत्यापित रोग का नाम",
    "Verified Severity": "सत्यापित तीव्रता",
    "Advisory Notes / Treatment": "सलाहकार नोट्स / उपचार",
    "Please log in to use Krishi Clinic.": "कृषि क्लिनिक का उपयोग करने के लिए कृपया लॉगिन करें।",
    "Login Credentials": "लॉगिन क्रेडेंशियल",
    "Farmer Profile": "किसान प्रोफ़ाइल",
    "Agronomist Profile": "कृषि विज्ञानी प्रोफ़ाइल",
    "Select Role": "भूमिका चुनें",
    "Create Account": "खाता बनाएं",
    "Already have an account? Login": "पहले से ही एक खाता है? लॉगिन करें",
    "Don't have an account? Register": "खाता नहीं है? पंजीकरण करें",
    "Error": "त्रुटि",
    "Success": "सफलता",
    "History List": "इतिहास सूची",
    "No predictions found.": "कोई इतिहास नहीं मिला।",
    "Export CSV": "सीएसवी निर्यात",
    "Back to History": "इतिहास पर वापस जाएं",
    "Analyzed on": "विश्लेषण की तिथि",
    "AI Provider": "एआई प्रदाता",
    "Farmer Observations": "किसान का अवलोकन",
    "Status": "स्थिति",
    "Low": "निम्न",
    "Medium": "मध्यम",
    "High": "उच्च",
    "Date": "दिनांक",
    "Crop": "फसल",
    "Disease": "बीमारी",
    "Provider": "प्रदाता",
    "View": "देखें",
    "All crops": "सभी फसलें",
    "Filter by disease...": "बीमारी से छानें...",
    "Clear Filters": "फ़िल्टर साफ़ करें",
    "Previous": "पिछला",
    "Next": "अगला",
    "Page": "पृष्ठ",
    "Showing": "दिखा रहा है",
    "of": "का",
    "predictions": "पूर्वानुमान",
    "PENDING": "लंबित",
    "PENDING_REVIEW": "समीक्षा लंबित",
    "REVIEWED": "सत्यापित",
    "Wheat": "गेहूं",
    "Rice": "चावल",
    "Tomato": "टमाटर",
    "Corn": "मक्का",
    "Potato": "आलू",
    "Cotton": "कपास",
    "Sugarcane": "गन्ना",
    "Soybean": "सोयाबीन",
    "Mustard": "सरसों",
    "Groundnut": "मूंगफली",
    "Chilli": "मिर्च",
    "mock": "Mock (परीक्षण)",
    "local": "Local PyTorch (स्थानीय मॉडल)",
    "gemini": "Google Gemini",
    "groq": "Groq Llama 4",
    "openai": "OpenAI GPT",
    "Hidden": "प्रच्छन्न",
    "Healthy": "स्वस्थ",
    "Voice Advisory": "ध्वनि सलाह",
    "Export PDF Advisory": "पीडीएफ सलाह निर्यात करें",
    "Exporting...": "निर्यात हो रहा है...",
    "Active Disease Clusters": "सक्रिय रोग क्लस्टर",
    "High Risk Areas": "उच्च जोखिम वाले क्षेत्र",
    "Monitored Field Cases": "निगरानी किए गए खेत मामले",
    "Early Warning Protocol": "प्रारंभिक चेतावनी प्रोटोकॉल",
    "Active (25km Radius)": "सक्रिय (25 किमी दायरा)",
    "Subscribe to Village Outbreak SMS Alerts": "ग्राम प्रकोप एसएमएस अलर्ट की सदस्यता लें",
    "Receive automated SMS warnings when crop diseases are identified on neighboring plots within your radius.":
      "अपने दायरे में पड़ोसी खेतों पर फसल रोगों की पहचान होने पर स्वचालित एसएमएस चेतावनी प्राप्त करें।",
    "Enter mobile number": "मोबाइल नंबर दर्ज करें",
    "Enable Proximity Warnings": "समीपस्थ चेतावनी सक्षम करें",
    "Proximity alert subscription enabled successfully.": "समीपस्थ चेतावनी सदस्यता सफलतापूर्वक सक्षम की गई।",
    "Active Regional Infestation Clusters": "सक्रिय क्षेत्रीय संक्रमण क्लस्टर",
    "Filter Crop:": "फसल फ़िल्टर करें:",
    "All Crops": "सभी फसलें",
    "Back to Diagnosis": "निदान पर वापस जाएं",
    "Recovery Tracker (Before vs After)": "सुधार ट्रैकर (उपचार से पहले बनाम बाद में)",
    "Before Treatment": "उपचार से पहले",
    "After Treatment": "उपचार के बाद",
    "Farmer Recovery Notes:": "किसान की सुधार संबंधी टिप्पणियां:",
    "Possible Reasons": "संभावित कारण",
    "Track Treatment Success": "उपचार की सफलता ट्रैक करें",
    "Have you applied the recommended treatment? Upload a follow-up photo to track recovery progress and see before-vs-after status.":
      "क्या आपने अनुशंसित उपचार लागू किया है? सुधार की प्रगति ट्रैक करने के लिए एक अनुवर्ती तस्वीर अपलोड करें।",
    "Follow-up Image": "अनुवर्ती तस्वीर",
    "Recovery Observations": "सुधार अवलोकन",
    "Describe the crop health now (e.g., spots disappearing, new leaves sprouting, yellowing reduced)":
      "अब फसल के स्वास्थ्य का वर्णन करें (जैसे धब्बे गायब होना, नई पत्तियां निकलना, पीलापन कम होना)",
    "Update Recovery Status": "सुधार स्थिति अपडेट करें",
    "Uploading...": "अपलोड हो रहा है...",
    "Prediction Not Found": "पूर्वानुमान नहीं मिला",
    "The prediction you're looking for doesn't exist.": "आप जिस पूर्वानुमान की तलाश कर रहे हैं वह मौजूद नहीं है।",
    "Our agronomist is currently reviewing this prediction. The diagnosis below is locked until verified.":
      "हमारे कृषि विज्ञानी वर्तमान में इस निदान की समीक्षा कर रहे हैं। सत्यापन तक नीचे का विवरण सुरक्षित है।",
    "Regional Outbreak Surveillance": "क्षेत्रीय प्रकोप निगरानी",
    "Aggregated anonymized crop disease detections to protect neighboring farmers within a 25km perimeter.":
      "25 किमी के दायरे में पड़ोसी किसानों की सुरक्षा के लिए फसल रोग का पता लगाने का सामूहिक डेटा।",
    "Alert": "चेतावनी",
    "Active Cases": "सक्रिय मामले",
    "fields": "खेत",
    "Warning Radius": "चेतावनी दायरा",
    "Trend": "प्रवृत्ति",
    "Coordinates": "निर्देशांक",
    "Preventive Action Advisory": "निवारक कार्रवाई सलाह",
    "Spreading": "फैल रहा है",
    "Contained": "नियंत्रित",
    "Stable": "स्थिर",
  },
  te: {
    "Upload": "అప్‌లోడ్",
    "History": "చరిత్ర",
    "Analytics": "విశ్లేషణలు",
    "Outbreak Radar": "తెగుళ్ల రాడార్",
    "Crop Disease Diagnosis": "పంట తెగులు నిర్ధారణ",
    "Upload a photo of your crop and our AI will analyze it for potential diseases, providing severity assessment and treatment recommendations.":
      "మీ పంట ఫోటోను అప్‌లోడ్ చేయండి. మా AI దానిని సంభావ్య తెగుళ్ల కోసం విశ్లేషించి, తీవ్రత అంచనా మరియు చికిత్స సిఫార్సులను అందిస్తుంది.",
    "Secure file handling": "సురక్షిత ఫైల్ హ్యాండ్లింగ్",
    "Instant AI analysis": "తక్షణ AI విశ్లేషణ",
    "8+ crop types": "8+ పంట రకాలు",
    "Crop Type": "పంట రకం",
    "Select a crop": "పంటను ఎంచుకోండి",
    "Farmer Notes": "రైతు గమనికలు",
    "Describe what you see (e.g., yellow spots, wilting)": "మీరు గమనించిన వివరాలు (ఉదా. పసుపు మచ్చలు, ఆకులు ముడుచుకోవడం)",
    "AI Model": "AI మోడల్",
    "Upload Image": "చిత్రాన్ని అప్‌లోడ్ చేయండి",
    "Analyzing...": "విశ్లేషిస్తోంది...",
    "Diagnosis Result": "నిర్ధారణ ఫలితం",
    "Confidence": "నమ్మకశాతం",
    "Severity": "తీవ్రత",
    "Treatment Recommendation": "చికిత్స సిఫార్సు",
    "Verified Advisory": "ధృవీకరించబడిన సలహా",
    "Pending Review": "సమీక్ష పెండింగ్‌లో ఉంది",
    "Verified": "ధృవీకరించబడింది",
    "Logout": "లాగ్అవుట్",
    "Login": "లాగిన్",
    "Username": "యూజర్ నేమ్",
    "Password": "పాస్‌వర్డ్",
    "Register": "నమోదు",
    "Agronomist Portal": "నిపుణుల పోర్టల్",
    "Pending Requests": "సమీక్ష కోసం వేచి ఉన్న అభ్యర్థనలు",
    "Submit Review": "సమీక్షను సమర్పించండి",
    "Confirm Diagnosis": "తెగులును ధృవీకరించండి",
    "Verified Disease Name": "ధృవీకరించబడిన తెగులు పేరు",
    "Verified Severity": "ధృవీకరించబడిన తీవ్రత",
    "Advisory Notes / Treatment": "సలహా గమనికలు / చికిత్స",
    "Please log in to use Krishi Clinic.": "దయచేసి కరిషి క్లినిక్ ఉపయోగించడానికి లాగిన్ చేయండి.",
    "Login Credentials": "లాగిన్ వివరాలు",
    "Farmer Profile": "రైతు ప్రొఫైల్",
    "Agronomist Profile": "వ్యవసాయ నిపుణుల ప్రొఫైల్",
    "Select Role": "పాత్రను ఎంచుకోండి",
    "Create Account": "ఖాతా సృష్టించండి",
    "Already have an account? Login": "ఖాతా ఉందా? లాగిన్ అవ్వండి",
    "Don't have an account? Register": "ఖాతా లేదా? నమోదు చేసుకోండి",
    "Error": "లోపం",
    "Success": "విజయం",
    "History List": "చరిత్ర జాబితా",
    "No predictions found.": "ఎలాంటి ఫలితాలు లేవు.",
    "Export CSV": "CSV ఎగుమతి",
    "Back to History": "చరిత్రకు తిరిగి వెళ్ళండి",
    "Analyzed on": "విశ్లేషించిన తేదీ",
    "AI Provider": "AI ప్రదాత",
    "Farmer Observations": "రైతు గమనింపులు",
    "Status": "స్థితి",
    "Low": "తక్కువ",
    "Medium": "మధ్యస్థం",
    "High": "ఎక్కువ",
    "Date": "తేది",
    "Crop": "పంట",
    "Disease": "తెగులు",
    "Provider": "ప్రదాత",
    "View": "చూడండి",
    "All crops": "అన్ని పంటలు",
    "Filter by disease...": "తెగులు ద్వారా వడపోత...",
    "Clear Filters": "ఫిల్టర్లను తీసివేయి",
    "Previous": "మునుపటి",
    "Next": "తదుపరి",
    "Page": "పేజీ",
    "Showing": "చూపిస్తోంది",
    "of": "లో",
    "predictions": "అంచనాలు",
    "PENDING": "పెండింగ్",
    "PENDING_REVIEW": "సమీక్ష పెండింగ్",
    "REVIEWED": "ధృవీకరించబడింది",
    "Wheat": "గోధుమ",
    "Rice": "వరి",
    "Tomato": "టమోటా",
    "Corn": "మొక్కజొన్న",
    "Potato": "బంగాళాదుంప",
    "Cotton": "పత్తి",
    "Sugarcane": "చెరకు",
    "Soybean": "సోయాబీన్",
    "Mustard": "ఆవాలు",
    "Groundnut": "వేరుశనగ",
    "Chilli": "మిరపకాయ",
    "mock": "Mock (టెస్ట్)",
    "local": "Local PyTorch (స్థానిక మోడల్)",
    "gemini": "Google Gemini",
    "groq": "Groq Llama 4",
    "openai": "OpenAI GPT",
    "Hidden": "దాచబడింది",
    "Healthy": "ఆరోగ్యకరమైనది",
    "Voice Advisory": "వాయిస్ సలహా",
    "Export PDF Advisory": "PDF సలహాను డౌన్‌లోడ్ చేయండి",
    "Exporting...": "ఎగుమతి చేస్తోంది...",
    "Active Disease Clusters": "క్రియాశీల తెగులు క్లస్టర్లు",
    "High Risk Areas": "అధిక ప్రమాద ప్రాంతాలు",
    "Monitored Field Cases": "పర్యవేక్షించబడుతున్న కేసులు",
    "Early Warning Protocol": "ముందస్తు హెచ్చరిక ప్రోటోకాల్",
    "Active (25km Radius)": "క్రియాశీలం (25 కిమీ పరిధి)",
    "Subscribe to Village Outbreak SMS Alerts": "గ్రామ తెగుళ్ల SMS హెచ్చరికలకు సభ్యత్వాన్ని పొందండి",
    "Receive automated SMS warnings when crop diseases are identified on neighboring plots within your radius.":
      "మీ పరిధిలోని పొరుగు పొలాల్లో పంట తెగుళ్లు గుర్తించినప్పుడు ఆటోమేటిక్ SMS హెచ్చరికలను పొందండి.",
    "Enter mobile number": "మొబైల్ నంబర్ నమోదు చేయండి",
    "Enable Proximity Warnings": "హెచ్చరికలను ప్రారంభించండి",
    "Proximity alert subscription enabled successfully.": "హెచ్చరికల సభ్యత్వం విజయవంతంగా ప్రారంభించబడింది.",
    "Active Regional Infestation Clusters": "ప్రాంతీయ తెగుళ్ల క్లస్టర్లు",
    "Filter Crop:": "పంట వడపోత:",
    "All Crops": "అన్ని పంటలు",
    "Back to Diagnosis": "నిర్ధారణకు తిరిగి వెళ్ళండి",
    "Recovery Tracker (Before vs After)": "కోలుకునే ట్రాకర్ (చికిత్సకు ముందు vs తర్వాత)",
    "Before Treatment": "చికిత్సకు ముందు",
    "After Treatment": "చికిత్స తర్వాత",
    "Farmer Recovery Notes:": "రైతు రికవరీ గమనికలు:",
    "Possible Reasons": "సంభావ్య కారణాలు",
    "Track Treatment Success": "చికిత్స విజయాన్ని ట్రాక్ చేయండి",
    "Have you applied the recommended treatment? Upload a follow-up photo to track recovery progress and see before-vs-after status.":
      "మీరు సిఫార్సు చేసిన చికిత్సను అందించారా? పురోగతిని చూడటానికి ఫాలో-అప్ ఫోటోను అప్‌లోడ్ చేయండి.",
    "Follow-up Image": "ఫాలో-అప్ చిత్రం",
    "Recovery Observations": "కోలుకుంటున్న పరిశీలనలు",
    "Describe the crop health now (e.g., spots disappearing, new leaves sprouting, yellowing reduced)":
      "పంట ఆరోగ్యాన్ని వివరించండి (ఉదా. మచ్చలు తగ్గడం, కొత్త ఆకులు రావడం)",
    "Update Recovery Status": "స్థితిని అప్‌డేట్ చేయండి",
    "Uploading...": "అప్‌లోడ్ అవుతోంది...",
    "Prediction Not Found": "ఫలితం కనుగొనబడలేదు",
    "The prediction you're looking for doesn't exist.": "మీరు వెతుకుతున్న అంచనా ఫలితం అందుబాటులో లేదు.",
    "Our agronomist is currently reviewing this prediction. The diagnosis below is locked until verified.":
      "మా వ్యవసాయ నిపుణులు ప్రస్తుతం ఈ అంచనాను సమీక్షిస్తున్నారు. ధృవీకరించబడే వరకు క్రింది సమాచారం లాక్ చేయబడింది.",
    "Regional Outbreak Surveillance": "ప్రాంతీయ తెగుళ్ల నిఘా",
    "Aggregated anonymized crop disease detections to protect neighboring farmers within a 25km perimeter.":
      "25 కి.మీ పరిధిలోని పొరుగు రైతులను రక్షించడానికి పంట తెగుళ్ల గుర్తింపు సమాచారం.",
    "Alert": "హెచ్చరిక",
    "Active Cases": "క్రియాశీల కేసులు",
    "fields": "పొలాలు",
    "Warning Radius": "హెచ్చరిక పరిధి",
    "Trend": "ధోరణి",
    "Coordinates": "కోఆర్డినేట్లు",
    "Preventive Action Advisory": "నివారణ చర్య సలహా",
    "Spreading": "వ్యాపిస్తోంది",
    "Contained": "నియంత్రించబడింది",
    "Stable": "స్థిరంగా ఉంది",
  },
  mr: {
    "Upload": "अपलोड करा",
    "History": "इतिहास",
    "Analytics": "विश्लेषण",
    "Outbreak Radar": "रोग प्रादुर्भाव रडार",
    "Crop Disease Diagnosis": "पिकांचे रोग निदान",
    "Upload a photo of your crop and our AI will analyze it for potential diseases, providing severity assessment and treatment recommendations.":
      "तुमच्या पिकाचा फोटो अपलोड करा. आमचे AI संभाव्य रोगांसाठी याचे विश्लेषण करेल आणि तीव्रता तसेच उपचारांची शिफारस करेल.",
    "Secure file handling": "सुरक्षित फाईल हाताळणी",
    "Instant AI analysis": "झटपट AI विश्लेषण",
    "8+ crop types": "८+ पिकांचे प्रकार",
    "Crop Type": "पिकाचा प्रकार",
    "Select a crop": "पीक निवडा",
    "Farmer Notes": "शेतकऱ्याची नोंद",
    "Describe what you see (e.g., yellow spots, wilting)": "तुम्हाला काय दिसते ते लिहा (उदा. पिवळे डाग, कोमेजणे)",
    "AI Model": "AI मॉडेल",
    "Upload Image": "प्रतिमा अपलोड करा",
    "Analyzing...": "विश्लेषण करत आहे...",
    "Diagnosis Result": "निदानाचे निकाल",
    "Confidence": "विश्वासार्हता",
    "Severity": "तीव्रता",
    "Treatment Recommendation": "उपचार शिफारस",
    "Verified Advisory": "सत्यापित कृषी सल्ला",
    "Pending Review": "पुनरावलोकन प्रलंबित",
    "Verified": "सत्यापित",
    "Logout": "लॉगआउट",
    "Login": "लॉगिन",
    "Username": "वापरकर्तानाव",
    "Password": "पासवर्ड",
    "Register": "नोंदणी",
    "Agronomist Portal": "कृषी तज्ज्ञ पोर्टल",
    "Pending Requests": "प्रलंबित विनंत्या",
    "Submit Review": "पुनरावलोकन सादर करा",
    "Confirm Diagnosis": "निदानाची पुष्टी करा",
    "Verified Disease Name": "सत्यापित रोगाचे नाव",
    "Verified Severity": "सत्यापित तीव्रता",
    "Advisory Notes / Treatment": "कृषी सल्ला / उपचार",
    "Please log in to use Krishi Clinic.": "कृपया कृषी क्लिनिक वापरण्यासाठी लॉगिन करा.",
    "Login Credentials": "लॉगिन क्रेडेंशियल",
    "Farmer Profile": "शेतकरी प्रोफाइल",
    "Agronomist Profile": "कृषी तज्ज्ञ प्रोफाइल",
    "Select Role": "भूमिका निवडा",
    "Create Account": "खाते तयार करा",
    "Already have an account? Login": "आधीच खाते आहे? लॉगिन करा",
    "Don't have an account? Register": "खाते नाही? नोंदणी करा",
    "Error": "त्रुटी",
    "Success": "यशस्वी",
    "History List": "इतिहास सूची",
    "No predictions found.": "कोणतीही नोंद आढळली नाही.",
    "Export CSV": "CSV निर्यात",
    "Back to History": "इतिहासाकडे परत जा",
    "Analyzed on": "विश्लेषण तारीख",
    "AI Provider": "AI प्रदाता",
    "Farmer Observations": "शेतकऱ्याचे निरीक्षण",
    "Status": "स्थिती",
    "Low": "कमी",
    "Medium": "मध्यम",
    "High": "जास्त",
    "Date": "तारीख",
    "Crop": "पीक",
    "Disease": "रोग",
    "Provider": "प्रदाता",
    "View": "पहा",
    "All crops": "सर्व पिके",
    "Filter by disease...": "रोगाने फिल्टर करा...",
    "Clear Filters": "फिल्टर साफ करा",
    "Previous": "मागील",
    "Next": "पुढील",
    "Page": "पान",
    "Showing": "दाखवत आहे",
    "of": "पैकी",
    "predictions": "अंदाज",
    "PENDING": "प्रलंबित",
    "PENDING_REVIEW": "पुनरावलोकन प्रलंबित",
    "REVIEWED": "सत्यापित",
    "Wheat": "गहू",
    "Rice": "तांदूळ",
    "Tomato": "टोमॅटो",
    "Corn": "मका",
    "Potato": "बटाटा",
    "Cotton": "कापूस",
    "Sugarcane": "ऊस",
    "Soybean": "सोयाबीन",
    "Mustard": "मोहरी",
    "Groundnut": "भुईमूग",
    "Chilli": "मिरची",
    "mock": "Mock (चाचणी)",
    "local": "Local PyTorch (स्थानिक मॉडेल)",
    "gemini": "Google Gemini",
    "groq": "Groq Llama 4",
    "openai": "OpenAI GPT",
    "Hidden": "लपवलेले",
    "Healthy": "निरोगी",
    "Voice Advisory": "व्हॉईस सल्ला",
    "Export PDF Advisory": "PDF सल्ला डाउनलोड करा",
    "Exporting...": "निर्यात करत आहे...",
    "Active Disease Clusters": "सक्रिय रोग क्लस्टर",
    "High Risk Areas": "अति धोक्याचे क्षेत्र",
    "Monitored Field Cases": "निरीक्षणातील शेत प्रकरणे",
    "Early Warning Protocol": "पूर्व चेतावणी प्रोटोकॉल",
    "Active (25km Radius)": "सक्रिय (२५ किमी परीघ)",
    "Subscribe to Village Outbreak SMS Alerts": "गाव पातळीवरील रोग प्रादुर्भाव SMS अलर्ट मिळवा",
    "Receive automated SMS warnings when crop diseases are identified on neighboring plots within your radius.":
      "तुमच्या परिसरातील लगतच्या शेतात पिकांचे रोग आढळल्यास स्वयंचलित SMS चेतावणी मिळवा.",
    "Enter mobile number": "मोबाईल नंबर टाका",
    "Enable Proximity Warnings": "परिसर चेतावणी सुरू करा",
    "Proximity alert subscription enabled successfully.": "चेतावणी सेवा यशस्वीरीत्या सुरू करण्यात आली आहे.",
    "Active Regional Infestation Clusters": "सक्रिय प्रादेशिक रोग क्लस्टर",
    "Filter Crop:": "पीक फिल्टर:",
    "All Crops": "सर्व पिके",
    "Back to Diagnosis": "निदानाकडे परत जा",
    "Recovery Tracker (Before vs After)": "सुधारणा ट्रॅकर (उपचारापूर्वी vs नंतर)",
    "Before Treatment": "उपचारापूर्वी",
    "After Treatment": "उपचारानंतर",
    "Farmer Recovery Notes:": "शेतकऱ्याची सुधारणा नोंद:",
    "Possible Reasons": "संभाव्य कारणे",
    "Track Treatment Success": "उपचाराचे यश ट्रॅक करा",
    "Have you applied the recommended treatment? Upload a follow-up photo to track recovery progress and see before-vs-after status.":
      "तुम्ही शिफारस केलेले उपचार केले आहेत का? प्रगती पाहण्यासाठी नवीन फोटो अपलोड करा.",
    "Follow-up Image": "नवीन फोटो",
    "Recovery Observations": "सुधारणा निरीक्षण",
    "Describe the crop health now (e.g., spots disappearing, new leaves sprouting, yellowing reduced)":
      "आता पिकाच्या आरोग्याचे वर्णन करा (उदा. डाग कमी झाले, नवीन पालवी फुटली)",
    "Update Recovery Status": "स्थिती अपडेट करा",
    "Uploading...": "अपलोड होत आहे...",
    "Prediction Not Found": "नोंद आढळली नाही",
    "The prediction you're looking for doesn't exist.": "आपण शोधत असलेली नोंद अस्तित्वात नाही.",
    "Our agronomist is currently reviewing this prediction. The diagnosis below is locked until verified.":
      "आमचे कृषी तज्ज्ञ सध्या या अंदाजाचे पुनरावलोकन करत आहेत. पडताळणी होईपर्यंत खालील माहिती सुरक्षित आहे.",
    "Regional Outbreak Surveillance": "प्रादेशिक रोग प्रादुर्भाव देखरेख",
    "Aggregated anonymized crop disease detections to protect neighboring farmers within a 25km perimeter.":
      "२५ किमी परिघातील शेतकर्‍यांच्या संरक्षणासाठी पिकांवरील रोगांची एकत्रित माहिती.",
    "Alert": "इशारा",
    "Active Cases": "सक्रिय प्रकरणे",
    "fields": "शेते",
    "Warning Radius": "इशारा परीघ",
    "Trend": "कल",
    "Coordinates": "निर्देशांक",
    "Preventive Action Advisory": "प्रतिबंधात्मक कृती सल्ला",
    "Spreading": "पसरत आहे",
    "Contained": "नियंत्रित",
    "Stable": "स्थिर",
  },
  es: {
    "Upload": "Subir",
    "History": "Historial",
    "Analytics": "Analítica",
    "Outbreak Radar": "Radar de Brotes",
    "Crop Disease Diagnosis": "Diagnóstico de Enfermedades",
    "Upload a photo of your crop and our AI will analyze it for potential diseases, providing severity assessment and treatment recommendations.":
      "Suba una foto de su cultivo y nuestra IA la analizará en busca de posibles enfermedades, proporcionando evaluación de severidad y recomendaciones de tratamiento.",
    "Secure file handling": "Manejo seguro de archivos",
    "Instant AI analysis": "Análisis de IA instantáneo",
    "8+ crop types": "8+ tipos de cultivos",
    "Crop Type": "Tipo de cultivo",
    "Select a crop": "Seleccione un cultivo",
    "Farmer Notes": "Notas del agricultor",
    "Describe what you see (e.g., yellow spots, wilting)": "Describa lo que observa (ej. manchas amarillas, marchitamiento)",
    "AI Model": "Modelo IA",
    "Upload Image": "Subir Imagen",
    "Analyzing...": "Analizando...",
    "Diagnosis Result": "Resultado de diagnóstico",
    "Confidence": "Confianza",
    "Severity": "Severidad",
    "Treatment Recommendation": "Recomendación de tratamiento",
    "Verified Advisory": "Asesoramiento verificado",
    "Pending Review": "Revisión pendiente",
    "Verified": "Verificado",
    "Logout": "Cerrar sesión",
    "Login": "Iniciar sesión",
    "Username": "Usuario",
    "Password": "Contraseña",
    "Register": "Registrarse",
    "Agronomist Portal": "Portal de Agrónomos",
    "Pending Requests": "Solicitudes pendientes",
    "Submit Review": "Enviar revisión",
    "Confirm Diagnosis": "Confirmar diagnóstico",
    "Verified Disease Name": "Nombre verificado de la enfermedad",
    "Verified Severity": "Severidad verificada",
    "Advisory Notes / Treatment": "Notas de asesoría / Tratamiento",
    "Please log in to use Krishi Clinic.": "Inicie sesión para utilizar Krishi Clinic.",
    "Login Credentials": "Credenciales de inicio de sesión",
    "Farmer Profile": "Perfil de Agricultor",
    "Agronomist Profile": "Perfil de Agrónomo",
    "Select Role": "Seleccionar rol",
    "Create Account": "Crear cuenta",
    "Already have an account? Login": "¿Ya tiene cuenta? Iniciar sesión",
    "Don't have an account? Register": "¿No tiene cuenta? Registrarse",
    "Error": "Error",
    "Success": "Éxito",
    "History List": "Lista de Historial",
    "No predictions found.": "No se encontraron predicciones.",
    "Export CSV": "Exportar CSV",
    "Back to History": "Volver al Historial",
    "Analyzed on": "Analizado el",
    "AI Provider": "Proveedor de IA",
    "Farmer Observations": "Observaciones del agricultor",
    "Status": "Estado",
    "Low": "Bajo",
    "Medium": "Medio",
    "High": "Alto",
    "Date": "Fecha",
    "Crop": "Cultivo",
    "Disease": "Enfermedad",
    "Provider": "Proveedor",
    "View": "Ver",
    "All crops": "Todos los cultivos",
    "Filter by disease...": "Filtrar por enfermedad...",
    "Clear Filters": "Borrar filtros",
    "Previous": "Anterior",
    "Next": "Siguiente",
    "Page": "Página",
    "Showing": "Mostrando",
    "of": "de",
    "predictions": "predicciones",
    "PENDING": "PENDIENTE",
    "PENDING_REVIEW": "REVISIÓN PENDIENTE",
    "REVIEWED": "VERIFICADO",
    "Wheat": "Trigo",
    "Rice": "Arroz",
    "Tomato": "Tomate",
    "Corn": "Maíz",
    "Potato": "Papa",
    "Cotton": "Algodón",
    "Sugarcane": "Caña de azúcar",
    "Soybean": "Soja",
    "Mustard": "Mostaza",
    "Groundnut": "Maní",
    "Chilli": "Chile",
    "mock": "Mock (Prueba)",
    "local": "Local PyTorch (Modelo local)",
    "gemini": "Google Gemini",
    "groq": "Groq Llama 4",
    "openai": "OpenAI GPT",
    "Hidden": "Oculto",
    "Healthy": "Saludable",
    "Voice Advisory": "Asesoría por voz",
    "Export PDF Advisory": "Descargar PDF de asesoría",
    "Exporting...": "Exportando...",
    "Active Disease Clusters": "Brotes activos",
    "High Risk Areas": "Zonas de alto riesgo",
    "Monitored Field Cases": "Casos monitoreados",
    "Early Warning Protocol": "Protocolo de alerta temprana",
    "Active (25km Radius)": "Activo (Radio de 25 km)",
    "Subscribe to Village Outbreak SMS Alerts": "Suscribirse a alertas SMS de brotes locales",
    "Receive automated SMS warnings when crop diseases are identified on neighboring plots within your radius.":
      "Reciba alertas automáticas por SMS cuando se identifiquen enfermedades en parcelas vecinas dentro de su radio.",
    "Enter mobile number": "Ingrese número de móvil",
    "Enable Proximity Warnings": "Activar alertas de proximidad",
    "Proximity alert subscription enabled successfully.": "Suscripción a alertas de proximidad activada con éxito.",
    "Active Regional Infestation Clusters": "Brotes regionales activos",
    "Filter Crop:": "Filtrar cultivo:",
    "All Crops": "Todos los cultivos",
    "Back to Diagnosis": "Volver al Diagnóstico",
    "Recovery Tracker (Before vs After)": "Seguimiento de recuperación (Antes vs Después)",
    "Before Treatment": "Antes del tratamiento",
    "After Treatment": "Después del tratamiento",
    "Farmer Recovery Notes:": "Notas de recuperación del agricultor:",
    "Possible Reasons": "Posibles causas",
    "Track Treatment Success": "Seguimiento del tratamiento",
    "Have you applied the recommended treatment? Upload a follow-up photo to track recovery progress and see before-vs-after status.":
      "¿Ha aplicado el tratamiento recomendado? Suba una foto de seguimiento para ver el progreso antes y después.",
    "Follow-up Image": "Foto de seguimiento",
    "Recovery Observations": "Observaciones de recuperación",
    "Describe the crop health now (e.g., spots disappearing, new leaves sprouting, yellowing reduced)":
      "Describa el estado actual del cultivo (ej. manchas desapareciendo, nuevos brotes, menos amarillamiento)",
    "Update Recovery Status": "Actualizar estado de recuperación",
    "Uploading...": "Subiendo...",
    "Prediction Not Found": "Predicción no encontrada",
    "The prediction you're looking for doesn't exist.": "La predicción que busca no existe.",
    "Our agronomist is currently reviewing this prediction. The diagnosis below is locked until verified.":
      "Nuestro agrónomo está revisando actualmente esta predicción. El diagnóstico a continuación está bloqueado hasta su verificación.",
    "Regional Outbreak Surveillance": "Vigilancia Regional de Brotes",
    "Aggregated anonymized crop disease detections to protect neighboring farmers within a 25km perimeter.":
      "Detecciones agregadas y anónimas para proteger a los agricultores vecinos en un radio de 25 km.",
    "Alert": "Alerta",
    "Active Cases": "Casos activos",
    "fields": "campos",
    "Warning Radius": "Radio de advertencia",
    "Trend": "Tendencia",
    "Coordinates": "Coordenadas",
    "Preventive Action Advisory": "Asesoramiento de acción preventiva",
    "Spreading": "En propagación",
    "Contained": "Contenido",
    "Stable": "Estable",
  },
};

// Merge common disease translations into STATIC_TRANSLATIONS for fast lookup
const STATIC_TRANSLATIONS: Record<string, Record<string, string>> = {
  hi: { ...BASE_STATIC_TRANSLATIONS.hi },
  te: { ...BASE_STATIC_TRANSLATIONS.te },
  mr: { ...BASE_STATIC_TRANSLATIONS.mr },
  es: { ...BASE_STATIC_TRANSLATIONS.es },
};

for (const [disease, langMap] of Object.entries(COMMON_DISEASES)) {
  for (const [lang, val] of Object.entries(langMap)) {
    if (STATIC_TRANSLATIONS[lang]) {
      STATIC_TRANSLATIONS[lang][disease] = val;
      STATIC_TRANSLATIONS[lang][disease.toLowerCase()] = val;
    }
  }
}

function parseJwt(token: string) {
  try {
    const base64Url = token.split(".")[1];
    const base64 = base64Url.replace(/-/g, "+").replace(/_/g, "/");
    const jsonPayload = decodeURIComponent(
      atob(base64)
        .split("")
        .map((c) => "%" + ("00" + c.charCodeAt(0).toString(16)).slice(-2))
        .join("")
    );
    const parsed = JSON.parse(jsonPayload);
    return {
      id: parsed.sub,
      username: parsed.username,
      role: parsed.role,
    };
  } catch (e) {
    return null;
  }
}

export function AppProvider({ children }: { children: React.ReactNode }) {
  const [user, setUser] = useState<UserProfile | null>(null);
  const [language, setLanguageState] = useState<string>("en");
  const [isInitialized, setIsInitialized] = useState<boolean>(false);

  useEffect(() => {
    const storedToken = localStorage.getItem("token");
    const storedLang = localStorage.getItem("lang") || "en";
    
    setLanguageState(storedLang);

    if (storedToken) {
      const decoded = parseJwt(storedToken);
      if (decoded) {
        setUser({
          id: decoded.id,
          username: decoded.username,
          role: decoded.role as "FARMER" | "AGRONOMIST" | "ADMIN",
          token: storedToken,
        });
      } else {
        localStorage.removeItem("token");
      }
    }
    setIsInitialized(true);
  }, []);

  const login = (token: string) => {
    localStorage.setItem("token", token);
    const decoded = parseJwt(token);
    if (decoded) {
      setUser({
        id: decoded.id,
        username: decoded.username,
        role: decoded.role as "FARMER" | "AGRONOMIST" | "ADMIN",
        token: token,
      });
    }
  };

  const logout = () => {
    localStorage.removeItem("token");
    setUser(null);
  };

  const setLanguage = (lang: string) => {
    localStorage.setItem("lang", lang);
    setLanguageState(lang);
  };

  const t = (key: string): string => {
    if (!key || language === "en") return key;
    const trans = STATIC_TRANSLATIONS[language];
    if (trans) {
      if (trans[key]) return trans[key];
      const trimmed = key.trim();
      if (trans[trimmed]) return trans[trimmed];
      const lower = trimmed.toLowerCase();
      if (trans[lower]) return trans[lower];
    }
    return key;
  };

  const translateDynamic = async (text: string): Promise<string> => {
    if (!text || language === "en") return text;
    
    // Fast dictionary check first
    const staticRes = t(text);
    if (staticRes && staticRes !== text) {
      return staticRes;
    }

    try {
      const apiBase = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";
      const resp = await fetch(`${apiBase}/api/v1/translate`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          text: text,
          target_language: language,
        }),
      });
      if (resp.ok) {
        const data = await resp.json();
        return data.translated_text || text;
      }
    } catch (e) {
      console.error("Dynamic translation error", e);
    }
    return text;
  };

  return (
    <AppContext.Provider
      value={{
        user,
        language,
        isInitialized,
        t,
        translateDynamic,
        login,
        logout,
        setLanguage,
      }}
    >
      {children}
    </AppContext.Provider>
  );
}

export function useApp() {
  const context = useContext(AppContext);
  if (context === undefined) {
    throw new Error("useApp must be used within an AppProvider");
  }
  return context;
}

export function Translate({ text }: { text: string }) {
  const { language, translateDynamic, t } = useApp();
  const [translated, setTranslated] = useState(text);

  useEffect(() => {
    let active = true;

    const staticTrans = t(text);
    if (staticTrans !== text) {
      setTranslated(staticTrans);
      return;
    }

    if (language === "en" || !text) {
      setTranslated(text);
      return;
    }

    translateDynamic(text).then((res) => {
      if (active) setTranslated(res);
    });

    return () => {
      active = false;
    };
  }, [text, language, t, translateDynamic]);

  return <>{translated}</>;
}
