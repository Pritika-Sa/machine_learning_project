import streamlit as st
import pandas as pd
import joblib

# ------------------- CONFIG -------------------
st.set_page_config(page_title="Dyslexia Predictor", page_icon="🧠", layout="wide")

# Load trained model
model = joblib.load("model.pkl")

# ------------------- FEATURE COLUMNS -------------------
expected_columns = ['Gender', 'Nativelang', 'Otherlang', 'Age']
for i in range(30):
    if (0 <= i < 12) or (13 <= i < 17) or i in [21, 22, 29]:
        expected_columns += [
            f'Clicks{i+1}', f'Hits{i+1}', f'Misses{i+1}',
            f'Score{i+1}', f'Accuracy{i+1}', f'Missrate{i+1}'
        ]

# ------------------- SIDEBAR -------------------
with st.sidebar:
    st.title("📘 About This Project")
    st.markdown("""
    ## 🧠 Dyslexia Prediction

    This app predicts the likelihood of **dyslexia** based on user interactions.

    ### 📂 Dataset
    - Device: Desktop & Tablet
    - Features: Clicks, Hits, Misses, Accuracy, Score, etc.

    ### 🤖 ML Models Used
    - ✅ Random Forest Classifier
    - 🔍 Others: SVM, Logistic Regression

    ### 🛠️ Built With
    - Python, Scikit-learn, Streamlit

    ---
    ⚠️ *Not a medical diagnostic tool.*
    """)

# ------------------- HEADER -------------------
st.markdown("<h1 style='text-align: center; color: #367589;'>DYSLEXIA PREDICTION SYSTEM</h1>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align: center;'>An Intelligent Assistant For Early Detection</h4>", unsafe_allow_html=True)
st.write("---")

# ------------------- USER INPUT -------------------
st.markdown(
    "<h3 style='color:#367589; padding-bottom:6px;'> User Information</h3>",
    unsafe_allow_html=True
)

with st.container():
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**Gender Selection:**")
        gender = st.radio("Gender", ["Male", "Female"], horizontal=True)

    with col2:
        st.markdown("**Language Preference:**")
        lang1, lang2 = st.columns(2)
        with lang1:
            nativelang = st.radio("Native Language", ["Yes", "No"], horizontal=True)
        with lang2:
            otherlang = st.radio("Other Language", ["Yes", "No"], horizontal=True)

# Age (Placed below)
st.markdown("**Age Selection:**")
age_col, _ = st.columns([1, 3])  # control width
with age_col:
    age = st.selectbox("Select Age", options=list(range(5, 101)), index=20)


st.markdown(
    "<h3 style='color:#367589; padding-bottom:6px;'>Task 1 Performance Metrics</h3>",
    unsafe_allow_html=True
)

with st.expander("Metrices:", expanded=True):
    col1, col2, col3 = st.columns(3)

    with col1:
        clicks1 = st.number_input("Clicks1", min_value=0, max_value=50, value=5, help="Total user clicks in Task 1")
        hits1 = st.number_input("Hits1", min_value=0, max_value=50, value=3, help="Correct selections")
    
    with col2:
        misses1 = st.number_input("Misses1", min_value=0, max_value=50, value=1, help="Wrong or missed attempts")
        score1 = st.number_input("Score1", min_value=0, max_value=100, value=5, help="Task 1 score")

    with col3:
        accuracy1 = st.selectbox("Accuracy1", [round(x * 0.1, 2) for x in range(11)], index=10, help="Hit accuracy %")
        missrate1 = st.selectbox("Missrate1", [round(x * 0.1, 2) for x in range(11)], index=0, help="Miss rate %")

# ------------------- PREDICTION -------------------
st.write("---")
if st.button("🔍 Predict Dyslexia"):
    input_data = {
        "Gender": 1 if gender == "Male" else 2,
        "Nativelang": 1 if nativelang == "Yes" else 0,
        "Otherlang": 1 if otherlang == "Yes" else 0,
        "Age": age,
        "Clicks1": clicks1,
        "Hits1": hits1,
        "Misses1": misses1,
        "Score1": score1,
        "Accuracy1": accuracy1,
        "Missrate1": missrate1
    }

    # Fill remaining missing columns with 0
    full_input = pd.DataFrame([input_data])
    full_input = full_input.reindex(columns=expected_columns, fill_value=0)

    # Predict
    prediction = model.predict(full_input)[0]

    st.write("---")
    if prediction == 1:
        st.error("🟥 **Prediction: Dyslexic**\n\nFurther educational screening is advised.")
    else:
        st.success("🟩 **Prediction: Non-Dyslexic**\n\nNo patterns of dyslexia detected.")

# ------------------- FOOTER -------------------
st.markdown("---")
