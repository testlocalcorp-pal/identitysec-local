"""Production login fraud/risk scoring model architecture (XGBoost)."""
import xgboost as xgb


def build_model(params: dict) -> xgb.XGBClassifier:
    return xgb.XGBClassifier(**params)
