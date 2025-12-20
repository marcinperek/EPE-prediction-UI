import streamlit as st
from utils.model import load_model, load_preprocessor
from scripts.inference import get_prediction
from utils.app_config import load_config

load_config("N+ Prediction")
st.session_state.setdefault("language_select", "English")
label = "Język" if st.session_state["language_select"] == "Polski" else "Language"
st.sidebar.selectbox(label, options=["English", "Polski"], index=0, key="language_select")

if st.session_state.language_select == "English":
    with st.spinner('Loading model...'):
        model = load_model("models/xgb_n_plus_model.json")
        preprocessor = load_preprocessor("models/preprocessor_n_plus.pkl")

    st.markdown("<h1 style='font-size:50px; margin-bottom:0.5rem;'>N+ Prediction</h1>", unsafe_allow_html=True)
    st.warning('This model is not suitable for medical use. For research purposes only.', icon="⚠️")

    col1, col2 = st.columns([1, 1], gap="large")

    with col1:
        with st.form("input_form"):
            form_col1, form_col2 = st.columns([1, 1], gap="large")
            with form_col1:
                st.write("## General")
                st.number_input("Age", key="wiek", min_value=0, max_value=100, value=None, step=1)
                st.number_input("PSA", key="PSA", min_value=0.0, max_value=1000.0, value=None, step=0.01)
                st.write("## MRI Features")
                st.number_input("Volume", key="MRI vol", min_value=0.0, max_value=None, value=None, step=0.1)
                st.number_input("Lesion size", key="MRI SIZE", min_value=0.0, max_value=None, value=None, step=0.1)
            with form_col2:
                st.selectbox("Pirads", options=[1,2,3,4,5], key="MRI Pirads")
                st.selectbox("EPE", key="MRI EPE", options=["No","Yes"])
                st.selectbox("SVI", key="MRI SVI", options=["No","Yes"])
                st.write("## Biopsy Features")
                st.selectbox("ISUP Grade", key="Bx ISUP Grade", options=[0,1,2,3,4,5])

            st.divider()

            submitted = st.form_submit_button("Predict", width='stretch', key="predict_button")


    with col2:
        st.write("## Model Prediction")   
        if submitted:
            if st.session_state["wiek"] is None:
                st.error("Please enter a valid number for Age.")
            elif st.session_state["PSA"] is None:
                st.error("Please enter a valid number for PSA.")
            elif st.session_state["MRI vol"] is None:
                st.error("Please enter a valid number for MRI Volume.")
            elif st.session_state["MRI SIZE"] is None:
                st.error("Please enter a valid number for MRI Lesion size.")
            else:
                with st.spinner('Predicting...'):
                    prediction, prediction_prob, df = get_prediction(st.session_state, model, preprocessor, target="N+")
                
                # bg_color = "#77dd77"
                bg_color = "green"
                if prediction_prob[0] > 0.8:
                    # bg_color = "#f8625a"
                    bg_color = "red"
                elif prediction_prob[0] > 0.5:
                    # bg_color = "#ffd580"
                    # bg_color = "#3e4116"
                    bg_color = "orange"
                st.divider()
                col3, col4 = st.columns([1, 1], gap="small")
                with col3:
                    st.markdown(f"### N+ present?", unsafe_allow_html=True)
                    st.markdown(f"### Probability of N+ present:", unsafe_allow_html=True)
                with col4:
                    st.markdown(f"### <span id='result' style='color:white; background:{bg_color}'> {"yes" if prediction[0] else "no"}</span>", unsafe_allow_html=True)
                    st.markdown(f"### <span id='result' style='color:white; background:{bg_color}'>{prediction_prob[0]:.2f}</span>", unsafe_allow_html=True)
                
                st.divider()

elif st.session_state.language_select == "Polski":
    with st.spinner('Ładowanie modelu...'):
        model = load_model("models/xgb_n_plus_model.json")
        preprocessor = load_preprocessor("models/preprocessor_n_plus.pkl")

    st.markdown("<h1 style='font-size:50px; margin-bottom:0.5rem;'>Predykcja N+</h1>", unsafe_allow_html=True)
    st.warning('Ten model nie nadaje się do użytku medycznego. Tylko do celów badawczych.', icon="⚠️")



    col1, col2 = st.columns([1, 1], gap="large")

    with col1:
        with st.form("input_form"):
            form_col1, form_col2 = st.columns([1, 1], gap="large")
            with form_col1:
                st.write("## Ogólne")
                st.number_input("Wiek", key="wiek", min_value=0, max_value=100, value=None, step=1)
                st.number_input("PSA", key="PSA", min_value=0.0, max_value=1000.0, value=None, step=0.01)
                st.write("## Wyniki MRI")
                st.number_input("Objętość", key="MRI vol", min_value=0.0, max_value=None, value=None, step=0.1)
                st.number_input("Rozmiar zmiany", key="MRI SIZE", min_value=0.0, max_value=None, value=None, step=0.1)
            with form_col2:
                st.selectbox("Pirads", options=[1,2,3,4,5], key="MRI Pirads")
                st.selectbox("EPE", key="MRI EPE", options=["Nie","Tak"])
                st.selectbox("SVI", key="MRI SVI", options=["Nie","Tak"])
                st.write("## Wyniki biopsji")
                st.selectbox("Gleason", key="Bx ISUP Grade", options=[0,1,2,3,4,5])

            st.divider()

            submitted = st.form_submit_button("Sprawdź", width='stretch', key="predict_button")


    with col2:
        st.write("## Wynik modelu")   
        if submitted:
            if st.session_state["wiek"] is None:
                st.error("Please enter a valid number for Age.")
            elif st.session_state["PSA"] is None:
                st.error("Please enter a valid number for PSA.")
            elif st.session_state["MRI vol"] is None:
                st.error("Please enter a valid number for MRI Volume.")
            elif st.session_state["MRI SIZE"] is None:
                st.error("Please enter a valid number for MRI Lesion size.")
            else:
                with st.spinner('Przewiduwanie...'):
                    prediction, prediction_prob, df = get_prediction(st.session_state, model, preprocessor, target="N+")
                
                # bg_color = "#77dd77"
                bg_color = "green"
                if prediction_prob[0] > 0.8:
                    # bg_color = "#f8625a"
                    bg_color = "red"
                elif prediction_prob[0] > 0.5:
                    # bg_color = "#ffd580"
                    # bg_color = "#3e4116"
                    bg_color = "orange"
                st.divider()
                col3, col4 = st.columns([1, 1], gap="small")
                with col3:
                    st.markdown(f"### Czy N+ jest obecne?", unsafe_allow_html=True)
                    st.markdown(f"### Prawdopodobieństwo wystąpienia N+:", unsafe_allow_html=True)
                with col4:
                    st.markdown(f"### <span id='result' style='color:white; background:{bg_color}'> {"tak" if prediction[0] else "nie"}</span>", unsafe_allow_html=True)
                    st.markdown(f"### <span id='result' style='color:white; background:{bg_color}'>{prediction_prob[0]:.2f}</span>", unsafe_allow_html=True)
                
                st.divider()