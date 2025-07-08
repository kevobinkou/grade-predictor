import streamlit as st
from joblib import load
import os
import mysql.connector
from mysql.connector import Error
import pandas as pd
import matplotlib.pyplot as plt

# ----------------- Page Configuration -----------------
st.set_page_config(
    page_title="Student Grade Predictor",
    page_icon="🎓",
    layout="centered"
)

# ----------------- Load Trained Model -----------------
model = load("grade_predictor_model.joblib")

# ----------------- Web App Title -----------------
st.title("🎓 Student Grade Predictor")
st.write("Enter student details to predict the final grade (G3).")

# ----------------- Input Fields -----------------
G1 = st.number_input("G1 (1st Period Grade)", min_value=0.0, max_value=20.0, value=10.0)
G2 = st.number_input("G2 (2nd Period Grade)", min_value=0.0, max_value=20.0, value=10.0)
studytime = st.slider("Study Time (1 = <2h, 4 = >10h)", 1, 4, 2)
failures = st.number_input("Number of Past Failures", min_value=0, max_value=4, value=0)
absences = st.number_input("Number of Absences", min_value=0, max_value=100, value=5)

# ----------------- Predict Button -----------------
if st.button("Predict Final Grade"):
    student_data = [[G1, G2, studytime, failures, absences]]
    prediction = model.predict(student_data)[0]

    st.success(f"📊 Predicted Final Grade (G3): {prediction:.2f}")

    # Feedback
    if prediction >= 10:
        st.info("✅ Likely to pass")
    else:
        st.warning("⚠️ At risk of failing")

    # Insert into MySQL DB
    try:
        conn = mysql.connector.connect(
            host=st.secrets["mysql"]["host"],
            port=st.secrets["mysql"]["port"],
            database=st.secrets["mysql"]["database"],
            user=st.secrets["mysql"]["user"],
            password=st.secrets["mysql"]["password"]
        )
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS predictions (
                id INT AUTO_INCREMENT PRIMARY KEY,
                G1 FLOAT, G2 FLOAT,
                studytime INT,
                failures INT,
                absences INT,
                predicted_grade FLOAT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        cursor.execute("""
            INSERT INTO predictions (G1, G2, studytime, failures, absences, predicted_grade)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (float(G1), float(G2), int(studytime), int(failures), int(absences), float(prediction)))
        conn.commit()
    except Error as e:
        st.error(f"❌ Database error: {e}")
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

# ----------------- Admin Dashboard -----------------
with st.expander("🔐 Admin Dashboard"):
    admin_password = st.text_input("Enter admin password", type="password")

    if admin_password == "admin123":
        try:
            conn = mysql.connector.connect(
                host=st.secrets["mysql"]["host"],
                port=st.secrets["mysql"]["port"],
                database=st.secrets["mysql"]["database"],
                user=st.secrets["mysql"]["user"],
                password=st.secrets["mysql"]["password"]
            )
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM predictions ORDER BY timestamp DESC")
            rows = cursor.fetchall()

            if rows:
                st.write("### 📊 Stored Predictions")
                df = pd.DataFrame(rows, columns=[
                    "id", "G1", "G2", "studytime", "failures", "absences", "predicted_grade", "timestamp"
                ])
                st.dataframe(df, use_container_width=True)

                # 📉 Bar Chart: Average Predicted Grade by Failures
                st.write("### 📈 Average Grade by Number of Past Failures")
                avg_df = df.groupby("failures")["predicted_grade"].mean().reset_index()

                fig, ax = plt.subplots()
                ax.bar(avg_df["failures"], avg_df["predicted_grade"], color="steelblue")
                ax.set_xlabel("Number of Past Failures")
                ax.set_ylabel("Average Predicted Grade")
                ax.set_title("How Past Failures Affect Predicted Grade")
                ax.set_xticks(avg_df["failures"])

                st.pyplot(fig)

                # 📍 Bar Chart: Average Grade by Study Time
                st.write("### 📍 Average Grade by Study Time")
                study_df = df.groupby("studytime")["predicted_grade"].mean().reset_index()

                fig2, ax2 = plt.subplots()
                ax2.bar(study_df["studytime"], study_df["predicted_grade"], color="salmon")
                ax2.set_xlabel("Study Time (1 = <2h ... 4 = >10h)")
                ax2.set_ylabel("Average Predicted Grade")
                ax2.set_title("Predicted Grade by Study Time")
                ax2.set_xticks(study_df["studytime"])

                st.pyplot(fig2)

            else:
                st.info("No predictions stored yet.")

        except mysql.connector.Error as e:
            st.error(f"❌ Database error: {e}")
        finally:
            if conn.is_connected():
                cursor.close()
                conn.close()
    elif admin_password != "":
        st.error("Incorrect password")

# ----------------- Developer Info and Image -----------------
image_path = "student_grade_predictor.jpg"
if os.path.exists(image_path):
    st.image(image_path, width=150, caption="Kelvin Maina — Student | Data Enthusiast")

with st.sidebar:
    if os.path.exists(image_path):
        st.image(image_path, width=150)

    st.markdown("""
    ### 👨‍💻 Developer Info
    **Developer:** Kelvin Maina  
    **University:** Dedan Kimathi University of Technology  
    **Project:** *Machine Learning – Student Grade Predictor*
    """)
