# 🧪 TB Sentinel | Global High-Burden Tuberculosis Surveillance & Clinical Triage Platform

**TB Sentinel** is an advanced, production-grade epidemiological intelligence and clinical workflow platform designed to monitor, triage, and manage tuberculosis (TB) surveillance across the 8 global high-burden nations responsible for over 67% of worldwide transmission. 

Built with **Python** and **Streamlit**, the application bridges high-level spatial epidemiology with practical, patient-level clinical decision support and supply chain logistics.

---

## 🚀 Key Features & Architectural Modules

1. **🗺️ Global High-Burden Spatial Matrix**
   * Powered by **Pydeck**, mapping critical epicenter coordinates and visualizing risk tiers, national incidence rates, and multi-year trajectory trends.
   * Interactive country deep-dive panels displaying MDR-TB proportions and national intervention strategies.

2. **📊 Historical & Projected Trends (Plotly Integration)**
   * Multi-year epidemiological incidence tracking charts to analyze past trajectories and forecasted intervention impacts.

3. **📋 Clinical Triage & Risk Scoring Engine**
   * Multi-parameter clinician intake evaluating symptom duration, clinical markers (hemoptysis, fever, weight loss), and exposure history to compute real-time risk tiers.
   * Automated WHO-compliant regimen prescribing (DS-TB standard courses, BPaLM regimens for MDR-TB, and individualized XDR protocols).

4. **➕ Live Session State Patient Registration**
   * Seamlessly transitions evaluated patients from the triage workflow directly into active cohort registers in real time.

5. **📈 DOTS Therapy Compliance Register**
   * Live pill-count tracking, adherence percentage calculations, automated risk alerting for default thresholds (<75%), and CSV report export functionality.

6. **📦 Regional Supply Chain & Drug Stockpile Estimator**
   * Operational logistics calculator ensuring regional clinics maintain optimal pharmaceutical reserves (Rifampicin, Isoniazid, Bedaquiline) to prevent stockouts.

---

## 🛠️ Tech Stack
* **Core Language:** Python
* **Web Framework:** Streamlit
* **Spatial Visualization:** PyDeck (CARTO Light theme)
* **Analytical Plotting:** Plotly Express
* **Data Manipulation & State:** Pandas, Streamlit Session State

---

## 💻 Local Installation & Setup

To run this repository locally on your machine:

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/YOUR-USERNAME/tb-sentinel.git](https://github.com/YOUR-USERNAME/tb-sentinel.git)
   cd tb-sentinel
