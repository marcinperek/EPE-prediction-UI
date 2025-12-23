import dalex as dx
from sklearn.pipeline import Pipeline
import pandas as pd
import warnings

warnings.simplefilter(action='ignore', category=FutureWarning)

def get_explanation(patient, model, preprocessor, target='EPE'):
    pipeline = Pipeline(steps=[
        ('preprocessor', preprocessor),
        ('model', model)
    ])
    if target == 'EPE':
        X = pd.read_csv('data/X_train_epe_rp.csv')
        y = pd.read_csv('data/y_train_epe_rp.csv')
    elif target == 'N+':
        X = pd.read_csv('data/X_train_n_plus.csv')
        y = pd.read_csv('data/y_train_n_plus.csv')
    else:
        raise ValueError(f"Incorrect target specified: {target}")
    
    explainer = dx.Explainer(pipeline, X, y, verbose=False)
    return explainer.predict_parts(patient[X.columns], random_state=42).plot(show=False)