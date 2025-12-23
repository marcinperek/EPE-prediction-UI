import streamlit as st
from utils.app_utils import load_config

load_config("Main")

pg = st.navigation([
    st.Page("index.py", title="Home"),
    st.Page("epe.py", title="EPE Prediction"),
    st.Page("n_plus.py", title="N+ Prediction")
])

pg.run()