import streamlit as st
from utils.model import load_model, load_preprocessor
import time

st.set_page_config(page_title="EPE Prediction", layout="wide")

st.markdown(
    """<style>
    .stFormSubmitButton button {
        background-color:#2ecc71 !important;
        color:#ffffff !important;
        border:none !important;
    }
    .stFormSubmitButton button:hover {
        background-color:#27ae60 !important;
        color:#ffffff !important;
        border:none !important;
    }

    label p {
        font-size: 25px !important;
    }

    </style>""",
    unsafe_allow_html=True,
)
with st.spinner('Loading model...'):
    model = load_model("models/xgb_epe_rp_model.json")
    preprocessor = load_preprocessor("models/preprocessor_epe_rp.pkl")

numerical_cols = ['wiek', 'PSA', 'PSAdensity', 'MRI vol', 'MRI SIZE']
categorical_cols = ['MRI Pirads', 'MRI EPE', 'MRI EPE L', 'MRI EPE P', 'MRI SVI', 'MRI SVI L', 'MRI SVI P','Bx ISUP Grade P', 'Bx ISUP Grade L', 'Bx ISUP Grade']


def labeled_number_input(label, key, min_value=None, max_value=None, value=None, step=None):
    col_label, col_input = st.columns([1, 2])
    with col_label:
        st.markdown(f"<p style='font-size:28px; margin:0;'>{label}:</p>", unsafe_allow_html=True)
    with col_input:
        return st.number_input(" ", label_visibility="collapsed", key=key, min_value=min_value, max_value=max_value, value=value, step=step)

def labeled_text_input(label, key):
    col_label, col_input = st.columns([1, 2])
    with col_label:
        st.markdown(f"<p style='font-size:28px; margin:0;'>{label}:</p>", unsafe_allow_html=True)
    with col_input:
        return st.text_input(" ", key=key, label_visibility="collapsed")
    
def labeled_selectbox(label, options, key):
    col_label, col_input = st.columns([1, 2])
    with col_label:
        st.markdown(f"<p style='font-size:28px; margin:0;'>{label}</p>", unsafe_allow_html=True)
    with col_input:
        return st.selectbox(" ", options=options, key=key, label_visibility="collapsed")

st.title("EPE Prediction")
st.warning('This model is not suitable for medical use. For research purposes only.', icon="⚠️")

col1, col2 = st.sidebar.columns(2)

button1 = col1.button('Button 1')
button2 = col2.button('Button 2')

col1, col2 = st.columns([1, 3])

with col1:
    with st.form("input_form"):
        labeled_number_input("Wiek", "wiek", min_value=0, max_value=100, value=None, step=1)
        labeled_number_input("PSA", "PSA", min_value=0.0, max_value=1000.0, value=None, step=0.01)
        labeled_number_input("PSA Density", "PSAdensity", min_value=0.0, max_value=1000.0, value=None, step=0.001)
        st.divider()
        st.write("## MRI Features")
        labeled_text_input("Volume", "MRI vol")
        labeled_text_input("Lesion size", "MRI SIZE")
        labeled_selectbox("Pirads", options=[1,2,3,4,5], key="MRI Pirads")
        labeled_selectbox("EPE", options=["No","Yes"], key="MRI EPE")
        labeled_selectbox("EPE L", options=["No","Yes"], key="MRI EPE L")
        labeled_selectbox("EPE P", options=["No","Yes"], key="MRI EPE P")
        labeled_selectbox("SVI", options=["No","Yes"], key="MRI SVI")
        labeled_selectbox("SVI L", options=["No","Yes"], key="MRI SVI L")
        labeled_selectbox("SVI P", options=["No","Yes"], key="MRI SVI P")
        st.divider()
        st.write("### Biopsy Features")
        labeled_selectbox("Bx ISUP Grade P", options=[0,1,2,3,4,5], key="Bx ISUP Grade P")
        labeled_selectbox("Bx ISUP Grade L", options=[0,1,2,3,4,5], key="Bx ISUP Grade L")
        labeled_selectbox("Bx ISUP Grade", options=[0,1,2,3,4,5], key="Bx ISUP Grade")

        st.divider()

        submitted = st.form_submit_button("Predict", width='stretch', key="predict_button")


with col2:
    st.write("## Prediction Result")   
    if submitted:
        with st.spinner('Predicting...'):
            input_data = {col: [st.session_state[col]] for col in numerical_cols + categorical_cols}
            import pandas as pd
            input_df = pd.DataFrame(input_data)
            input_processed = preprocessor.transform(input_df)
            prediction, prediction_prob = model.predict(input_processed), model.predict_proba(input_processed)[:, 1]
            with col2:
                st.write(f"Predicted EPE: {prediction[0]}, Probability: {prediction_prob[0]:.2f}")
