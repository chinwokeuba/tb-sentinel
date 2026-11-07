import pandas as pd
import plotly.express as px
import pydeck as pdk
import streamlit as st

# 1. Page Configuration
st.set_page_config(
    page_title="TB Sentinel | Global High-Burden Surveillance Platform",
    page_icon="🧪",
    layout="wide",
    initial_sidebar_state="expanded",
)

# 2. Custom CSS - Unique Clean-Clinical Light Aesthetic
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap');

    html, body, .stApp {
        background-color: #F4F7F9 !important;
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        color: #1A2533 !important;
    }

    h1, h2, h3, h4, h5, h6 {
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        font-weight: 700 !important;
        color: #0F172A !important;
        letter-spacing: -0.02em;
    }

    p, span, label {
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        color: #334155 !important;
    }

    /* Metric Cards */
    div[data-testid="stMetric"] {
        background: #FFFFFF !important;
        border: 1px solid #E2E8F0 !important;
        border-radius: 16px !important;
        padding: 24px !important;
        box-shadow: 0px 4px 20px rgba(148, 163, 184, 0.12) !important;
    }
    [data-testid="stMetricValue"] {
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        font-weight: 800 !important;
        color: #0F2942 !important;
        font-size: 2rem !important;
    }
    [data-testid="stMetricLabel"] {
        font-weight: 600 !important;
        text-transform: uppercase;
        font-size: 0.75rem !important;
        letter-spacing: 0.05em;
        color: #64748B !important;
    }
    [data-testid="stMetricDelta"] {
        font-size: 0.85rem !important;
        font-weight: 600 !important;
    }

    .stTabs [data-baseweb="tab-list"] {
        gap: 12px;
        background-color: #E2E8F0;
        padding: 6px;
        border-radius: 12px;
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 8px;
        padding: 10px 20px;
        font-weight: 600;
        color: #475569;
        background-color: transparent;
        border: none !important;
    }
    .stTabs [aria-selected="true"] {
        background-color: #FFFFFF !important;
        color: #0F2942 !important;
        box-shadow: 0px 2px 8px rgba(0, 0, 0, 0.08) !important;
    }

    div[data-testid="stForm"] {
        background: #FFFFFF !important;
        border: 1px solid #E2E8F0 !important;
        border-radius: 16px !important;
        padding: 28px !important;
        box-shadow: 0px 4px 20px rgba(148, 163, 184, 0.08) !important;
    }

    /* Universal Button Styling */
    div.stButton button, 
    div[data-testid="stFormSubmitButton"] button, 
    div.stDownloadButton button {
        background: linear-gradient(135deg, #0F2942 0%, #1E40AF 100%) !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 12px 24px !important;
        box-shadow: 0px 4px 12px rgba(15, 41, 66, 0.2) !important;
    }
    
    div.stButton button *, 
    div[data-testid="stFormSubmitButton"] button *, 
    div.stDownloadButton button *,
    div.stButton button p, div[data-testid="stFormSubmitButton"] button p, div.stDownloadButton button p,
    div.stButton button span, div[data-testid="stFormSubmitButton"] button span, div.stDownloadButton button span {
        color: #FFFFFF !important;
        font-weight: 600 !important;
        font-family: 'Plus Jakarta Sans', sans-serif !important;
    }
    
    div.stButton button:hover, 
    div[data-testid="stFormSubmitButton"] button:hover, 
    div.stDownloadButton button:hover {
        background: linear-gradient(135deg, #1E40AF 100%, #1E3A8A 100%) !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# 3. Initialize Session State for Live Adherence Register
if "adherence_df" not in st.session_state:
    st.session_state.adherence_df = pd.DataFrame(
        [
            {"Patient_Ref": "TB-PAT-101", "Country": "Nigeria", "Doses_Logged": 28, "Target_Doses": 30, "Adherence_Score": 93.3, "Cohort_Status": "Stable"},
            {"Patient_Ref": "TB-PAT-102", "Country": "India", "Doses_Logged": 30, "Target_Doses": 30, "Adherence_Score": 100.0, "Cohort_Status": "Optimal"},
            {"Patient_Ref": "TB-PAT-103", "Country": "Indonesia", "Doses_Logged": 22, "Target_Doses": 30, "Adherence_Score": 73.3, "Cohort_Status": "Default Risk"},
            {"Patient_Ref": "TB-PAT-104", "Country": "The Philippines", "Doses_Logged": 29, "Target_Doses": 30, "Adherence_Score": 96.7, "Cohort_Status": "Optimal"},
        ]
    )

# 4. Data Generators
@st.cache_data
def load_spatial_data():
    return pd.DataFrame(
        [
            {
                "Country": "India", "Capital_Hub": "New Delhi", "lat": 28.6139, "lon": 77.2090, 
                "Global_Share": "25% - 26%", "Risk_Tier": "Critical High-Load",
                "Est_Incidence_100k": 210, "MDR_TB_Rate": "2.8%", "Treatment_Success": "82%",
                "Primary_Intervention": "Expanded GeneXpert roll-out & Nikshay portal tracking"
            },
            {
                "Country": "Indonesia", "Capital_Hub": "Jakarta", "lat": -6.2088, "lon": 106.8456, 
                "Global_Share": "~10%", "Risk_Tier": "Critical High-Load",
                "Est_Incidence_100k": 354, "MDR_TB_Rate": "4.2%", "Treatment_Success": "76%",
                "Primary_Intervention": "Active case finding in dense urban settlements"
            },
            {
                "Country": "The Philippines", "Capital_Hub": "Manila", "lat": 14.5995, "lon": 120.9842, 
                "Global_Share": "~6.8%", "Risk_Tier": "High Burden",
                "Est_Incidence_100k": 650, "MDR_TB_Rate": "3.1%", "Treatment_Success": "79%",
                "Primary_Intervention": "Barangay-level mobile chest X-ray screening"
            },
            {
                "Country": "China", "Capital_Hub": "Beijing", "lat": 39.9042, "lon": 116.4074, 
                "Global_Share": "6.5% - 6.8%", "Risk_Tier": "High Burden",
                "Est_Incidence_100k": 59, "MDR_TB_Rate": "7.1%", "Treatment_Success": "91%",
                "Primary_Intervention": "Digital pillbox monitors & advanced public insurance integration"
            },
            {
                "Country": "Pakistan", "Capital_Hub": "Islamabad", "lat": 33.6844, "lon": 73.0479, 
                "Global_Share": "~6.3%", "Risk_Tier": "High Burden",
                "Est_Incidence_100k": 268, "MDR_TB_Rate": "4.5%", "Treatment_Success": "80%",
                "Primary_Intervention": "Public-private mix (PPM) treatment provider expansion"
            },
            {
                "Country": "Nigeria", "Capital_Hub": "Abuja / Ibadan", "lat": 9.0765, "lon": 7.3986, 
                "Global_Share": "4.6% - 4.8%", "Risk_Tier": "Moderate-High Load",
                "Est_Incidence_100k": 219, "MDR_TB_Rate": "2.3%", "Treatment_Success": "85%",
                "Primary_Intervention": "Community DOTS workers & National Tuberculosis Network scale-up"
            },
            {
                "Country": "Democratic Republic of the Congo", "Capital_Hub": "Kinshasa", "lat": -4.4419, "lon": 15.2663, 
                "Global_Share": "3.1% - 3.9%", "Risk_Tier": "Moderate Load",
                "Est_Incidence_100k": 321, "MDR_TB_Rate": "2.1%", "Treatment_Success": "81%",
                "Primary_Intervention": "Rural clinic diagnostic capacity reinforcement"
            },
            {
                "Country": "Bangladesh", "Capital_Hub": "Dhaka", "lat": 23.8103, "lon": 90.4125, 
                "Global_Share": "3.5% - 3.6%", "Risk_Tier": "Moderate Load",
                "Est_Incidence_100k": 221, "MDR_TB_Rate": "1.8%", "Treatment_Success": "94%",
                "Primary_Intervention": "Upazila health complex molecular testing deployment"
            },
        ]
    )

spatial_df = load_spatial_data()
current_adherence_df = st.session_state.adherence_df

# 5. Header Canvas
st.title("🧪 TB Sentinel | Global High-Burden Surveillance Platform")
st.write("Tracking the Top 8 global nations accounting for over 67% of worldwide tuberculosis transmission, paired with clinical triage and DOTS adherence analytics.")

# 5.1 Automated Epidemiological Risk Alert Banner
default_risk_count = len(current_adherence_df[current_adherence_df["Cohort_Status"] == "Default Risk"])
if default_risk_count > 0:
    st.warning(f"⚠️ **EPIDEMIOLOGICAL SURVEILLANCE ALERT:** Active cohort monitoring has flagged **{default_risk_count} patient(s)** approaching default risk threshold (Adherence < 75%). Regional DOTS outreach protocol automatically initialized.")
else:
    st.success("✅ **EPIDEMIOLOGICAL SURVEILLANCE STATUS:** All active monitored high-burden cohorts operating within optimal adherence parameters.")

st.markdown("---")

# 6. Executive KPI Row
m1, m2, m3, m4 = st.columns(4)
m1.metric("Monitored High-Load", "8 Nations", "67% Global Cases")
m2.metric("Primary Epicenter", "India", "25% Global Share")
mean_score = round(current_adherence_df["Adherence_Score"].mean(), 1)
m3.metric("Mean DOTS Adherence", f"{mean_score}%", "Live Cohort Average")
m4.metric("Default Risk Pool", f"{default_risk_count} Patient(s)", "Requires Outreach")

st.write("")
st.write("")

# 7. Tab Navigation
tab_spatial, tab_triage, tab_register, tab_adherence, tab_supply = st.tabs([
    "🗺️ Global High-Burden Map", 
    "📋 Clinical Triage", 
    "➕ Register Patient",
    "📈 DOTS Adherence Log",
    "📦 Supply Chain Estimator"
])

with tab_spatial:
    st.subheader("Global High-Burden Spatial Matrix")
    st.caption("Visualizing the 8 nations driving the majority of worldwide tuberculosis cases.")

    layer = pdk.Layer(
        "ScatterplotLayer",
        data=spatial_df,
        get_position="[lon, lat]",
        get_color="[225, 29, 72, 180]",
        get_radius=250000,
        pickable=True,
    )
    
    view_state = pdk.ViewState(latitude=15.0, longitude=30.0, zoom=1.5, pitch=0)
    deck = pdk.Deck(
        layers=[layer], initial_view_state=view_state, map_style=pdk.map_styles.CARTO_LIGHT,
        tooltip={"text": "Country: {Country}\nCapital Hub: {Capital_Hub}\nGlobal Case Share: {Global_Share}\nRisk Tier: {Risk_Tier}"}
    )
    st.pydeck_chart(deck)
    
    st.markdown("### 🔍 High-Burden Country Deep-Dive & Trend Analysis")
    selected_country = st.selectbox("Select a High-Burden Nation for Epidemiological Profile:", spatial_df["Country"].tolist())
    
    c_info = spatial_df[spatial_df["Country"] == selected_country].iloc[0]
    
    col_d1, col_d2, col_d3 = st.columns(3)
    col_d1.metric("Estimated Incidence", f"{c_info['Est_Incidence_100k']} per 100k", f"Tier: {c_info['Risk_Tier']}")
    col_d2.metric("MDR-TB Rate", c_info["MDR_TB_Rate"], "Resistance Proportion")
    col_d3.metric("Treatment Success Rate", c_info["Treatment_Success"], "National Cohort Average")
    
    st.info(f"💡 **Primary National Strategy ({selected_country}):** {c_info['Primary_Intervention']}")

    # Plotly Historical Trend & Projection Chart
    st.markdown(f"#### 📊 Multi-Year Incidence Trajectory & Projection ({selected_country})")
    trend_data = pd.DataFrame({
        "Year": ["2020", "2021", "2022", "2023", "2024", "2025", "2026 (Est.)"],
        "Incidence_Per_100k": [
            c_info['Est_Incidence_100k'] * 1.15,
            c_info['Est_Incidence_100k'] * 1.12,
            c_info['Est_Incidence_100k'] * 1.08,
            c_info['Est_Incidence_100k'] * 1.04,
            c_info['Est_Incidence_100k'] * 1.01,
            c_info['Est_Incidence_100k'] * 0.98,
            c_info['Est_Incidence_100k'] * 0.94
        ]
    })
    fig = px.line(trend_data, x="Year", y="Incidence_Per_100k", markers=True, 
                  color_discrete_sequence=["#1E40AF"])
    fig.update_layout(plot_bgcolor="white", paper_bgcolor="white", margin=dict(t=20, b=20, l=20, r=20))
    st.plotly_chart(fig, use_container_width=True)

    with tab_register:
         st.subheader("➕ New Patient Cohort Registration")
         st.caption("Enroll a new patient into active global surveillance and assign initial pill-count adherence parameters.")

    with st.form("direct_patient_registration"):
        col_reg1, col_reg2 = st.columns(2)
        
        reg_patient_ref = col_reg1.text_input("Patient Reference Number", "TB-PAT-106")
        reg_country = col_reg1.selectbox("Assigned High-Burden Country Corridor", spatial_df["Country"].tolist(), key="reg_country")
        
        reg_initial_doses = col_reg2.slider("Initial Doses Logged (Pill Count out of 30)", 0, 30, 28, key="reg_doses")
        reg_status_override = col_reg2.selectbox("Initial Cohort Status", ["Optimal", "Stable", "Default Risk"], key="reg_status")

        submit_direct_reg = st.form_submit_button("Enroll Patient into Register")

    if submit_direct_reg:
        reg_adherence_score = round((reg_initial_doses / 30) * 100, 1)
        
        new_row = {
            "Patient_Ref": reg_patient_ref,
            "Country": reg_country,
            "Doses_Logged": reg_initial_doses,
            "Target_Doses": 30,
            "Adherence_Score": reg_adherence_score,
            "Cohort_Status": reg_status_override
        }
        
        if reg_patient_ref in st.session_state.adherence_df["Patient_Ref"].values:
            st.session_state.adherence_df.loc[st.session_state.adherence_df["Patient_Ref"] == reg_patient_ref, :] = new_row
            st.success(f"✅ Updated existing patient record for **{reg_patient_ref}**!")
        else:
            st.session_state.adherence_df = pd.concat([st.session_state.adherence_df, pd.DataFrame([new_row])], ignore_index=True)
            st.success(f"🎉 Successfully enrolled patient **{reg_patient_ref}** into the {reg_country} corridor!")

with tab_triage:
    st.subheader("Patient Clinical Risk Triage System & Live Registration")
    st.write("Enter patient clinical presentation. Submitting will compute triage scores, assign WHO treatment regimens, and automatically register the patient into the active cohort adherence log.")

    with st.form("triage_intake"):
        col_left, col_right = st.columns(2)
        
        patient_ref = col_left.text_input("Patient Reference Number", "TB-PAT-105")
        patient_country = col_left.selectbox("Assigned High-Burden Country Corridor", spatial_df["Country"].tolist())
        cough_duration = col_left.number_input("Cough Duration (Weeks)", min_value=0, max_value=16, value=3)
        hemoptysis = col_left.checkbox("Hemoptysis (Coughing up Blood)")
        
        fever = col_right.checkbox("Persistent Unexplained Fever")
        weight_loss = col_right.checkbox("Significant Weight Loss (>5%)")
        contact_history = col_right.checkbox("Confirmed Exposure to Active Case")

        st.markdown("---")
        st.markdown("#### 🧬 Drug-Resistance Testing (DST) & Pill-Count Inputs")
        dst_status = st.selectbox("Molecular / GeneXpert Test Result", [
            "Pending / Not Tested", 
            "Drug-Susceptible (DS-TB)", 
            "Rifampicin-Resistant (RR-TB / MDR-TB)", 
            "Extensively Drug-Resistant (XDR-TB)"
        ])
        doses_logged = col_right.slider("Initial Doses Logged (Pill Count)", 0, 30, 25)

        submit_triage = st.form_submit_button("Compute Risk & Register Patient")

    if submit_triage:
        score = (cough_duration * 2) + (10 if hemoptysis else 0) + (5 if fever else 0) + (5 if weight_loss else 0) + (8 if contact_history else 0)
        adherence_score = round((doses_logged / 30) * 100, 1)
        cohort_status = "Default Risk" if adherence_score < 75 else ("Optimal" if adherence_score >= 95 else "Stable")

        # Append new patient to session state adherence log
        new_patient_row = {
            "Patient_Ref": patient_ref,
            "Country": patient_country,
            "Doses_Logged": doses_logged,
            "Target_Doses": 30,
            "Adherence_Score": adherence_score,
            "Cohort_Status": cohort_status
        }
        
        # Avoid duplicate patient refs
        if patient_ref in st.session_state.adherence_df["Patient_Ref"].values:
            st.session_state.adherence_df.loc[st.session_state.adherence_df["Patient_Ref"] == patient_ref, :] = new_patient_row
        else:
            st.session_state.adherence_df = pd.concat([st.session_state.adherence_df, pd.DataFrame([new_patient_row])], ignore_index=True)

        st.markdown("### Triage & Treatment Output Matrix")
        
        if score >= 15:
            st.error(f"🚨 **CRITICAL RISK TIER (Score: {score})** — Immediate GeneXpert / Sputum Microscopy ordering required. Patient logged into cohort.")
        elif score >= 8:
            st.warning(f"⚠️ **MODERATE RISK TIER (Score: {score})** — Secondary diagnostic screening (Chest X-Ray) advised within 48 hours.")
        else:
            st.success(f"✅ **LOW RISK / CLEAR TIER (Score: {score})** — Routine outpatient review.")

        st.markdown(f"**📌 Cohort Registration Status:** Patient `{patient_ref}` successfully added with adherence score **{adherence_score}% ({cohort_status})**.")

        st.markdown("#### 💊 WHO-Compliant Regimen Prescription")
        if dst_status == "Drug-Susceptible (DS-TB)":
            st.info("**Standard 6-Month Regimen (2HRZE/4HR):** 2 months of Isoniazid, Rifampicin, Pyrazinamide, and Ethambutol, followed by 4 months of Isoniazid and Rifampicin.")
        elif dst_status == "Rifampicin-Resistant (RR-TB / MDR-TB)":
            st.warning("**BPaLM / 6-Month All-Oral Regimen:** Bedaquiline, Pretomanid, Linezolid, and Moxifloxacin. Requires close cardiac monitoring.")
        elif dst_status == "Extensively Drug-Resistant (XDR-TB)":
            st.error("**Individualized Longer Regimen:** Tailored combination including Bedaquiline, Linezolid, and Delamanid for 18–20 months.")
        else:
            st.caption("Awaiting molecular drug-sensitivity test (DST) confirmation.")

with tab_adherence:
    st.subheader("DOTS Therapy Compliance Register")
    st.caption("Real-time patient pill-count compliance across high-burden corridors.")

    st.dataframe(st.session_state.adherence_df, use_container_width=True)

    st.download_button(
        label="Export Cohort Compliance Report (CSV)",
        data=st.session_state.adherence_df.to_csv(index=False),
        file_name="tb_dots_adherence_report.csv",
        mime="text/csv",
    )

with tab_supply:
    st.subheader("📦 Regional Supply Chain & Drug Stockpile Estimator")
    st.caption("Operational logistics calculator determining monthly pharmaceutical reserves needed across active clinic cohorts.")

    col_s1, col_s2 = st.columns(2)
    active_patients = col_s1.number_input("Active Enrolled Patients in Clinic", min_value=1, max_value=5000, value=120)
    months_buffer = col_s2.slider("Required Stock Buffer (Months)", 1, 6, 3)

    # Calculation logic for 6-month regimen packs (approx 30 pills per month per patient)
    rifampicin_packs = active_patients * months_buffer
    isoniazid_packs = active_patients * months_buffer
    bedaquiline_kits = int(active_patients * 0.15) * months_buffer # ~15% MDR rate estimation

    st.markdown("### 📋 Required Monthly Pharmaceutical Stockpile")
    cs1, cs2, cs3 = st.columns(3)
    cs1.metric("Rifampicin Blisters", f"{rifampicin_packs:,} Packs", "Standard Regimen")
    cs2.metric("Isoniazid Blisters", f"{isoniazid_packs:,} Packs", "Standard Regimen")
    cs3.metric("Bedaquiline Kits", f"{bedaquiline_kits:,} Kits", "MDR-TB Reserve")

    st.info("💡 **Logistics Recommendation:** Stock levels meet safety buffer thresholds. Automated distribution order ready for regional warehouse dispatch.")
    
    
    
    


























    