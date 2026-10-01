import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import streamlit as st
import folium
from streamlit_folium import st_folium
from geopy.geocoders import Nominatim
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Bilal’s Sentinel",
    page_icon="⚠️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ====================== SESSION STATE ======================
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

# ====================== TRANSLATIONS ======================
translations = {
    "English": {
        "title": "⚠️ Bilal’s Sentinel",
        "subtitle": "AI Landslide Early Warning System | By Bilal Ali",
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
        "map": "🗺️ Location Map",
        "map_info": "Enter a valid location name to see the map.",
        "voice_danger": "Warning! High risk of landslide detected. Please take immediate action.",
        "voice_safe": "You are safe. Situation is currently stable."
    },
    "Hindi": {
        "title": "⚠️ बिलाल्स सेंटिनल",
        "subtitle": "एआई लैंडस्लाइड अर्ली वार्निंग सिस्टम | बिलाल अली",
        "location": "📍 लोकेशन दर्ज करें",
        "placeholder": "उदाहरण: गंगटोक, दार्जिलिंग, मनाली, शिमला",
        "params": "🔢 पर्यावरणीय पैरामीटर",
        "rainfall": "🌧️ वर्षा (मिमी)",
        "slope": "📐 ढलान कोण (डिग्री)",
        "moisture": "💧 मिट्टी की नमी (0-1)",
        "elevation": "⛰️ ऊंचाई (मीटर)",
        "button": "🔍 जोखिम का अनुमान लगाएं और मैप दिखाएं",
        "result": "📊 भविष्यवाणी परिणाम",
        "high_risk": "🚨 लैंडस्लाइड का उच्च जोखिम पाया गया",
        "low_risk": "✅ कम जोखिम — स्थिति वर्तमान में स्थिर है",
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
        "voice_danger": "चेतावनी! लैंडस्लाइड का उच्च जोखिम पाया गया है। कृपया तुरंत कार्रवाई करें।",
        "voice_safe": "आप सुरक्षित हैं। स्थिति वर्तमान में स्थिर है।"
    },
    "Bengali": {
        "title": "⚠️ বিলাল’স সেন্টিনেল",
        "subtitle": "এআই ল্যান্ডস্লাইড আর্লি ওয়ার্নিং সিস্টেম | বিলাল আলি",
        "location": "📍 লোকেশন লিখুন",
        "placeholder": "উদাহরণ: গ্যাংটক, দার্জিলিং, মানালি",
        "params": "🔢 পরিবেশগত প্যারামিটার",
        "rainfall": "🌧️ বৃষ্টিপাত (মিমি)",
        "slope": "📐 ঢালের কোণ (ডিগ্রি)",
        "moisture": "💧 মাটির আর্দ্রতা (0-1)",
        "elevation": "⛰️ উচ্চতা (মিটার)",
        "button": "🔍 ঝুঁকি নির্ণয় করুন এবং ম্যাপ দেখান",
        "result": "📊 পূর্বাভাসের ফলাফল",
        "high_risk": "🚨 ল্যান্ডস্লাইডের উচ্চ ঝুঁকি সনাক্ত হয়েছে",
        "low_risk": "✅ কম ঝুঁকি — পরিস্থিতি বর্তমানে স্থিতিশীল",
        "probability": "ঝুঁকির সম্ভাবনা",
        "actions": "তাৎক্ষণিক পদক্ষেপ",
        "action1": "ঢালু এবং নিচু এলাকা থেকে মানুষ সরিয়ে নিন",
        "action2": "স্থানীয় দুর্যোগ ব্যবস্থাপনা কর্তৃপক্ষকে জানান",
        "action3": "পাহাড়ি রাস্তায় চলাচল এড়িয়ে চলুন",
        "action4": "বৃষ্টির ক্রমাগত পর্যবেক্ষণ করুন",
        "status": "বর্তমান অবস্থা",
        "status1": "পরিস্থিতি নিরাপদ সীমার মধ্যে আছে",
        "status2": "নিয়মিত পর্যবেক্ষণ চালিয়ে যান",
        "status3": "ভারী বৃষ্টির সময় সতর্ক থাকুন",
        "map": "🗺️ লোকেশন ম্যাপ",
        "map_info": "ম্যাপ দেখতে একটি বৈধ লোকেশন নাম লিখুন।",
        "voice_danger": "সতর্কতা! ভূমিধসের উচ্চ ঝুঁকি সনাক্ত হয়েছে।",
        "voice_safe": "আপনি নিরাপদ। পরিস্থিতি বর্তমানে স্থিতিশীল।"
    },
    "Tamil": {
        "title": "⚠️ பிலால்’ஸ் சென்டினல்",
        "subtitle": "AI நிலச்சரிவு முன்னெச்சரிக்கை அமைப்பு | பிலால் அலி",
        "location": "📍 இடத்தை உள்ளிடவும்",
        "placeholder": "உதாரணம்: காங்டாக், டார்ஜிலிங், மணாலி",
        "params": "🔢 சுற்றுச்சூழல் அளவுருக்கள்",
        "rainfall": "🌧️ மழைப்பொழிவு (மிமீ)",
        "slope": "📐 சாய்வு கோணம் (டிகிரி)",
        "moisture": "💧 மண் ஈரப்பதம் (0-1)",
        "elevation": "⛰️ உயரம் (மீட்டர்)",
        "button": "🔍 அபாயத்தை கணித்து வரைபடத்தைக் காட்டு",
        "result": "📊 கணிப்பு முடிவு",
        "high_risk": "🚨 நிலச்சரிவு அதிக அபாயம் கண்டறியப்பட்டது",
        "low_risk": "✅ குறைந்த அபாயம் — நிலைமை தற்போது நிலையானது",
        "probability": "அபாய நிகழ்தகவு",
        "actions": "உடனடி நடவடிக்கைகள்",
        "action1": "சாய்வு மற்றும் தாழ்வான பகுதிகளிலிருந்து மக்களை வெளியேற்றுங்கள்",
        "action2": "உள்ளூர் பேரிடர் மேலாண்மை ஆணையத்திற்கு தெரிவிக்கவும்",
        "action3": "மலைச்சாலைகளில் பயணத்தைத் தவிர்க்கவும்",
        "action4": "மழையை தொடர்ந்து கண்காணிக்கவும்",
        "status": "தற்போதைய நிலை",
        "status1": "நிலைமைகள் பாதுகாப்பான வரம்புக்குள் உள்ளன",
        "status2": "வழக்கமான கண்காணிப்பைத் தொடரவும்",
        "status3": "கனமழையின் போது விழிப்புடன் இருங்கள்",
        "map": "🗺️ இட வரைபடம்",
        "map_info": "வரைபடத்தைக் காண சரியான இடப் பெயரை உள்ளிடவும்.",
        "voice_danger": "எச்சரிக்கை! நிலச்சரிவு அதிக அபாயம் கண்டறியப்பட்டது.",
        "voice_safe": "நீங்கள் பாதுகாப்பாக இருக்கிறீர்கள். நிலைமை நிலையானது."
    },
    "Telugu": {
        "title": "⚠️ బిలాల్’స్ సెంటినెల్",
        "subtitle": "AI భూపాతం ముందస్తు హెచ్చరిక వ్యవస్థ | బిలాల్ అలి",
        "location": "📍 లొకేషన్ నమోదు చేయండి",
        "placeholder": "ఉదా: గ్యాంగ్‌టక్, డార్జిలింగ్, మనాలి",
        "params": "🔢 పర్యావరణ పారామితులు",
        "rainfall": "🌧️ వర్షపాతం (మిమీ)",
        "slope": "📐 వాలు కోణం (డిగ్రీలు)",
        "moisture": "💧 నేల తేమ (0-1)",
        "elevation": "⛰️ ఎత్తు (మీటర్లు)",
        "button": "🔍 ప్రమాదాన్ని అంచనా వేసి మ్యాప్ చూపించు",
        "result": "📊 అంచనా ఫలితం",
        "high_risk": "🚨 భూపాతం అధిక ప్రమాదం గుర్తించబడింది",
        "low_risk": "✅ తక్కువ ప్రమాదం — పరిస్థితి ప్రస్తుతం స్థిరంగా ఉంది",
        "probability": "ప్రమాద సంభావ్యత",
        "actions": "తక్షణ చర్యలు",
        "action1": "వాలు మరియు లోతట్టు ప్రాంతాల నుండి ప్రజలను తరలించండి",
        "action2": "స్థానిక విపత్తు నిర్వహణ అధికారులకు సమాచారం ఇవ్వండి",
        "action3": "కొండ రోడ్లపై ప్రయాణం నివారించండి",
        "action4": "వర్షపాతాన్ని నిరంతరం పర్యవేక్షించండి",
        "status": "ప్రస్తుత స్థితి",
        "status1": "పరిస్థితులు సురక్షిత పరిమితుల్లో ఉన్నాయి",
        "status2": "క్రమం తప్పకుండా పర్యవేక్షణ కొనసాగించండి",
        "status3": "భారీ వర్షాల సమయంలో అప్రమత్తంగా ఉండండి",
        "map": "🗺️ లొకేషన్ మ్యాప్",
        "map_info": "మ్యాప్ చూడటానికి సరైన లొకేషన్ పేరు నమోదు చేయండి.",
        "voice_danger": "హెచ్చరిక! భూపాతం అధిక ప్రమాదం గుర్తించబడింది.",
        "voice_safe": "మీరు సురక్షితంగా ఉన్నారు. పరిస్థితి స్థిరంగా ఉంది."
    },
    "Marathi": {
        "title": "⚠️ बिलाल्स सेंटिनल",
        "subtitle": "एआय भूस्खलन पूर्व चेतावणी प्रणाली | बिलाल अली",
        "location": "📍 स्थान प्रविष्ट करा",
        "placeholder": "उदाहरण: गँगटोक, दार्जिलिंग, मनाली",
        "params": "🔢 पर्यावरणीय पॅरामीटर्स",
        "rainfall": "🌧️ पर्जन्य (मिमी)",
        "slope": "📐 उतार कोन (अंश)",
        "moisture": "💧 मातीची आर्द्रता (0-1)",
        "elevation": "⛰️ उंची (मीटर)",
        "button": "🔍 जोखीम अंदाज लावा आणि नकाशा दाखवा",
        "result": "📊 अंदाज परिणाम",
        "high_risk": "🚨 भूस्खलनाचा उच्च धोका आढळला",
        "low_risk": "✅ कमी धोका — परिस्थिती सध्या स्थिर आहे",
        "probability": "जोखीम संभाव्यता",
        "actions": "तात्काळ कृती",
        "action1": "उतार आणि सखल भागांतून लोकांना हलवा",
        "action2": "स्थानिक आपत्ती व्यवस्थापन प्राधिकरणाला कळवा",
        "action3": "डोंगराळ रस्त्यांवर प्रवास टाळा",
        "action4": "पर्जन्याचे सतत निरीक्षण करा",
        "status": "सध्याची स्थिती",
        "status1": "परिस्थिती सुरक्षित मर्यादेत आहे",
        "status2": "नियमित निरीक्षण सुरू ठेवा",
        "status3": "मुसळधार पावसाच्या वेळी सतर्क रहा",
        "map": "🗺️ स्थान नकाशा",
        "map_info": "नकाशा पाहण्यासाठी वैध स्थान नाव प्रविष्ट करा.",
        "voice_danger": "चेतावणी! भूस्खलनाचा उच्च धोका आढळला आहे.",
        "voice_safe": "तुम्ही सुरक्षित आहात. परिस्थिती सध्या स्थिर आहे."
    }
}

