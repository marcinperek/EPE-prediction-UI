import streamlit as st
from utils.model import load_model, load_preprocessor
from scripts.inference import get_prediction
from utils.app_config import load_config

# load_config()

with st.spinner('Loading model...'):
    model = load_model("models/xgb_epe_rp_model.json")
    preprocessor = load_preprocessor("models/preprocessor_epe_rp.pkl")

st.markdown("<h1 style='font-size:50px; margin-bottom:0.5rem;'>EPE Prediction</h1>", unsafe_allow_html=True)
st.warning('This model is not suitable for medical use. For research purposes only.', icon="⚠️")

with st.sidebar:
    st.write("## Models")
    st.write("EPE")
    st.write("N+")
    st.write("----")

col1, col2 = st.columns([1, 1], gap="large")

with col1:
    with st.form("input_form"):
        form_col1, form_col2 = st.columns([1, 1], gap="large")
        with form_col1:
            st.write("## General")
            st.number_input("Wiek", key="wiek", min_value=0, max_value=100, value=None, step=1)
            st.number_input("PSA", key="PSA", min_value=0.0, max_value=1000.0, value=None, step=0.01)
            st.write("## MRI Features")
            st.number_input("Volume", key="MRI vol", min_value=0.0, max_value=None, value=None, step=0.1)
            st.number_input("Lesion size", key="MRI SIZE", min_value=0.0, max_value=None, value=None, step=0.1)
            st.selectbox("Pirads", options=[1,2,3,4,5], key="MRI Pirads")
            st.selectbox("EPE", key="MRI EPE", options=["No","Yes"])
            st.selectbox("EPE L", key="MRI EPE L", options=["No","Yes"])
        with form_col2:
            st.selectbox("EPE P", key="MRI EPE P", options=["No","Yes"])
            st.selectbox("SVI", key="MRI SVI", options=["No","Yes"])
            st.selectbox("SVI L", key="MRI SVI L", options=["No","Yes"])
            st.selectbox("SVI P", key="MRI SVI P", options=["No","Yes"])
            st.write("## Biopsy Features")
            st.selectbox("Bx ISUP Grade P", key="Bx ISUP Grade P", options=[0,1,2,3,4,5])
            st.selectbox("Bx ISUP Grade L", key="Bx ISUP Grade L", options=[0,1,2,3,4,5])
            st.selectbox("Bx ISUP Grade", key="Bx ISUP Grade", options=[0,1,2,3,4,5])

        st.divider()

        submitted = st.form_submit_button("Predict", width='stretch', key="predict_button")


with col2:
    st.write("## Model Prediction")   
    if submitted:
        with st.spinner('Predicting...'):
            import time
            time.sleep(3)  # Simulate a delay for prediction
            prediction, prediction_prob = get_prediction(st.session_state, model, preprocessor)
        
        bg_color = "#77dd77"
        if prediction_prob[0] > 0.8:
            bg_color = "#f8857f"
        elif prediction_prob[0] > 0.5:
            bg_color = "#ffd580"
        st.divider()
        col3, col4 = st.columns([1, 1], gap="small")
        with col3:
            st.markdown(f"### Predicted EPE present?", unsafe_allow_html=True)
            st.markdown(f"### Probability of EPE present:", unsafe_allow_html=True)
        with col4:
            st.markdown(f"### <span id='result' style='color:white; background:{bg_color}'> {"yes" if prediction[0] else "no"}</span>", unsafe_allow_html=True)
            st.markdown(f"### <span id='result' style='color:white; background:{bg_color}'>{prediction_prob[0]:.2f}</span>", unsafe_allow_html=True)
        
        st.divider()