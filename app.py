import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import streamlit as st
import folium
from streamlit_folium import st_folium
from geopy.geocoders import Nominatim
import base64

st.set_page_config(page_title="AI Landslide Early Warning System", page_icon="⚠️", layout="wide")

# ====================== TRANSLATIONS ======================
translations = {
    "English": {
        "title": "⚠️ AI Landslide Early Warning System",
        "subtitle": "SIH 2026 Prototype | Location Based Disaster Management",
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
        "lang": "Select Language"
    },
    "Hindi": {
        "title": "⚠️ एआई लैंडस्लाइड अर्ली वार्निंग सिस्टम",
        "subtitle": "SIH 2026 प्रोटोटाइप | लोकेशन बेस्ड डिजास्टर मैनेजमेंट",
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
        "lang": "भाषा चुनें"
    },
    "Bengali": {
        "title": "⚠️ এআই ল্যান্ডস্লাইড আর্লি ওয়ার্নিং সিস্টেম",
        "subtitle": "SIH 2026 প্রোটোটাইপ | লোকেশন ভিত্তিক দুর্যোগ ব্যবস্থাপনা",
        "about": "প্রজেক্ট সম্পর্কে",
        "about_text": "যেকোনো লোকেশন টাইপ করুন এবং ম্যাপসহ ল্যান্ডস্লাইড ঝুঁকির পূর্বাভাস পান।",
        "location": "📍 যেকোনো লোকেশন লিখুন",
        "placeholder": "শহরের নাম লিখুন (উদাহরণ: লখনউ, গ্যাংটক, দার্জিলিং)",
        "params": "🔢 পরিবেশগত প্যারামিটার",
        "rainfall": "🌧️ বৃষ্টিপাত (মিমি)",
        "slope": "📐 ঢালের কোণ (ডিগ্রি)",
        "moisture": "💧 মাটির আর্দ্রতা (0-1)",
        "elevation": "⛰️ উচ্চতা (মিটার)",
        "button": "🔍 ঝুঁকি নির্ণয় করুন এবং ম্যাপ দেখান",
        "result": "📊 পূর্বাভাসের ফলাফল",
        "high_risk": "🚨 ল্যান্ডস্লাইডের উচ্চ ঝুঁকি সনাক্ত হয়েছে",
        "low_risk": "✅ কম ঝুঁকি - পরিস্থিতি বর্তমানে স্থিতিশীল",
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
        "lang": "ভাষা নির্বাচন করুন"
    },
    "Tamil": {
        "title": "⚠️ AI நிலச்சரிவு முன்னெச்சரிக்கை அமைப்பு",
        "subtitle": "SIH 2026 முன்மாதிரி | இட அடிப்படையிலான பேரிடர் மேலாண்மை",
        "about": "திட்டம் பற்றி",
        "about_text": "எந்த இடத்தையும் உள்ளிட்டு வரைபடத்துடன் நிலச்சரிவு அபாய முன்னறிவிப்பைப் பெறுங்கள்.",
        "location": "📍 எந்த இடத்தையும் உள்ளிடவும்",
        "placeholder": "நகரத்தின் பெயரை உள்ளிடவும் (உதாரணம்: லக்னோ, காங்டாக், டார்ஜிலிங்)",
        "params": "🔢 சுற்றுச்சூழல் அளவுருக்கள்",
        "rainfall": "🌧️ மழைப்பொழிவு (மிமீ)",
        "slope": "📐 சாய்வு கோணம் (டிகிரி)",
        "moisture": "💧 மண் ஈரப்பதம் (0-1)",
        "elevation": "⛰️ உயரம் (மீட்டர்)",
        "button": "🔍 அபாயத்தை கணித்து வரைபடத்தைக் காட்டு",
        "result": "📊 கணிப்பு முடிவு",
        "high_risk": "🚨 நிலச்சரிவு அதிக அபாயம் கண்டறியப்பட்டது",
        "low_risk": "✅ குறைந்த அபாயம் - நிலைமை தற்போது நிலையானது",
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
        "lang": "மொழியைத் தேர்ந்தெடுக்கவும்"
    },
    "Telugu": {
        "title": "⚠️ AI భూపాతం ముందస్తు హెచ్చరిక వ్యవస్థ",
        "subtitle": "SIH 2026 ప్రోటోటైప్ | లొకేషన్ ఆధారిత విపత్తు నిర్వహణ",
        "about": "ప్రాజెక్ట్ గురించి",
        "about_text": "ఏదైనా లొకేషన్ టైప్ చేసి మ్యాప్‌తో భూపాత ప్రమాద అంచనా పొందండి.",
        "location": "📍 ఏదైనా లొకేషన్ నమోదు చేయండి",
        "placeholder": "నగరం పేరు టైప్ చేయండి (ఉదా: లక్నో, గ్యాంగ్‌టక్, డార్జిలింగ్)",
        "params": "🔢 పర్యావరణ పారామితులు",
        "rainfall": "🌧️ వర్షపాతం (మిమీ)",
        "slope": "📐 వాలు కోణం (డిగ్రీలు)",
        "moisture": "💧 నేల తేమ (0-1)",
        "elevation": "⛰️ ఎత్తు (మీటర్లు)",
        "button": "🔍 ప్రమాదాన్ని అంచనా వేసి మ్యాప్ చూపించు",
        "result": "📊 అంచనా ఫలితం",
        "high_risk": "🚨 భూపాతం అధిక ప్రమాదం గుర్తించబడింది",
        "low_risk": "✅ తక్కువ ప్రమాదం - పరిస్థితి ప్రస్తుతం స్థిరంగా ఉంది",
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
        "lang": "భాషను ఎంచుకోండి"
    },
    "Marathi": {
        "title": "⚠️ एआय भूस्खलन पूर्व चेतावणी प्रणाली",
        "subtitle": "SIH 2026 प्रोटोटाइप | स्थान आधारित आपत्ती व्यवस्थापन",
        "about": "प्रकल्पाबद्दल",
        "about_text": "कोणतेही स्थान टाइप करा आणि नकाशा सह भूस्खलन जोखीम अंदाज मिळवा.",
        "location": "📍 कोणतेही स्थान प्रविष्ट करा",
        "placeholder": "शहराचे नाव लिहा (उदाहरण: लखनौ, गँगटोक, दार्जिलिंग)",
        "params": "🔢 पर्यावरणीय पॅरामीटर्स",
        "rainfall": "🌧️ पर्जन्य (मिमी)",
        "slope": "📐 उतार कोन (अंश)",
        "moisture": "💧 मातीची आर्द्रता (0-1)",
        "elevation": "⛰️ उंची (मीटर)",
        "button": "🔍 जोखीम अंदाज लावा आणि नकाशा दाखवा",
        "result": "📊 अंदाज परिणाम",
        "high_risk": "🚨 भूस्खलनाचा उच्च धोका आढळला",
        "low_risk": "✅ कमी धोका - परिस्थिती सध्या स्थिर आहे",
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
        "lang": "भाषा निवडा"
    }
}

