# ==========================================================
# SICKLE CELL VOC RISK ASSESSMENT TOOL
# Machine Learning-Based Clinical Decision Support System
# for Sickle Cell Disease Management in Ondo State
# ==========================================================
import pandas as pd
import joblib
import streamlit as st
import shap
from pdf_report import generate_pdf
from datetime import datetime
from io import BytesIO
model = joblib.load("xgboost_model.pkl")
preprocessor = joblib.load("preprocessor.pkl")
label_encoder = joblib.load("label_encoder.pkl")
explainer = shap.TreeExplainer(model)
# ----------------------------------------------------------
# SESSION STATE INITIALIZATION
# ----------------------------------------------------------

if "history" not in st.session_state:
    st.session_state.history = []
# ----------------------------------------------------------
# EXCEL EXPORT FUNCTION
# ----------------------------------------------------------

def generate_excel(history):

    df = pd.DataFrame(history)

    output = BytesIO()

    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        df.to_excel(
            writer,
            index=False,
            sheet_name="Prediction History"
        )

    output.seek(0)

    return output
# ----------------------------------------------------------
# PAGE CONFIGURATION
# ----------------------------------------------------------

st.set_page_config(
    page_title="Sickle Cell VOC Risk Assessment Tool",
    page_icon="🩸",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ----------------------------------------------------------
# CUSTOM CSS
# ----------------------------------------------------------
st.markdown("""
<style>

/* ===========================
   MAIN PAGE
=========================== */

.stApp{
    background:#F5F9FC;
}

/* Reduce empty spaces */
.block-container{
    padding-top:1.5rem;
    padding-bottom:1rem;
    padding-left:2rem;
    padding-right:2rem;
}

/* ===========================
   HEADINGS
=========================== */

h1{
    color:#174EA6;
    font-size:50px;
    font-weight:800;
}

h2{
    color:#174EA6;
    font-weight:700;
}

h3{
    color:#1F2937;
    font-weight:600;
}

/* ===========================
   INPUTS
=========================== */

.stNumberInput,
.stSelectbox{

    margin-bottom:10px;
}

/* ===========================
   BUTTONS
=========================== */

.stButton>button{

    width:100%;

    height:52px;

    border-radius:12px;

    border:none;

    background:#0B5ED7;

    color:white;

    font-size:17px;

    font-weight:bold;

    transition:0.25s;
}

.stButton>button:hover{

    background:#084298;

    transform:translateY(-2px);
}

/* ===========================
   ALERT BOXES
=========================== */

.stSuccess,
.stInfo,
.stWarning,
.stError{

    border-radius:12px;
}

/* ===========================
   DIVIDER
=========================== */

hr{

    margin-top:25px;
    margin-bottom:25px;
}

/* ===========================
   SIDEBAR
=========================== */

section[data-testid="stSidebar"]{

    background:#F5F9FC;
}

</style>
""", unsafe_allow_html=True)


# ----------------------------------------------------------
# HEADER
# ----------------------------------------------------------

st.markdown("""
<div style="
    background: linear-gradient(90deg, #0B5ED7, #4A90E2);
    padding: 30px;
    border-radius: 15px;
    text-align: center;
    color: white;
    box-shadow: 0px 4px 15px rgba(0,0,0,0.15);
    margin-bottom: 25px;
">

<h1 style="
    color:white;
    margin-bottom:10px;
    font-size:42px;
">
🩸 Sickle Cell VOC Risk Assessment Tool
</h1>

<h3 style="
    color:white;
    margin-bottom:5px;
    font-weight:500;
">
Machine Learning-Based Risk Assessment Tool
</h3>

<p style="
    font-size:22px;
    margin-top:10px;
">
for Sickle Cell Disease Management in Ondo State
</p>

</div>
""", unsafe_allow_html=True)
# ----------------------------------------------------------
# TWO COLUMNS
# ----------------------------------------------------------

left,right=st.columns([1.8,1.2])

# ==========================================================
# LEFT COLUMN
# ==========================================================

with left:

    with st.container(border=True):

        st.markdown("## 👤 Patient Information")

        col1, col2 = st.columns(2)
    with col1:

        age=st.number_input(
            "Age (Years)",
            min_value=1,
            max_value=100,
            value=20
        )

        sex=st.selectbox(
            "Sex",
            [
                "Male",
                "Female"
            ]
        )

    with col2:

        weight=st.number_input(
            "Weight (kg)",
            min_value=10.0,
            max_value=200.0,
            value=60.0
        )

        genotype=st.selectbox(
            "Genotype",
            [
                "HbSS",
                "HbSC"
            ]
        )


    st.divider()
    
with st.container(border=True):
    st.markdown("## 🧪 Laboratory Results")
    
    lab1,lab2=st.columns(2)

    with lab1:

        pcv=st.number_input(
            "PCV (%)",
            min_value=0.0,
            max_value=100.0,
            value=25.0
        )

        wbc=st.number_input(
            "WBC (/µL)",
            min_value=0,
            max_value=100000,
            value=8000
        )

    with lab2:

        hb=st.number_input(
            "Hb (g/dL)",
            min_value=0.0,
            max_value=20.0,
            value=8.0
        )

        platelets=st.number_input(
            "Platelets (/µL)",
            min_value=0,
            max_value=1000000,
            value=250000
        )
    st.divider()

    # =========================================================
    # CLINICAL ASSESSMENT
    # ==========================================================

    st.markdown("## 🩺 Clinical Assessment")

    clinical1, clinical2 = st.columns(2)

    with clinical1:

        admission_history = st.selectbox(
    "Hospital Admission History",
    [
        "No",
        "Yes"
    ]
)
        voc_history = st.selectbox(
            "Previous VOC History",
            [
                "No",
                "Yes"
            ]
        )

    with clinical2:

        blood_transfusion = st.selectbox(
            "Blood Transfusion",
            [
                "No",
                "Yes"
            ]
        )

        hydroxyurea = st.selectbox(
            "Hydroxyurea Therapy",
            [
                "No",
                "Yes"
            ]
        )

    st.divider()

    # ==========================================================
    # BUTTONS
    # ==========================================================

    button1, button2 = st.columns(2)

    with button1:

        predict_button = st.button(
            "🩸 Predict VOC Risk",
            use_container_width=True
        )

    with button2:

        clear_button = st.button(
            "🔄 Clear Form",
            use_container_width=True
        )
if clear_button:

    st.session_state.clear()

    st.rerun()
# ==========================================================
# RIGHT PANEL
# ==========================================================

with right:

    st.markdown("## 📊 Prediction Result")

    if "prediction" not in st.session_state:

        st.info("Awaiting Prediction...")

    else:

        risk = st.session_state.prediction
        confidence = st.session_state.confidence

        # ---------------------------------------------
        # RISK CARD
        # ---------------------------------------------

        if risk.lower() == "low":

            st.markdown(f"""
<div style="
background:#D1FAE5;
padding:30px;
border-radius:12px;
text-align:center;
">

<h2 style="color:#065F46;">
🟢 LOW RISK
</h2>

<h3>
Confidence: {confidence:.2f}%
</h3>

</div>
""", unsafe_allow_html=True)

        elif risk.lower() == "medium":

            st.markdown(f"""
<div style="
background:#FEF3C7;
padding:30px;
border-radius:12px;
text-align:center;
">

<h2 style="color:#92400E;">
🟡 MEDIUM RISK
</h2>

<h3>
Confidence: {confidence:.2f}%
</h3>

</div>
""", unsafe_allow_html=True)

        else:

            st.markdown(f"""
<div style="
background:#FECACA;
padding:30px;
border-radius:12px;
text-align:center;
">

<h2 style="color:#991B1B;">
🔴 HIGH RISK
</h2>

<h3>
Confidence: {confidence:.2f}%
</h3>

</div>
""", unsafe_allow_html=True)

        st.divider()

        # ---------------------------------------------
        # PATIENT SUMMARY
        # ---------------------------------------------

        st.markdown("### 👤 Patient Summary")

        st.markdown(f"""
**Age:** {age} Years

**Weight:** {weight:.1f} kg

**Sex:** {sex}

**Genotype:** {genotype}

**PCV:** {pcv:.1f} %

**Hb:** {hb:.1f} g/dL

**WBC:** {wbc:,} /µL

**Platelets:** {platelets:,} /µL
""")

        st.divider()
                    # ---------------------------------------------
        # SHAP EXPLANATION
        # ---------------------------------------------

        st.markdown("### 🔍 Why this prediction?")

        if "shap_explanation" in st.session_state:

            st.markdown(
                "**Main factors influencing the model's prediction:**"
            )

            # Convert model feature names to clinical names
            feature_names_readable = {
                "num__Age": "Age",
                "num__Weight": "Weight",
                "num__PCV": "PCV",
                "num__Hb": "Haemoglobin (Hb)",
                "num__WBC": "White Blood Cell Count (WBC)",
                "num__Platelets": "Platelet Count",
                "cat__Sex_F": "Sex: Female",
                "cat__Sex_M": "Sex: Male",
                "cat__Genotype_HbSC": "Genotype: HbSC",
                "cat__Genotype_HbSS": "Genotype: HbSS",
                "cat__Admission_History_No": "No Admission History",
                "cat__Admission_History_Yes": "Previous Admission History",
                "cat__Blood_Transfusion_No": "No Blood Transfusion",
                "cat__Blood_Transfusion_Yes": "Previous Blood Transfusion",
                "cat__VOC_History_No": "No Previous VOC History",
                "cat__VOC_History_Yes": "Previous VOC History",
                "cat__Hydroxyurea_No": "No Hydroxyurea Use",
                "cat__Hydroxyurea_Yes": "Hydroxyurea Use"
            }

            for _, row in st.session_state.shap_explanation.iterrows():

                feature = row["Feature"]
                shap_value = row["SHAP_Value"]

                readable_name = feature_names_readable.get(
                    feature,
                    feature
                )

                if shap_value > 0:
                    direction = f"toward **{risk} Risk**"
                else:
                    direction = f"away from **{risk} Risk**"

                st.write(
                    f"• **{readable_name}** — contribution {direction}"
                )

        st.divider()

        # ---------------------------------------------
        # CLINICAL RECOMMENDATION
        # ---------------------------------------------

        st.markdown("### 💊 Clinical Recommendation")

        if risk.lower() == "low":

            recommendation = """
✅ Continue routine clinic visits<br>
💧 Maintain adequate hydration<br>
💊 Continue prescribed medication
"""

            color = "#D1FAE5"
            border = "#16A34A"

        elif risk.lower() == "medium":

            recommendation = """
🩺 Monitor patient closely<br>
💊 Review medication compliance<br>
📅 Schedule earlier follow-up
"""

            color = "#FEF3C7"
            border = "#D97706"

        else:

            recommendation = """
🚨 Immediate clinical review<br>
🏥 Consider hospital admission<br>
🩸 Continue intensive management
"""

            color = "#FECACA"
            border = "#DC2626"

        st.markdown(f"""
<div style="
background:{color};
padding:18px;
border-radius:12px;
border-left:6px solid {border};
">

<h4 style="margin-top:0;">
Clinical Recommendation
</h4>

{recommendation}

</div>
""", unsafe_allow_html=True)

        st.divider()

        # ---------------------------------------------
        # MODEL INFORMATION
        # ---------------------------------------------

        st.markdown("""
<div style="
background:#E8F4FD;
padding:15px;
border-radius:10px;
border-left:6px solid #0B5ED7;
">

<h4 style="margin:0;color:#0B5ED7;">
🤖 Model Information
</h4>

<b>Algorithm:</b> XGBoost Classifier<br>

<b>Status:</b> 🟢 Ready<br>

<b>Version:</b> 1.0

</div>
""", unsafe_allow_html=True)
if "patient_info" in st.session_state:

    pdf = generate_pdf(
        st.session_state.patient_info,
        risk,
        confidence
    )

    st.download_button(
        label="📄 Download PDF Report",
        data=pdf,
        file_name="VOC_Risk_Assessment_Report.pdf",
        mime="application/pdf",
        use_container_width=True
    )

# ==========================================================
# END OF RIGHT PANEL
# ==========================================================

# ============================================
    # ==========================================================
# PREDICTION LOGIC
# ==========================================================

if predict_button:

    # ===============================
    # INPUT VALIDATION
    # ===============================

    if hb <= 0:
        st.error("❌ Haemoglobin (Hb) must be greater than 0 g/dL.")
        st.stop()

    if pcv <= 0:
        st.error("❌ PCV must be greater than 0%.")
        st.stop()

    if wbc <= 0:
        st.error("❌ White Blood Cell Count must be greater than 0.")
        st.stop()

    if platelets <= 0:
        st.error("❌ Platelet count must be greater than 0.")
        st.stop()

    if weight <= 0:
        st.error("❌ Weight must be greater than 0 kg.")
        st.stop()

        
    # Create DataFrame from user input
    patient_data = pd.DataFrame({
        "Age": [age],
        "Weight": [weight],
        "PCV": [pcv],
        "Hb": [hb],
        "WBC": [wbc],
        "Platelets": [platelets],
        "Sex": [sex],
        "Genotype": [genotype],
        "Admission_History": [admission_history],
        "Blood_Transfusion": [blood_transfusion],
        "VOC_History": [voc_history],
        "Hydroxyurea": [hydroxyurea]
    })

    # Preprocess patient data
    processed_data = preprocessor.transform(patient_data)

    # Make prediction
    prediction = model.predict(processed_data)

    # Decode prediction
    predicted_risk = label_encoder.inverse_transform(prediction)[0]

    # Prediction confidence
    probability = model.predict_proba(processed_data)
    confidence = probability.max() * 100
    # ==========================================================
    # SHAP EXPLANATION
    # ==========================================================

    shap_values = explainer.shap_values(processed_data)

    predicted_class = prediction[0]

    # Get SHAP values for the predicted class
    patient_shap_values = shap_values[0, :, predicted_class]

    # Get feature names from the preprocessor
    feature_names = preprocessor.get_feature_names_out()

    # Create explanation table
    explanation_data = pd.DataFrame({
        "Feature": feature_names,
        "SHAP_Value": patient_shap_values
    })

    # Calculate importance
    explanation_data["Absolute_SHAP"] = explanation_data["SHAP_Value"].abs()

    # Sort by importance
    explanation_data = explanation_data.sort_values(
        by="Absolute_SHAP",
        ascending=False
    )

    # Take the top 5 factors
    top_features = explanation_data.head(5)
    st.session_state.shap_explanation = top_features
    patient_info = {
    "Age": age,
    "Sex": sex,
    "Weight": weight,
    "Genotype": genotype,
    "PCV": pcv,
    "Hb": hb,
    "WBC": wbc,
    "Platelets": platelets,
    "Admission History": admission_history,
    "Blood Transfusion": blood_transfusion,
    "VOC History": voc_history,
    "Hydroxyurea": hydroxyurea
}
    # ==========================================
    # SAVE PREDICTION HISTORY
    # ==========================================

    history_record = {
    "Date": datetime.now().strftime("%d-%m-%Y %H:%M"),
    "Age": age,
    "Sex": sex,
    "Weight (kg)": weight,
    "Genotype": genotype,
    "PCV (%)": pcv,
    "Hb (g/dL)": hb,
    "WBC (/µL)": wbc,
    "Platelets (/µL)": platelets,
    "Admission History": admission_history,
    "Blood Transfusion": blood_transfusion,
    "VOC History": voc_history,
    "Hydroxyurea": hydroxyurea,
    "Prediction": predicted_risk,
    "Confidence (%)": round(confidence, 2)
}

    st.session_state.history.append(history_record)

    # Display prediction
    st.session_state.prediction = predicted_risk
    st.session_state.patient_info = patient_info
    st.session_state.confidence = confidence

    st.rerun()
    # ==========================================================
# PREDICTION HISTORY
# ==========================================================

st.divider()

st.subheader("📜 Prediction History")

if len(st.session_state.history) == 0:

    st.info("No predictions have been made yet.")

else:

    history_df = pd.DataFrame(st.session_state.history)

    st.dataframe(
        history_df,
        use_container_width=True,
        hide_index=True
    )

    excel_file = generate_excel(st.session_state.history)

    st.download_button(
        label="📥 Download Prediction History (.xlsx)",
        data=excel_file,
        file_name="Prediction_History.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        use_container_width=True
    )
# ==========================================================
# PROFESSIONAL FOOTER
# ==========================================================

st.markdown("""
<div style="
margin-top:40px;
padding:20px;
background:#F8FBFF;
border:1px solid #D6E4F0;
border-radius:12px;
">

<div style="
display:flex;
justify-content:space-between;
align-items:flex-start;
gap:20px;
flex-wrap:wrap;
">

<div style="flex:1; min-width:250px;">

<h4 style="color:#0B5ED7; margin-bottom:10px;">
ℹ Clinical Decision Support
</h4>

<p style="font-size:15px; color:#555;">
This clinical decision support tool is intended to assist healthcare
professionals in assessing the risk of vaso-occlusive crisis (VOC)
among sickle cell patients.
</p>

<p style="font-size:15px; color:#555;">
It should support—not replace—clinical judgement.
</p>

</div>

<div style="flex:1; min-width:220px;">

<h4 style="color:#0B5ED7; margin-bottom:10px;">
🛡 Clinical Use
</h4>

<p style="font-size:15px; color:#555;">
Use this application together with patient history,
physical examination and laboratory findings before
making any clinical decision.
</p>

</div>

<div style="flex:1; min-width:220px;">

<h4 style="color:#0B5ED7; margin-bottom:10px;">
Version 1.0
</h4>

<p style="font-size:15px; color:#555;">
<b>Developer:</b><br>
Kolawole Toheeb Adeola
</p>

<p style="font-size:15px; color:#555;">
Machine Learning-Based Clinical Decision Support Tool
</p>

</div>

</div>

<hr>

<div style="
text-align:center;
font-size:14px;
color:#777;
">

Department of Information and Communication Engineering |
Federal University of Technology, Akure |

Dataset: FUTA Teaching Hospital, Akure

</div>

</div>
""", unsafe_allow_html=True)