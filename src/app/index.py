import streamlit as st
from utils.app_utils import load_config
from utils.app_translations import get_index_translations

st.session_state.setdefault('language', 'English')

labels = get_index_translations(st.session_state['language'])
load_config(labels['short_title'])

st.sidebar.selectbox(labels['language_select'], options=['English', 'Polski'], index=0, key='language')

st.title(labels['title'])
st.write(labels['instructions'])
st.write(labels['description'])