lang_codes = {
    "English": "en-IN",
    "Hindi": "hi-IN",
    "Bengali": "bn-IN",
    "Tamil": "ta-IN",
    "Telugu": "te-IN",
    "Marathi": "mr-IN"
}

# ====================== SIDEBAR ======================
st.sidebar.title("⚠️ Bilal’s Sentinel")
st.sidebar.caption("AI Landslide Early Warning System")
st.sidebar.markdown("---")

page = st.sidebar.radio(
    "Go to page",
    ["🏠 Home", "🔍 Risk Prediction", "🛡️ Safety Guidelines", "🚨 Emergency Actions"]
)

st.sidebar.markdown("---")
lang = st.sidebar.selectbox("🌐 Language", ["English", "Hindi", "Bengali", "Tamil", "Telugu", "Marathi"])
t = translations[lang]
current_lang_code = lang_codes.get(lang, "en-IN")

st.sidebar.markdown("---")
st.sidebar.markdown("**Developed by Bilal Ali**")
st.sidebar.markdown("CSE | KMCLU")
st.sidebar.markdown("SIH 2026 | SIH26001")

# ====================== PAGE 1: HOME ======================
if page == "🏠 Home":
    st.title("⚠️ Bilal’s Sentinel")
    st.markdown("### AI-Powered Landslide Early Warning System")
    st.markdown("**By Bilal Ali | CSE Department, KMCLU**")
    st.markdown("---")

    c1, c2, c3 = st.columns(3)
    with c1:
        st.info("📍 **Location Based**\n\nEnter any place and get risk analysis with map.")
    with c2:
        st.success("🤖 **AI Prediction**\n\nRandom Forest model using rainfall, slope, moisture & elevation.")
    with c3:
        st.warning("🔊 **Voice + Guidance**\n\nSpoken alerts and clear safety instructions.")

    st.markdown("### Why this system?")
    st.write("""
    Every year landslides cause loss of life and property in hilly regions of India 
    (Uttarakhand, Himachal Pradesh, Northeast, Western Ghats).  
    An early warning system based on simple environmental parameters can help 
    people and authorities take timely action and save lives.
    """)

    st.markdown("### How to use")
    st.write("""
    1. Go to **🔍 Risk Prediction** page  
    2. Enter a location (example: Gangtok, Darjeeling, Manali)  
    3. Adjust Rainfall, Slope, Soil Moisture, Elevation  
    4. Click **Predict Risk & Show Map**  
    5. Read the result + map + safety guidance  
    """)

    st.success("👉 Open **Risk Prediction** page from the left sidebar to try the system.")

