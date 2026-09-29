import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import streamlit as st
import folium
from streamlit_folium import st_folium
from geopy.geocoders import Nominatim
import streamlit.components.v1 as components
import time

st.set_page_config(page_title="Bilal’s Sentinel", page_icon="⚠️", layout="wide")

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
        .stApp {
            background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
            color: white;
        }
        .intro-title {
            font-size: 3.2rem;
            font-weight: 800;
            text-align: center;
            background: linear-gradient(90deg, #ff4b4b, #ffcc00);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-top: 8vh;
            animation: fadeIn 1.5s ease-in;
        }
        .intro-sub {
            text-align: center;
            font-size: 1.3rem;
            color: #e0e0e0;
            margin-top: 1rem;
            animation: fadeIn 2s ease-in;
        }
        .intro-msg {
            text-align: center;
            font-size: 1.1rem;
            color: #b0b0b0;
            margin-top: 2rem;
            max-width: 600px;
            margin-left: auto;
            margin-right: auto;
            animation: fadeIn 2.5s ease-in;
        }
        .landslide-anim {
            text-align: center;
            font-size: 4rem;
            margin-top: 3rem;
            animation: shake 2s infinite;
        }
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(20px); }
            to { opacity: 1; transform: translateY(0); }
        }
        @keyframes shake {
            0% { transform: translateY(0); }
            25% { transform: translateY(8px); }
            50% { transform: translateY(0); }
            75% { transform: translateY(-8px); }
            100% { transform: translateY(0); }
        }
        </style>
    """, unsafe_allow_html=True)

    st.markdown('<div class="intro-title">⚠️ Bilal’s Sentinel</div>', unsafe_allow_html=True)
    st.markdown('<div class="intro-sub">AI Landslide Early Warning System</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="landslide-anim">🏔️💥🪨</div>', unsafe_allow_html=True)
    
    st.markdown("""
        <div class="intro-msg">
            Welcome — where the most relevant data is provided to alert you<br>
            before disaster strikes.
        </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🚀 Enter App", use_container_width=True):
            st.session_state.show_intro = False
            st.rerun()

    # Auto redirect after 5 seconds
    time.sleep(5)
    st.session_state.show_intro = False
    st.rerun()

