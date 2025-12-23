import dalex as dx
from sklearn.pipeline import Pipeline
import pandas as pd
import warnings

warnings.simplefilter(action='ignore', category=FutureWarning)

def get_explanation(patient, model, preprocessor):
    pipeline = Pipeline(steps=[
        ('preprocessor', preprocessor),
        ('model', model)
    ])
    X = pd.read_csv('data/X_epe_rp_full.csv')
    explainer = dx.Explainer(pipeline, X, verbose=False)
    return explainer.predict_parts(patient[X.columns], keep_distributions=True).plot(show=False)