# ====================== PAGE 2: RISK PREDICTION ======================
elif page == "🔍 Risk Prediction":
    st.title(t["title"])
    st.markdown(f"**{t['subtitle']}**")
    st.markdown("---")

    try:
        data = pd.read_csv("data.csv")
        X = data[["rainfall_mm", "slope_angle", "soil_moisture", "elevation"]]
        y = data["landslide"]
        model = RandomForestClassifier(n_estimators=100, random_state=42)
        model.fit(X, y)
    except Exception:
        st.error("Error loading data.csv. Make sure the file is uploaded on GitHub.")
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
                st.warning("Location not found")
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
                    var msg = new SpeechSynthesisUtterance(`{t['voice_danger']}`);
                    msg.lang = "{current_lang_code}";
                    msg.rate = 0.85;
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
                    var msg = new SpeechSynthesisUtterance(`{t['voice_safe']}`);
                    msg.lang = "{current_lang_code}";
                    msg.rate = 0.85;
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
            folium.Circle(
                radius=2500,
                location=[st.session_state.lat, st.session_state.lon],
                color=map_color,
                fill=True,
                fill_opacity=0.25
            ).add_to(m)
            st_folium(m, width=700, height=400, key="risk_map")
        else:
            st.info(t["map_info"])

# ====================== PAGE 3: SAFETY GUIDELINES ======================
elif page == "🛡️ Safety Guidelines":
    st.title("🛡️ Safety Guidelines")
    st.markdown("What to do **before, during and after** a landslide.")
    st.markdown("---")

    st.subheader("1️⃣ Before a Landslide (Preparedness)")
    st.write("""
    - Know whether your area is landslide-prone  
    - Prepare emergency kit (torch, water, first-aid, documents, power bank)  
    - Save emergency contact numbers  
    - Avoid building/staying on steep unstable slopes  
    - Maintain vegetation on slopes  
    - Follow IMD and local rainfall warnings  
    """)

    st.subheader("2️⃣ When Landslide is About to Happen")
    st.warning("""
    **Act Fast:**
    - Move immediately to higher safer ground  
    - Stay away from slopes, valleys and streams  
    - Do not waste time collecting belongings  
    - Alert neighbours and help children & elderly  
    - Listen to official alerts  
    """)

    st.subheader("3️⃣ After a Landslide")
    st.write("""
    - Stay away from the slide area  
    - Check for injured and give first aid if trained  
    - Report to disaster management / police  
    - Do not drink water from nearby streams  
    - Wait for official clearance before returning  
    """)

    st.info("**Golden Rule:** Life first. If ground is moving or you hear rumbling, leave immediately.")

