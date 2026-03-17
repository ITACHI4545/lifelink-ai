from sklearn.linear_model import LinearRegression
import numpy as np
import streamlit as st
import math

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="LifeLink AI", layout="wide")

# ---------------- CUSTOM UI ----------------
st.markdown("""
    <style>
        .main {
            background-color: #0e1117;
        }
        h1, h2, h3, h4 {
            color: white;
        }
        .stButton>button {
            background-color: #ff4b4b;
            color: white;
            border-radius: 10px;
            height: 50px;
            width: 100%;
            font-size: 18px;
        }
        .card {
            padding: 15px;
            border-radius: 12px;
            background-color: #1c1f26;
            margin-bottom: 12px;
            box-shadow: 0px 0px 10px rgba(255,75,75,0.2);
        }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h1>🩸 LifeLink AI</h1>", unsafe_allow_html=True)
st.markdown("<h3>🚑 Intelligent Blood Allocation System</h3>", unsafe_allow_html=True)

# ---------------- ML MODEL ----------------
X = np.array([
    [1, 200],
    [2, 150],
    [3, 100],
    [4, 80],
    [5, 50]
])

y = np.array([9, 8, 7, 5, 3])

model = LinearRegression()
model.fit(X, y)

# ---------------- INPUT SECTION ----------------
col1, col2, col3 = st.columns(3)

with col1:
    blood_group = st.selectbox("🩸 Blood Group", ["A+", "B+", "AB+", "O+"])

with col2:
    user_lat = st.number_input("📍 Latitude", value=28.61)

with col3:
    user_lon = st.number_input("📍 Longitude", value=77.20)

# ---------------- DISTANCE FUNCTION ----------------
def calculate_distance(lat1, lon1, lat2, lon2):
    R = 6371
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat/2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    return R * c

# ---------------- DATA ----------------
blood_banks = [
    {"name": "AIIMS", "lat": 28.5672, "lon": 77.2100, "A+": 5, "B+": 2, "AB+": 1, "O+": 4},
    {"name": "Red Cross", "lat": 28.6139, "lon": 77.2090, "A+": 0, "B+": 3, "AB+": 2, "O+": 1}
]

donors = [
    {"name": "Raj", "lat": 28.61, "lon": 77.20, "blood": "A+", "last_donation": 120},
    {"name": "Aman", "lat": 28.62, "lon": 77.21, "blood": "A+", "last_donation": 200},
    {"name": "Neha", "lat": 28.60, "lon": 77.19, "blood": "A+", "last_donation": 90}
]

# ---------------- AI SCORING ----------------
def donor_score(distance, last_donation):
    return model.predict([[distance, last_donation]])[0]

# ---------------- BUTTON ----------------
if st.button("🔍 Find Best Source"):

    bank_results = []
    for bank in blood_banks:
        if bank[blood_group] > 0:
            dist = calculate_distance(user_lat, user_lon, bank["lat"], bank["lon"])
            bank_results.append((dist, bank))

    bank_results.sort(key=lambda x: x[0])

    donor_results = []
    for d in donors:
        if d["blood"] == blood_group:
            dist = calculate_distance(user_lat, user_lon, d["lat"], d["lon"])
            score = donor_score(dist, d["last_donation"])
            donor_results.append((score, dist, d))

    donor_results.sort(key=lambda x: x[0], reverse=True)

    # ---------------- AI DECISION ----------------
    st.markdown("## 🧠 AI Decision")

    if bank_results:
        best_bank_dist = bank_results[0][0]
    else:
        best_bank_dist = float('inf')

    if donor_results:
        best_donor_score, best_donor_dist, best_donor = donor_results[0]
    else:
        best_donor_dist = float('inf')

    if best_bank_dist < best_donor_dist:
        st.success("🏥 Recommended: Blood Bank (Fastest & Reliable)")
    else:
        st.success("🧑 Recommended: Donor (Closer & Suitable)")

    # ---------------- DISPLAY ----------------
    col1, col2 = st.columns(2)

    # Blood Banks
    with col1:
        st.markdown("### 🏥 Blood Banks")
        if bank_results:
            for dist, bank in bank_results[:2]:
                st.markdown(f"""
                <div class="card">
                    <h4>{bank['name']}</h4>
                    <p>📍 Distance: {round(dist,2)} km</p>
                    <p>🩸 Units Available: {bank[blood_group]}</p>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.warning("No blood banks available")

    # Donors
    with col2:
        st.markdown("### 🧑 Donors")
        if donor_results:
            for score, dist, d in donor_results[:3]:
                st.markdown(f"""
                <div class="card">
                    <h4>{d['name']}</h4>
                    <p>📍 Distance: {round(dist,2)} km</p>
                    <p>🕒 Last Donation: {d['last_donation']} days</p>
                    <p>🤖 AI Score: {round(score,2)}</p>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.warning("No donors found")