# ====================== LANGUAGE SELECT ======================
lang = st.sidebar.selectbox("🌐 Select Language / भाषा चुनें", 
                            ["English", "Hindi", "Bengali", "Tamil", "Telugu", "Marathi"])

t = translations[lang]

st.title(t["title"])
st.markdown(f"**{t['subtitle']}**")
st.markdown("---")

# Load data & model
data = pd.read_csv("data.csv")
X = data[["rainfall_mm", "slope_angle", "soil_moisture", "elevation"]]
y = data["landslide"]
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X, y)

# Sidebar
st.sidebar.header(t["about"])
st.sidebar.write(t["about_text"])
st.sidebar.write("**Problem:** SIH26001")
st.sidebar.write("CSE Department | KMCLU")

# Session state
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

# Location
st.subheader(t["location"])
location_name = st.text_input(t["placeholder"], placeholder=t["placeholder"])

if location_name:
    try:
        geolocator = Nominatim(user_agent="landslide_app")
        location = geolocator.geocode(location_name, timeout=10)
        if location:
            st.session_state.lat = location.latitude
            st.session_state.lon = location.longitude
            st.session_state.loc_name = location_name
            st.success(f"{location.address}")
        else:
            st.warning("Location not found / स्थान नहीं मिला")
    except:
        st.warning("Could not fetch location")

st.markdown("---")

# Parameters
st.subheader(t["params"])
c1, c2 = st.columns(2)
with c1:
    rainfall = st.slider(t["rainfall"], 0, 300, 120)
    slope = st.slider(t["slope"], 0, 60, 28)
with c2:
    moisture = st.slider(t["moisture"], 0.0, 1.0, 0.50)
    elevation = st.slider(t["elevation"], 100, 3000, 800)

st.markdown("---")

# Button
if st.button(t["button"], use_container_width=True):
    input_data = [[rainfall, slope, moisture, elevation]]
    st.session_state.prediction = model.predict(input_data)[0]
    st.session_state.probability = model.predict_proba(input_data)[0][1] * 100
    st.session_state.predicted = True

# Result
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
        
        # Alarm sound
        try:
            st.audio("alarm.mp3", format="audio/mp3", start_time=0)
            st.markdown("🔊 **Alarm Playing...**")
        except:
            st.warning("Alarm sound file not found")
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

    # Map
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
st.caption("AI Landslide Early Warning System | SIH 2026 | CSE Department, KMCLU")