import streamlit as st

def load_config():
    st.set_page_config(
        page_title="EPE Prediction", 
        page_icon="random",
        layout="wide",
        initial_sidebar_state="auto"
    )

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

        #result {
            border-radius: 15px;
            padding: 10px;
        }
        </style>""",
        unsafe_allow_html=True,
    )