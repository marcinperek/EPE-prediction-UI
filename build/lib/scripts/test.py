from utils.model import load_model, load_preprocessor

import pandas as pd

model = load_model("models/xgb_epe_rp_model.json")
preprocessor = load_preprocessor("models/preprocessor_epe_rp.pkl")

X_test = pd.read_csv("data/X_test_epe_rp.csv")
y_test = pd.read_csv("data/y_test_epe_rp.csv").squeeze()

X_test = preprocessor.transform(X_test)
y_pred = model.predict(X_test)
y_pred_probs = model.predict_proba(X_test)[:, 1]
print(y_pred, y_pred_probs)