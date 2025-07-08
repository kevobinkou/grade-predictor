import streamlit as st
from joblib import load
import os

# Load the trained model
model = load("grade_predictor_model.joblib")

# Web app title
st.title("🎓 Student Grade Predictor")
st.write("Enter student details to predict the final grade (G3).")

# Main input fields
G1 = st.number_input("G1 (1st Period Grade)", min_value=0.0, max_value=20.0, value=10.0)
G2 = st.number_input("G2 (2nd Period Grade)", min_value=0.0, max_value=20.0, value=10.0)
studytime = st.slider("Study Time (1 = <2h, 4 = >10h)", 1, 4, 2)
failures = st.number_input("Number of Past Failures", min_value=0, max_value=4, value=0)
absences = st.number_input("Number of Absences", min_value=0, max_value=100, value=5)

# Predict button
if st.button("Predict Final Grade"):
    student_data = [[G1, G2, studytime, failures, absences]]
    prediction = model.predict(student_data)[0]
    
    st.success(f"📊 Predicted Final Grade (G3): {prediction:.2f}")
    
    # Feedback message
    if prediction >= 10:
        st.info("✅ Likely to pass")
    else:
        st.warning("⚠️ At risk of failing")

# Load image (main section)
image_path = r"C:\Users\ADMIN\OneDrive\Desktop\Coding_projects\Grade predictor\student_grade_predictor.jpg"
if os.path.exists(image_path):
    st.image(image_path, width=150, caption="Kelvin Maina — Student | Data Enthusiast")

# Sidebar info
with st.sidebar:
    if os.path.exists(image_path):
        st.image(image_path, width=150)
    
    st.markdown("""
    ### 👨‍💻 Developer Info
    **Developer:** Kelvin Maina  
    **University:** Dedan Kimathi University of Technology  
    **Project:** *Machine Learning – Student Grade Predictor*
    """)