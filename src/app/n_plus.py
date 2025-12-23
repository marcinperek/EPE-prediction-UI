import streamlit as st
from utils.model import load_model, load_preprocessor
from scripts.inference import get_prediction
from utils.app_utils import load_config, clear_on_page_change
from utils.app_translations import get_n_plus_translations
from scripts.explainer import get_explanation

clear_on_page_change(st, "N+")

st.session_state.setdefault('language', 'English')

labels = get_n_plus_translations(st.session_state['language'])

load_config(labels['title'])

st.sidebar.selectbox(labels['language_select'], options=['English', 'Polski'], index=0, key='language')


with st.spinner(labels['loading_model']):
    model = load_model("models/xgb_n_plus_model.json")
    preprocessor = load_preprocessor("models/preprocessor_n_plus.pkl")

st.markdown(f"<h1 style='font-size:50px; margin-bottom:0.5rem;'>{labels['title']}</h1>", unsafe_allow_html=True)
st.warning(labels['warning'], icon='⚠️')

col1, col2 = st.columns(2, gap='large')

with col1:
    with st.form('input_form'):
        form_col1, form_col2 = st.columns(2, gap='large')
        with form_col1:
            st.write(f'## {labels['general_section']}')
            st.number_input(labels['age'], key='wiek', min_value=0, max_value=100, value=None, step=1)
            st.number_input(labels['psa'], key='PSA', min_value=0.0, max_value=None, value=None, step=0.01)
            st.write(f'## {labels['mri_section']}')
            st.number_input(labels['mri_volume'], key='MRI vol', min_value=0.0, max_value=None, value=None, step=0.1)
            st.number_input(labels['mri_lesion'], key='MRI SIZE', min_value=0.0, max_value=None, value=None, step=0.1)
        with form_col2:
            st.selectbox(labels['mri_pirads'], options=[1,2,3,4,5], key='MRI Pirads')
            st.selectbox(labels['mri_epe'], key='MRI EPE', options=[labels['no'],labels['yes']])
            st.selectbox(labels['mri_svi'], key='MRI SVI', options=[labels['no'],labels['yes']])
            st.write(f'## {labels['biopsy_section']}')
            st.selectbox(labels['bx_isup_grade'], key='Bx ISUP Grade', options=[0,1,2,3,4,5])

        st.divider()

        submitted = st.form_submit_button(labels['predict_button'], width='stretch', key='predict_button')

with col2:
    st.write(f'## {labels['model_prediction']}')
    if submitted:
        if st.session_state['wiek'] is None:
            st.error(labels['age_error'])
        elif st.session_state['PSA'] is None:
            st.error(labels['psa_error'])
        elif st.session_state['MRI vol'] is None:
            st.error(labels['mri_volume_error'])
        elif st.session_state['MRI SIZE'] is None:
            st.error(labels['mri_lesion_error'])
        else:
            with st.spinner(labels['predicting']):
                prediction, prediction_prob, patient = get_prediction(st.session_state, model, preprocessor, target='N+')
                st.session_state['prediction'] = prediction
                st.session_state['prediction_prob'] = prediction_prob
                st.session_state['patient'] = patient
                st.session_state['explanation'] = None

    if 'prediction' in st.session_state and 'prediction_prob' in st.session_state:
        bg_color = 'green'
        if st.session_state['prediction_prob'][0] > 0.8:
            bg_color = 'red'
        elif st.session_state['prediction_prob'][0] > 0.5:
            bg_color = 'orange'
        st.divider()
        col3, col4 = st.columns([1, 1], gap='small')
        with col3:
            st.markdown(f'### {labels['prediction']}', unsafe_allow_html=True)
            st.markdown(f'### {labels['probability']}', unsafe_allow_html=True)
        with col4:
            st.markdown(f"### <span id='result' style='color:white; background:{bg_color}'> {labels['yes'] if st.session_state['prediction'][0] else labels['no']}</span>", unsafe_allow_html=True)
            st.markdown(f"### <span id='result' style='color:white; background:{bg_color}'>{st.session_state['prediction_prob'][0]:.2f}</span>", unsafe_allow_html=True)
        
        st.divider()

        st.write(f'## {labels["explanation_section"]}')
        explain = st.button(labels['explanation_button'], key='explain_button')
        if explain:
            with st.spinner(labels['generating_explanation']):
                st.session_state['explanation'] = get_explanation(st.session_state['patient'], model, preprocessor, target='N+')
        if 'explanation' in st.session_state and st.session_state['explanation'] is not None:
                st.plotly_chart(st.session_state['explanation'], width='stretch')