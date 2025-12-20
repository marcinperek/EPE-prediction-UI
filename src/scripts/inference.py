import pandas as pd
numerical_cols = {"EPE": ['wiek', 'PSA', 'MRI vol', 'MRI SIZE'],
                  "N+": ['wiek', 'PSA', 'MRI vol', 'MRI SIZE']}
categorical_cols = {"EPE": ['MRI Pirads', 'MRI EPE', 'MRI EPE L', 'MRI EPE P', 'MRI SVI', 'MRI SVI L', 'MRI SVI P',
                            'Bx ISUP Grade P', 'Bx ISUP Grade L', 'Bx ISUP Grade'],
                    "N+": ['MRI Pirads', 'MRI EPE', 'MRI SVI', 'Bx ISUP Grade']}

def get_prediction(session_state, model, preprocessor, target):
    input_data = {col: [session_state[col]] for col in numerical_cols[target] + categorical_cols[target]}
    import pandas as pd
    input_df = pd.DataFrame(input_data)
    input_df['PSAdensity'] = input_df['PSA'] / (input_df['MRI vol'] + 1e-6)
    input_processed = preprocessor.transform(input_df)
    return model.predict(input_processed), model.predict_proba(input_processed)[:, 1], input_df