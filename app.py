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

# ====================== SIDEBAR ======================
st.sidebar.title("⚠️ Bilal’s Sentinel")
st.sidebar.caption("AI Landslide Early Warning System")
st.sidebar.markdown("---")

page = st.sidebar.radio(
    "Go to page",
    ["🏠 Home", "🔍 Risk Prediction", "🛡️ Safety Guidelines", "🚨 Emergency Actions"]
)

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

    st.markdown("---")
    st.success("👉 Open **Risk Prediction** page from the left sidebar to try the system.")

# ====================== PAGE 2: RISK PREDICTION ======================
elif page == "🔍 Risk Prediction":
    st.title("🔍 Risk Prediction")
    st.markdown("Enter location and parameters to get landslide risk assessment.")
    st.markdown("---")

    # Load data & model
    try:
        data = pd.read_csv("data.csv")
        X = data[["rainfall_mm", "slope_angle", "soil_moisture", "elevation"]]
        y = data["landslide"]
        model = RandomForestClassifier(n_estimators=100, random_state=42)
        model.fit(X, y)
    except Exception as e:
        st.error("Error loading data.csv. Make sure the file is in the repository.")
        st.stop()

    # Location
    st.subheader("📍 Enter Location")
    location_name = st.text_input(
        "City / Place name",
        placeholder="Example: Gangtok, Darjeeling, Manali, Shimla, Lucknow"
    )

    if location_name:
        try:
            geolocator = Nominatim(user_agent="bilal_sentinel_app")
            location = geolocator.geocode(location_name, timeout=10)
            if location:
                st.session_state.lat = location.latitude
                st.session_state.lon = location.longitude
                st.session_state.loc_name = location_name
                st.success(f"✅ Found: {location.address}")
            else:
                st.warning("Location not found. Try a simpler name.")
        except Exception:
            st.warning("Could not fetch location. Check internet connection.")

    st.markdown("---")
    st.subheader("🔢 Environmental Parameters")

    col1, col2 = st.columns(2)
    with col1:
        rainfall = st.slider("🌧️ Rainfall (mm)", 0, 300, 120)
        slope = st.slider("📐 Slope Angle (degrees)", 0, 60, 28)
    with col2:
        moisture = st.slider("💧 Soil Moisture (0-1)", 0.0, 1.0, 0.50)
        elevation = st.slider("⛰️ Elevation (meters)", 100, 3000, 800)

    st.markdown("---")

    if st.button("🔍 Predict Risk & Show Map", use_container_width=True, type="primary"):
        input_data = [[rainfall, slope, moisture, elevation]]
        st.session_state.prediction = int(model.predict(input_data)[0])
        st.session_state.probability = float(model.predict_proba(input_data)[0][1] * 100)
        st.session_state.predicted = True

    # Result
    if st.session_state.predicted:
        st.subheader("📊 Prediction Result")

        if st.session_state.loc_name:
            st.write(f"**Location:** {st.session_state.loc_name}")

        if st.session_state.prediction == 1:
            st.error("🚨 HIGH RISK of Landslide Detected")
            st.metric("Risk Probability", f"{st.session_state.probability:.1f}%")

            st.warning("""
            **Immediate Actions:**
            - Evacuate people from steep slopes and low-lying areas  
            - Inform local District Disaster Management Authority  
            - Avoid travel on hilly roads  
            - Continuously monitor rainfall  
            """)

            map_color = "red"
            risk_text = "HIGH RISK"

            components.html("""
                <script>
                    var msg = new SpeechSynthesisUtterance("Warning! High risk of landslide detected. Please take immediate action.");
                    msg.lang = "en-IN";
                    msg.rate = 0.9;
                    window.speechSynthesis.speak(msg);
                </script>
            """, height=0)

        else:
            st.success("✅ LOW RISK — Situation Currently Stable")
            st.metric("Risk Probability", f"{st.session_state.probability:.1f}%")

            st.info("""
            **Current Status:**
            - Conditions are within safe limits  
            - Continue regular monitoring  
            - Stay alert during heavy rainfall  
            """)

            map_color = "green"
            risk_text = "LOW RISK"

            components.html("""
                <script>
                    var msg = new SpeechSynthesisUtterance("You are safe. Situation is currently stable.");
                    msg.lang = "en-IN";
                    msg.rate = 0.9;
                    window.speechSynthesis.speak(msg);
                </script>
            """, height=0)

        # Map
        st.subheader("🗺️ Location Map")
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
            st.info("Enter a valid location name above to see the map.")