# ====================== PAGE 4: EMERGENCY ACTIONS ======================
elif page == "🚨 Emergency Actions":
    st.title("🚨 Emergency Actions")
    st.markdown("If a landslide is about to happen — **what should you do first?**")
    st.markdown("---")

    st.error("### 🔴 FIRST PRIORITY — SAVE LIFE")
    st.write("""
    1. Evacuate immediately to higher safer ground  
    2. Do not wait to collect valuables  
    3. Help children, elderly and differently-abled first  
    4. Move away from the slope direction  
    5. Call emergency numbers  
    """)

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Do’s ✅")
        st.success("""
        - Move to higher ground fast  
        - Stay with family  
        - Follow official instructions  
        - Keep phone charged  
        - Wear sturdy shoes  
        """)
    with col2:
        st.subheader("Don’ts ❌")
        st.error("""
        - Do not go near slope edge  
        - Do not shelter under trees on slope  
        - Do not drive on cracked roads  
        - Do not return until safe  
        - Do not spread rumours  
        """)

    st.markdown("---")
    st.subheader("📞 Helpline Numbers (India)")
    st.write("""
    - **National Emergency:** 112  
    - **Disaster Management:** 1078 / 1070  
    - **Police:** 100  
    - **Ambulance:** 108 / 102  
    - **Fire:** 101  
    """)

st.markdown("---")
st.caption("Bilal’s Sentinel | Developed by Bilal Ali | SIH 2026")
