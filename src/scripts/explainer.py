import dalex as dx
from utils.model import load_model, load_preprocessor
from sklearn.pipeline import Pipeline
import pandas as pd

model = load_model("models/xgb_epe_rp_model.json")
preprocessor = load_preprocessor("models/preprocessor_epe_rp.pkl")

pipeline = Pipeline(steps=[
    ('preprocessor', preprocessor),
    ('model', model)
])


X = pd.read_csv("data/X_test_epe_rp.csv")
explainer = dx.Explainer(pipeline, X)

# explainer.predict_parts(X.iloc[60]).plot()