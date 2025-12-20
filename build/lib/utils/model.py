from xgboost import XGBClassifier

def load_model(model_path: str) -> XGBClassifier:
    model = XGBClassifier()
    model.load_model(model_path)
    return model

def load_preprocessor(preprocessor_path: str):
    import joblib
    preprocessor = joblib.load(preprocessor_path)
    return preprocessor