# ====================== MAIN APP ======================
else:

    # Translations
    translations = {
        "English": {
            "title": "⚠️ Bilal’s Sentinel",
            "subtitle": "AI Landslide Early Warning System | By Bilal Ali",
            "about": "About Project",
            "about_text": "Type any location and get landslide risk prediction with map.",
            "location": "📍 Enter Any Location",
            "placeholder": "Enter city name (Example: Lucknow, Gangtok, Darjeeling)",
            "params": "🔢 Environmental Parameters",
            "rainfall": "🌧️ Rainfall (mm)",
            "slope": "📐 Slope Angle (degrees)",
            "moisture": "💧 Soil Moisture (0-1)",
            "elevation": "⛰️ Elevation (meters)",
            "button": "🔍 Predict Risk & Show Map",
            "result": "📊 Prediction Result",
            "high_risk": "🚨 HIGH RISK of Landslide Detected",
            "low_risk": "✅ LOW RISK - Situation Currently Stable",
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
            "map": "🗺️ Location Map",
            "map_info": "Enter a valid location name to see the map.",
            "voice_danger": "Warning! You are in danger. High risk of landslide detected. Please take immediate action.",
            "voice_safe": "You are safe. The situation is currently stable. Keep monitoring."
        },
        "Hindi": {
            "title": "⚠️ बिलाल्स सेंटिनल",
            "subtitle": "एआई लैंडस्लाइड अर्ली वार्निंग सिस्टम | बिलाल अली द्वारा",
            "about": "प्रोजेक्ट के बारे में",
            "about_text": "कोई भी लोकेशन टाइप करें और मैप के साथ लैंडस्लाइड रिस्क प्रेडिक्शन पाएं।",
            "location": "📍 कोई भी लोकेशन दर्ज करें",
            "placeholder": "शहर का नाम लिखें (उदाहरण: लखनऊ, गंगटोक, दार्जिलिंग)",
            "params": "🔢 पर्यावरणीय पैरामीटर",
            "rainfall": "🌧️ वर्षा (मिमी)",
            "slope": "📐 ढलान कोण (डिग्री)",
            "moisture": "💧 मिट्टी की नमी (0-1)",
            "elevation": "⛰️ ऊंचाई (मीटर)",
            "button": "🔍 जोखिम का अनुमान लगाएं और मैप दिखाएं",
            "result": "📊 भविष्यवाणी परिणाम",
            "high_risk": "🚨 लैंडस्लाइड का उच्च जोखिम पाया गया",
            "low_risk": "✅ कम जोखिम - स्थिति वर्तमान में स्थिर है",
            "probability": "जोखिम की संभावना",
            "actions": "तत्काल कार्रवाई",
            "action1": "ढलान और निचले क्षेत्रों से लोगों को निकालें",
            "action2": "स्थानीय आपदा प्रबंधन प्राधिकरण को सूचित करें",
            "action3": "पहाड़ी सड़कों पर यात्रा से बचें",
            "action4": "वर्षा की लगातार निगरानी करें",
            "status": "वर्तमान स्थिति",
            "status1": "स्थितियां सुरक्षित सीमा के भीतर हैं",
            "status2": "नियमित निगरानी जारी रखें",
            "status3": "भारी बारिश के दौरान सतर्क रहें",
            "map": "🗺️ लोकेशन मैप",
            "map_info": "मैप देखने के लिए मान्य लोकेशन नाम दर्ज करें।",
            "voice_danger": "चेतावनी! आप खतरे में हैं। लैंडस्लाइड का उच्च जोखिम पाया गया है।",
            "voice_safe": "आप सुरक्षित हैं। स्थिति वर्तमान में स्थिर है।"
        }
    }

    lang = st.sidebar.selectbox("🌐 Select Language", ["English", "Hindi"])
    t = translations[lang]

    st.title(t["title"])
    st.markdown(f"**{t['subtitle']}**")
    st.markdown("---")

    # Load data
    data = pd.read_csv("data.csv")
    X = data[["rainfall_mm", "slope_angle", "soil_moisture", "elevation"]]
    y = data["landslide"]
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X, y)

    st.sidebar.header(t["about"])
    st.sidebar.write(t["about_text"])
    st.sidebar.write("**Problem:** SIH26001")
    st.sidebar.write("Developed by **Bilal Ali**")
    st.sidebar.write("CSE Department | KMCLU")

    # Location
    st.subheader(t["location"])
    location_name = st.text_input(t["placeholder"])

    if location_name:
        try:
            geolocator = Nominatim(user_agent="bilal_sentinel")
            location = geolocator.geocode(location_name, timeout=10)
            if location:
                st.session_state.lat = location.latitude
                st.session_state.lon = location.longitude
                st.session_state.loc_name = location_name
                st.success(f"{location.address}")
            else:
                st.warning("Location not found")
        except:
            st.warning("Could not fetch location")

    st.markdown("---")
    st.subheader(t["params"])

    c1, c2 = st.columns(2)
    with c1:
        rainfall = st.slider(t["rainfall"], 0, 300, 120)
        slope = st.slider(t["slope"], 0, 60, 28)
    with c2:
        moisture = st.slider(t["moisture"], 0.0, 1.0, 0.50)
        elevation = st.slider(t["elevation"], 100, 3000, 800)

    st.markdown("---")

    if st.button(t["button"], use_container_width=True):
        input_data = [[rainfall, slope, moisture, elevation]]
        st.session_state.prediction = model.predict(input_data)[0]
        st.session_state.probability = model.predict_proba(input_data)[0][1] * 100
        st.session_state.predicted = True

    if st.session_state.predicted:
        st.subheader(t["result"])
        if st.session_state.loc_name:
            st.write(f"**Location:** {st.session_state.loc_name}")

        if st.session_state.prediction == 1:
            st.error(t["high_risk"])
            st.metric(t["probability"], f"{st.session_state.probability:.1f}%")
            st.warning(f"""
            **{t['actions']}:**
            - {t['action1']}
            - {t['action2']}
            - {t['action3']}
            - {t['action4']}
            """)
            map_color = "red"
            risk_text = "HIGH RISK"

            components.html(f"""
                <script>
                    var msg = new SpeechSynthesisUtterance("{t['voice_danger']}");
                    msg.rate = 0.9;
                    window.speechSynthesis.speak(msg);
                </script>
            """, height=0)

        else:
            st.success(t["low_risk"])
            st.metric(t["probability"], f"{st.session_state.probability:.1f}%")
            st.info(f"""
            **{t['status']}:**
            - {t['status1']}
            - {t['status2']}
            - {t['status3']}
            """)
            map_color = "green"
            risk_text = "LOW RISK"

            components.html(f"""
                <script>
                    var msg = new SpeechSynthesisUtterance("{t['voice_safe']}");
                    msg.rate = 0.9;
                    window.speechSynthesis.speak(msg);
                </script>
            """, height=0)

        st.subheader(t["map"])
        if st.session_state.lat and st.session_state.lon:
            m = folium.Map(location=[st.session_state.lat, st.session_state.lon], zoom_start=12)
            folium.Marker(
                [st.session_state.lat, st.session_state.lon],
                popup=f"{st.session_state.loc_name}<br>{risk_text}",
                tooltip=risk_text,
                icon=folium.Icon(color=map_color, icon="info-sign")
            ).add_to(m)
            folium.Circle(radius=2500, location=[st.session_state.lat, st.session_state.lon],
                          color=map_color, fill=True, fill_opacity=0.25).add_to(m)
            st_folium(m, width=800, height=450, key="map")
        else:
            st.info(t["map_info"])

    st.markdown("---")
    st.caption("Bilal’s Sentinel | Developed by Bilal Ali | SIH 2026")
