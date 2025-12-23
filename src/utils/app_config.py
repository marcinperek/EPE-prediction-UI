import streamlit as st

def load_config(page_title):
    st.set_page_config(
        page_title=page_title, 
        page_icon="random",
        layout="wide",
        initial_sidebar_state="expanded"
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

        .stFormSubmitButton button p {
            font-size: 25px !important;
            font-weight: bold;
        }

        .stButton p {
            font-size: 20px !important;
            padding: 5px;
            font-weight: bold;
        }


        label p {
            font-size: 25px !important;
        }

        #result {
            border-radius: 15px;
            padding: 10px;
        }
        
        .main-svg {
            border-radius: 20px !important;
        }

        .stNumberInput span {
            display: none !important;
            }
        </style>""",
        unsafe_allow_html=True,
    )