import pandas as pd

def get_prediction(session_state, model, preprocessor):
    numerical_cols = ['wiek', 'PSA', 'MRI vol', 'MRI SIZE']
    categorical_cols = ['MRI Pirads', 'MRI EPE', 'MRI EPE L', 'MRI EPE P', 'MRI SVI', 'MRI SVI L', 'MRI SVI P','Bx ISUP Grade P', 'Bx ISUP Grade L', 'Bx ISUP Grade']

    input_data = {col: [session_state[col]] for col in numerical_cols + categorical_cols}
    import pandas as pd
    input_df = pd.DataFrame(input_data)
    input_df['PSAdensity'] = input_df['PSA'] / (input_df['MRI vol'] + 1e-6)
    input_processed = preprocessor.transform(input_df)
    return model.predict(input_processed), model.predict_proba(input_processed)[:, 1]