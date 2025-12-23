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

def clear_on_page_change(st, page_name):
    if st.session_state.get("current_page") != page_name:
        st.session_state["current_page"] = page_name
        keys_to_clear = ["prediction", "prediction_prob", "patient", "explanation"]
        for key in keys_to_clear:
            if key in st.session_state:
                st.session_state.pop(key)