# ====================== PAGE 3: SAFETY GUIDELINES ======================
elif page == "🛡️ Safety Guidelines":
    st.title("🛡️ Safety Guidelines")
    st.markdown("What to do **before, during and after** a landslide.")
    st.markdown("---")

    st.subheader("1️⃣ Before a Landslide (Preparedness)")
    st.write("""
    - Know whether your area is landslide-prone (especially if you live on or near slopes)  
    - Prepare a small emergency kit (torch, water, first-aid, important documents, power bank)  
    - Save emergency contact numbers in your phone  
    - Avoid building or staying on steep / unstable slopes  
    - Maintain vegetation and trees on slopes  
    - Follow IMD and local administration rainfall warnings  
    """)

    st.subheader("2️⃣ When Landslide is About to Happen / During Heavy Rain")
    st.warning("""
    **Most Important — Act Fast:**
    - Move immediately to higher and safer ground  
    - Stay away from the path of possible landslide (slopes, valleys, streams)  
    - Do not waste time collecting belongings if the situation is urgent  
    - Alert neighbours and help children & elderly  
    - Listen to official alerts on radio / phone  
    """)

    st.subheader("3️⃣ After a Landslide")
    st.write("""
    - Stay away from the slide area — more slides can still occur  
    - Check for injured people and give first aid only if you are trained  
    - Report the incident to local disaster management / police  
    - Do not drink water from nearby streams (may be contaminated)  
    - Wait for official clearance before returning home  
    """)

    st.markdown("---")
    st.info("**Golden Rule:** Life first. Property can be replaced. If you feel the ground moving or hear unusual rumbling / cracking sounds, leave the area immediately.")

# ====================== PAGE 4: EMERGENCY ACTIONS ======================
elif page == "🚨 Emergency Actions":
    st.title("🚨 Emergency Actions")
    st.markdown("If a landslide is about to happen — **what should you do first?**")
    st.markdown("---")

    st.error("### 🔴 FIRST PRIORITY — SAVE LIFE")
    st.write("""
    1. **Evacuate immediately** to higher, safer ground  
    2. **Do not wait** to collect valuables  
    3. Help children, elderly and differently-abled persons first  
    4. Move away from the direction of the slope / flow  
    5. Call emergency numbers and inform authorities  
    """)

    st.markdown("---")

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Do’s ✅")
        st.success("""
        - Move to higher ground as fast as possible  
        - Stay together with family members  
        - Follow official evacuation instructions  
        - Keep phone charged and share location if possible  
        - Wear sturdy shoes  
        """)

    with col2:
        st.subheader("Don’ts ❌")
        st.error("""
        - Do not go near the edge of the slope to watch  
        - Do not take shelter under trees or weak structures on the slope  
        - Do not drive through cracked or blocked roads  
        - Do not return until authorities say it is safe  
        - Do not spread unverified information  
        """)

    st.markdown("---")
    st.subheader("📞 Important Helpline Numbers (India)")
    st.write("""
    - **National Emergency Number:** 112  
    - **Disaster Management:** 1078 / 1070  
    - **Police:** 100  
    - **Ambulance:** 108 / 102  
    - **Fire:** 101  
    """)

    st.info("Save these numbers. In hilly areas also keep your local SDM / District Control Room number.")

# ====================== FOOTER ======================
st.markdown("---")
st.caption("Bilal’s Sentinel | AI Landslide Early Warning System | Developed by Bilal Ali | SIH 2026")
           
      
