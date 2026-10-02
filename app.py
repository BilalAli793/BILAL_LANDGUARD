import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import streamlit as st
from geopy.geocoders import Nominatim
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Bilal’s Sentinel",
    page_icon="⚠️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ====================== SESSION STATE ======================
if "show_intro" not in st.session_state:
    st.session_state.show_intro = True
if "predicted" not in st.session_state:
    st.session_state.predicted = False
if "prediction" not in st.session_state:
    st.session_state.prediction = None
if "probability" not in st.session_state:
    st.session_state.probability = 0
if "lat" not in st.session_state:
    st.session_state.lat = None
if "lon" not in st.session_state:
    st.session_state.lon = None
if "loc_name" not in st.session_state:
    st.session_state.loc_name = ""

# ====================== INTRO PAGE ======================
if st.session_state.show_intro:

    st.markdown("""
        <style>
        header {visibility: hidden;}
        footer {visibility: hidden;}
        #MainMenu {visibility: hidden;}
        .stApp { background: #0b0f1a; }

        .intro-wrapper {
            position: relative;
            width: 100%;
            margin: 0 auto;
            overflow: hidden;
            border-radius: 12px;
            background: #000;
        }
        .intro-video {
            width: 100%;
            height: 55vh;
            object-fit: cover;
            display: block;
        }
        .intro-overlay {
            position: absolute;
            top: 0; left: 0;
            width: 100%; height: 100%;
            background: linear-gradient(to bottom, rgba(0,0,0,0.55) 0%, rgba(0,0,0,0.25) 40%, rgba(0,0,0,0.7) 100%);
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            text-align: center;
            padding: 1.5rem;
            box-sizing: border-box;
        }
        .intro-title {
            font-size: 2.6rem;
            font-weight: 800;
            background: linear-gradient(90deg, #ff6b35, #f7c948);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin: 0 0 0.4rem 0;
            line-height: 1.2;
        }
        .intro-sub {
            font-size: 1.15rem;
            color: #e8ecf4;
            margin: 0 0 0.8rem 0;
            font-weight: 500;
        }
        .intro-tagline {
            font-size: 0.95rem;
            color: #b0b8c8;
            max-width: 420px;
            line-height: 1.5;
            margin: 0;
        }
        @media (max-width: 600px) {
            .intro-title { font-size: 1.9rem; }
            .intro-sub { font-size: 1rem; }
            .intro-video { height: 45vh; }
        }
        </style>
    """, unsafe_allow_html=True)

    st.markdown("""
        <div class="intro-wrapper">
            <video class="intro-video" autoplay muted loop playsinline>
                <source src="https://raw.githubusercontent.com/BilalAli793/BILAL_LANDGUARD/main/landslide_intro.mp4" type="video/mp4">
            </video>
            <div class="intro-overlay">
                <div class="intro-title">⚠️ Bilal’s Sentinel</div>
                <div class="intro-sub">AI Landslide Early Warning System</div>
                <div class="intro-tagline">
                    Where the most relevant data is provided to alert you<br>
                    before disaster strikes.
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1.2, 2, 1.2])
    with col2:
        if st.button("🚀 Enter App  —  Skip Intro", use_container_width=True, type="primary"):
            st.session_state.show_intro = False
            st.rerun()

    st.markdown("""
        <p style="text-align:center; color:#6a7385; font-size:0.85rem; margin-top:1rem;">
            Developed by Bilal Ali  |  CSE, KMCLU  |  SIH 2026
        </p>
    """, unsafe_allow_html=True)
    st.stop()

# ====================== TRANSLATIONS ======================
translations = {
    "English": {
        "app_title": "⚠️ Bilal’s Sentinel",
        "app_sub": "AI Landslide Early Warning System | By Bilal Ali",
        "nav_home": "🏠 Home",
        "nav_risk": "🔍 Risk Prediction",
        "nav_safety": "🛡️ Safety Guidelines",
        "nav_emergency": "🚨 Emergency Actions",
        "home_title": "⚠️ Bilal’s Sentinel",
        "home_sub": "AI-Powered Landslide Early Warning System",
        "home_by": "By Bilal Ali | CSE Department, KMCLU",
        "home_card1": "📍 **Location Based**\n\nEnter any place and get risk analysis with Google Map.",
        "home_card2": "🤖 **AI Prediction**\n\nRandom Forest model using rainfall, slope, moisture & elevation.",
        "home_card3": "🔊 **Voice + Guidance**\n\nSpoken alerts and clear safety instructions.",
        "home_why": "### Why this system?",
        "home_why_text": "Every year landslides cause loss of life and property in hilly regions of India (Uttarakhand, Himachal, Northeast, Western Ghats). An early warning system can help save lives.",
        "home_how": "### How to use",
        "home_how_text": "1. Go to **Risk Prediction** page\n2. Enter a location\n3. Adjust parameters\n4. Click Predict\n5. See result + Google Map + guidance",
        "home_go": "👉 Open **Risk Prediction** from the left sidebar.",
        "location": "📍 Enter Location",
        "placeholder": "Example: Gangtok, Darjeeling, Manali, Shimla",
        "params": "🔢 Environmental Parameters",
        "rainfall": "🌧️ Rainfall (mm)",
        "slope": "📐 Slope Angle (degrees)",
        "moisture": "💧 Soil Moisture (0-1)",
        "elevation": "⛰️ Elevation (meters)",
        "button": "🔍 Predict Risk & Show Map",
        "result": "📊 Prediction Result",
        "high_risk": "🚨 HIGH RISK of Landslide Detected",
        "low_risk": "✅ LOW RISK — Situation Currently Stable",
        "probability": "Risk Probability",
        "actions": "Immediate Actions",
        "action1": "Evacuate people from steep slopes and low-lying areas",
        "action2": "Inform local District Disaster Management Authority",
        "action3": "Avoid travel on hilly roads",
        "action4": "Continuously monitor rainfall",
        "status": "Current Status",
        "status1": "Conditions are within safe limits",
        "status2": "Continue regular monitoring",
        "status3": "Stay alert during heavy rainfall",
        "map": "🗺️ Location Map (Google Maps)",
        "map_info": "Enter a valid location name to see the map.",
        "voice_danger": "Warning! High risk of landslide detected. Please take immediate action.",
        "voice_safe": "You are safe. Situation is currently stable.",
        "safety_title": "🛡️ Safety Guidelines",
        "safety_sub": "What to do **before, during and after** a landslide.",
        "safety_1": "1️⃣ Before a Landslide (Preparedness)",
        "safety_1_text": "- Know if your area is landslide-prone\n- Prepare emergency kit\n- Save emergency numbers\n- Avoid steep unstable slopes\n- Follow IMD warnings",
        "safety_2": "2️⃣ When Landslide is About to Happen",
        "safety_2_text": "**Act Fast:**\n- Move to higher safer ground\n- Stay away from slopes and streams\n- Help children & elderly\n- Listen to official alerts",
        "safety_3": "3️⃣ After a Landslide",
        "safety_3_text": "- Stay away from the slide area\n- Check for injured\n- Report to authorities\n- Do not drink stream water\n- Wait for official clearance",
        "safety_gold": "**Golden Rule:** Life first. If ground is moving, leave immediately.",
        "emg_title": "🚨 Emergency Actions",
        "emg_sub": "If a landslide is about to happen — **what should you do first?**",
        "emg_first": "### 🔴 FIRST PRIORITY — SAVE LIFE",
        "emg_first_text": "1. Evacuate to higher safer ground\n2. Do not wait for valuables\n3. Help children & elderly first\n4. Move away from slope\n5. Call emergency numbers",
        "emg_dos": "Do’s ✅",
        "emg_dos_text": "- Move to higher ground fast\n- Stay with family\n- Follow official instructions\n- Keep phone charged\n- Wear sturdy shoes",
        "emg_donts": "Don’ts ❌",
        "emg_donts_text": "- Do not go near slope edge\n- Do not shelter under trees on slope\n- Do not drive on cracked roads\n- Do not return until safe\n- Do not spread rumours",
        "emg_help": "📞 Helpline Numbers (India)",
        "emg_help_text": "- **National Emergency:** 112\n- **Disaster Management:** 1078 / 1070\n- **Police:** 100\n- **Ambulance:** 108 / 102\n- **Fire:** 101"
    },
    "Hindi": {
        "app_title": "⚠️ बिलाल्स सेंटिनल",
        "app_sub": "एआई लैंडस्लाइड अर्ली वार्निंग सिस्टम | बिलाल अली",
        "nav_home": "🏠 होम",
        "nav_risk": "🔍 जोखिम अनुमान",
        "nav_safety": "🛡️ सुरक्षा दिशानिर्देश",
        "nav_emergency": "🚨 आपातकालीन कार्रवाई",
        "home_title": "⚠️ बिलाल्स सेंटिनल",
        "home_sub": "एआई-संचालित लैंडस्लाइड अर्ली वार्निंग सिस्टम",
        "home_by": "बिलाल अली द्वारा | सीएसई विभाग, केएमसीएलयू",
        "home_card1": "📍 **लोकेशन आधारित**\n\nकोई भी स्थान डालें और Google Map के साथ जोखिम विश्लेषण पाएं।",
        "home_card2": "🤖 **एआई प्रेडिक्शन**\n\nवर्षा, ढलान, नमी और ऊंचाई पर आधारित मॉडल।",
        "home_card3": "🔊 **वॉइस + गाइडेंस**\n\nबोलकर अलर्ट और स्पष्ट सुरक्षा निर्देश।",
        "home_why": "### यह सिस्टम क्यों?",
        "home_why_text": "हर साल भारत के पहाड़ी क्षेत्रों में लैंडस्लाइड से जान-माल का नुकसान होता है। अर्ली वार्निंग सिस्टम जान बचा सकता है।",
        "home_how": "### कैसे इस्तेमाल करें",
        "home_how_text": "1. **जोखिम अनुमान** पेज पर जाएं\n2. लोकेशन डालें\n3. पैरामीटर सेट करें\n4. Predict दबाएं\n5. परिणाम + मैप देखें",
        "home_go": "👉 बाएं साइडबार से **जोखिम अनुमान** खोलें।",
        "location": "📍 लोकेशन दर्ज करें",
        "placeholder": "उदाहरण: गंगटोक, दार्जिलिंग, मनाली",
        "params": "🔢 पर्यावरणीय पैरामीटर",
        "rainfall": "🌧️ वर्षा (मिमी)",
        "slope": "📐 ढलान कोण (डिग्री)",
        "moisture": "💧 मिट्टी की नमी (0-1)",
        "elevation": "⛰️ ऊंचाई (मीटर)",
        "button": "🔍 जोखिम का अनुमान लगाएं और मैप दिखाएं",
        "result": "📊 भविष्यवाणी परिणाम",
        "high_risk": "🚨 लैंडस्लाइड का उच्च जोखिम पाया गया",
        "low_risk": "✅ कम जोखिम — स्थिति स्थिर है",
        "probability": "जोखिम की संभावना",
        "actions": "तत्काल कार्रवाई",
        "action1": "ढलान और निचले क्षेत्रों से लोगों को निकालें",
        "action2": "स्थानीय आपदा प्रबंधन को सूचित करें",
        "action3": "पहाड़ी सड़कों पर यात्रा से बचें",
        "action4": "वर्षा की निगरानी करें",
        "status": "वर्तमान स्थिति",
        "status1": "स्थितियां सुरक्षित हैं",
        "status2": "नियमित निगरानी जारी रखें",
        "status3": "भारी बारिश में सतर्क रहें",
        "map": "🗺️ लोकेशन मैप (Google Maps)",
        "map_info": "मान्य लोकेशन दर्ज करें।",
        "voice_danger": "चेतावनी! लैंडस्लाइड का उच्च जोखिम पाया गया है।",
        "voice_safe": "आप सुरक्षित हैं। स्थिति स्थिर है।",
        "safety_title": "🛡️ सुरक्षा दिशानिर्देश",
        "safety_sub": "लैंडस्लाइड से पहले, दौरान और बाद में क्या करें।",
        "safety_1": "1️⃣ लैंडस्लाइड से पहले",
        "safety_1_text": "- क्षेत्र का जोखिम जानें\n- इमरजेंसी किट तैयार रखें\n- नंबर सेव करें\n- ढलान पर न रहें\n- आईएमडी चेतावनी सुनें",
        "safety_2": "2️⃣ जब लैंडस्लाइड आने वाला हो",
        "safety_2_text": "**तुरंत:**\n- ऊंची जगह जाएं\n- ढलान से दूर रहें\n- बच्चों-बुजुर्गों की मदद करें\n- आधिकारिक अलर्ट सुनें",
        "safety_3": "3️⃣ लैंडस्लाइड के बाद",
        "safety_3_text": "- स्लाइड इलाके से दूर रहें\n- घायलों की मदद करें\n- अधिकारियों को बताएं\n- नाले का पानी न पिएं\n- मंजूरी के बाद लौटें",
        "safety_gold": "**सुनहरा नियम:** पहले जान। जमीन हिले तो तुरंत निकलें।",
        "emg_title": "🚨 आपातकालीन कार्रवाई",
        "emg_sub": "लैंडस्लाइड आने वाला हो तो सबसे पहले क्या करें?",
        "emg_first": "### 🔴 पहली प्राथमिकता — जान बचाएं",
        "emg_first_text": "1. ऊंची सुरक्षित जगह जाएं\n2. सामान का इंतजार न करें\n3. बच्चों-बुजुर्गों की मदद करें\n4. ढलान से दूर जाएं\n5. इमरजेंसी नंबर पर कॉल करें",
        "emg_dos": "क्या करें ✅",
        "emg_dos_text": "- जल्दी ऊंची जगह जाएं\n- परिवार के साथ रहें\n- निर्देशों का पालन करें\n- फोन चार्ज रखें\n- मजबूत जूते पहनें",
        "emg_donts": "क्या न करें ❌",
        "emg_donts_text": "- ढलान किनारे न जाएं\n- पेड़ों के नीचे न छुपें\n- टूटी सड़क पर न चलें\n- सुरक्षित होने तक न लौटें\n- अफवाह न फैलाएं",
        "emg_help": "📞 हेल्पलाइन (भारत)",
        "emg_help_text": "- **नेशनल इमरजेंसी:** 112\n- **आपदा प्रबंधन:** 1078 / 1070\n- **पुलिस:** 100\n- **एम्बुलेंस:** 108 / 102\n- **फायर:** 101"
    }
}

for lang_name in ["Bengali", "Tamil", "Telugu", "Marathi"]:
    translations[lang_name] = translations["English"].copy()

lang_codes = {
    "English": "en-IN", "Hindi": "hi-IN", "Bengali": "bn-IN",
    "Tamil": "ta-IN", "Telugu": "te-IN", "Marathi": "mr-IN"
}

# ====================== SIDEBAR ======================
st.sidebar.title("⚠️ Bilal’s Sentinel")
st.sidebar.caption("AI Landslide Early Warning System")
st.sidebar.markdown("---")

lang = st.sidebar.selectbox("🌐 Language / भाषा", ["English", "Hindi", "Bengali", "Tamil", "Telugu", "Marathi"])
t = translations[lang]
current_lang_code = lang_codes.get(lang, "en-IN")

page = st.sidebar.radio("Go to page", [t["nav_home"], t["nav_risk"], t["nav_safety"], t["nav_emergency"]])

st.sidebar.markdown("---")
st.sidebar.markdown("**Developed by Bilal Ali**")
st.sidebar.markdown("CSE | KMCLU | SIH 2026")

# ====================== PAGE 1: HOME ======================
if page == t["nav_home"]:
    st.title(t["home_title"])
    st.markdown(f"### {t['home_sub']}")
    st.markdown(f"**{t['home_by']}**")
    st.markdown("---")

    c1, c2, c3 = st.columns(3)
    with c1: st.info(t["home_card1"])
    with c2: st.success(t["home_card2"])
    with c3: st.warning(t["home_card3"])

    st.markdown(t["home_why"])
    st.write(t["home_why_text"])
    st.markdown(t["home_how"])
    st.write(t["home_how_text"])
    st.success(t["home_go"])

# ====================== PAGE 2: RISK ======================
elif page == t["nav_risk"]:
    st.title(t["app_title"])
    st.markdown(f"**{t['app_sub']}**")
    st.markdown("---")

    try:
        data = pd.read_csv("data.csv")
        X = data[["rainfall_mm", "slope_angle", "soil_moisture", "elevation"]]
        y = data["landslide"]
        model = RandomForestClassifier(n_estimators=100, random_state=42)
        model.fit(X, y)
    except Exception:
        st.error("Error loading data.csv")
        st.stop()

    st.subheader(t["location"])
    location_name = st.text_input(t["placeholder"])

    if location_name:
        try:
            geolocator = Nominatim(user_agent="bilal_sentinel_app")
            location = geolocator.geocode(location_name, timeout=10)
            if location:
                st.session_state.lat = location.latitude
                st.session_state.lon = location.longitude
                st.session_state.loc_name = location_name
                st.success(f"✅ {location.address}")
            else:
                st.warning("Location not found. Try: Gangtok, Manali, Shimla")
        except Exception:
            st.warning("Could not fetch location")

    st.markdown("---")
    st.subheader(t["params"])
    col1, col2 = st.columns(2)
    with col1:
        rainfall = st.slider(t["rainfall"], 0, 300, 120)
        slope = st.slider(t["slope"], 0, 60, 28)
    with col2:
        moisture = st.slider(t["moisture"], 0.0, 1.0, 0.50)
        elevation = st.slider(t["elevation"], 100, 3000, 800)

    st.markdown("---")
    if st.button(t["button"], use_container_width=True, type="primary"):
        input_data = [[rainfall, slope, moisture, elevation]]
        st.session_state.prediction = int(model.predict(input_data)[0])
        st.session_state.probability = float(model.predict_proba(input_data)[0][1] * 100)
        st.session_state.predicted = True

    if st.session_state.predicted:
        st.subheader(t["result"])
        if st.session_state.loc_name:
            st.write(f"**Location:** {st.session_state.loc_name}")

        if st.session_state.prediction == 1:
            st.error(t["high_risk"])
            st.metric(t["probability"], f"{st.session_state.probability:.1f}%")
            st.warning(f"**{t['actions']}:**\n- {t['action1']}\n- {t['action2']}\n- {t['action3']}\n- {t['action4']}")
            risk_text = "HIGH RISK"
            components.html(f"""
                <script>
                    var msg = new SpeechSynthesisUtterance(`{t['voice_danger']}`);
                    msg.lang = "{current_lang_code}";
                    msg.rate = 0.85;
                    window.speechSynthesis.speak(msg);
                </script>
            """, height=0)
        else:
            st.success(t["low_risk"])
            st.metric(t["probability"], f"{st.session_state.probability:.1f}%")
            st.info(f"**{t['status']}:**\n- {t['status1']}\n- {t['status2']}\n- {t['status3']}")
            risk_text = "LOW RISK"
            components.html(f"""
                <script>
                    var msg = new SpeechSynthesisUtterance(`{t['voice_safe']}`);
                    msg.lang = "{current_lang_code}";
                    msg.rate = 0.85;
                    window.speechSynthesis.speak(msg);
                </script>
            """, height=0)

        st.subheader(t["map"])
        if st.session_state.lat and st.session_state.lon:
            lat = st.session_state.lat
            lon = st.session_state.lon
            map_html = f"""
            <iframe width="100%" height="450" style="border:0; border-radius:12px;"
                loading="lazy" allowfullscreen
                src="https://www.google.com/maps?q={lat},{lon}&hl=en&z=14&output=embed">
            </iframe>
            """
            components.html(map_html, height=470)
            st.caption(f"📍 {lat:.5f}, {lon:.5f} | Risk: {risk_text}")
        else:
            st.info(t["map_info"])

# ====================== PAGE 3: SAFETY ======================
elif page == t["nav_safety"]:
    st.title(t["safety_title"])
    st.markdown(t["safety_sub"])
    st.markdown("---")
    st.subheader(t["safety_1"])
    st.write(t["safety_1_text"])
    st.subheader(t["safety_2"])
    st.warning(t["safety_2_text"])
    st.subheader(t["safety_3"])
    st.write(t["safety_3_text"])
    st.info(t["safety_gold"])

# ====================== PAGE 4: EMERGENCY ======================
elif page == t["nav_emergency"]:
    st.title(t["emg_title"])
    st.markdown(t["emg_sub"])
    st.markdown("---")
    st.error(t["emg_first"])
    st.write(t["emg_first_text"])
    col1, col2 = st.columns(2)
    with col1:
        st.subheader(t["emg_dos"])
        st.success(t["emg_dos_text"])
    with col2:
        st.subheader(t["emg_donts"])
        st.error(t["emg_donts_text"])
    st.markdown("---")
    st.subheader(t["emg_help"])
    st.write(t["emg_help_text"])

st.markdown("---")
st.caption("Bilal’s Sentinel | Developed by Bilal Ali | SIH 2026")