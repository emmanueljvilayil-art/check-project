import streamlit as st
import pandas as pd
import pickle
import shap
import matplotlib.pyplot as plt
from fpdf import FPDF
from datetime import datetime

# --- PAGE CONFIG ---
st.set_page_config(page_title="AI Multi-Disease Diagnostic", layout="wide")

# --- MOCK MODEL LOADING (For Demo Purposes) ---
# In a real scenario, you'd use: model = pickle.load(open('models/heart.pkl', 'rb'))
def mock_predict(data, disease_type):
    # Simulating a probability for the demo
    import numpy as np
    return np.random.uniform(0.1, 0.8)

# --- UI HEADER ---
st.title("🏥 AI-Powered Multi-Disease Health Suite")
st.markdown("Enter your vitals below for a comprehensive risk assessment.")

# --- SIDEBAR / INPUTS ---
with st.sidebar:
    st.header("👤 Patient Demographics")
    age = st.number_input("Age", 1, 120, 25)
    gender = st.selectbox("Gender", ["Male", "Female"])
    bmi = st.slider("BMI", 10.0, 50.0, 22.5)
    
    st.header("🩺 Clinical Vitals")
    glucose = st.number_input("Glucose Level", 50, 300, 100)
    bp = st.number_input("Blood Pressure (systolic)", 80, 200, 120)
    chol = st.number_input("Cholesterol", 100, 400, 180)

# --- PROCESSING ---
if st.button("Analyze Health Profile"):
    col1, col2 = st.columns(2)
    
    # Example Feature Vector
    input_data = pd.DataFrame([[age, bmi, glucose, bp, chol]], 
                              columns=['Age', 'BMI', 'Glucose', 'BP', 'Cholesterol'])

    with col1:
        st.subheader("📊 Risk Assessment")
        
        # Diabetes Check
        d_risk = mock_predict(input_data, "diabetes")
        st.write(f"**Diabetes Risk:** {d_risk*100:.1f}%")
        st.progress(d_risk)

        # Heart Disease Check
        h_risk = mock_predict(input_data, "heart")
        st.write(f"**Heart Disease Risk:** {h_risk*100:.1f}%")
        st.progress(h_risk)

    with col2:
        st.subheader("🔍 Why this score? (SHAP)")
        # SHAP visualization (Mock)
        fig, ax = plt.subplots()
        features = ['Glucose', 'Age', 'BMI']
        importances = [0.4, 0.2, 0.1]
        ax.barh(features, importances, color='teal')
        st.pyplot(fig)

    # --- PDF GENERATION ---
    st.divider()
    if st.button("Download Health Report (PDF)"):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", 'B', 16)
        pdf.cell(200, 10, "Personalized Health Report", ln=True, align='C')
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, f"Date: {datetime.now().strftime('%Y-%m-%d')}", ln=True)
        pdf.cell(200, 10, f"Diabetes Risk: {d_risk*100:.1f}%", ln=True)
        pdf.cell(200, 10, f"Heart Risk: {h_risk*100:.1f}%", ln=True)
        pdf.multi_cell(0, 10, "Recommendation: Consult a physician for further testing and maintain a balanced diet.")
        
        pdf_output = "health_report.pdf"
        pdf.output(pdf_output)
        with open(pdf_output, "rb") as f:
            st.download_button("Click to Download PDF", f, file_name="Health_Summary.pdf")

# --- DOCTOR BOOKING ---
st.divider()
st.subheader("📅 Direct Specialist Consult")
st.info("Based on your profile, we recommend speaking with a Cardiologist.")
st.link_button("Book Appointment via ZocDoc", "https://www.zocdoc.com")
