"""Feast feature view definitions for login fraud/risk scoring."""
from feast import FeatureView, Field
from feast.types import Float32, Int64

risk_features = FeatureView(
    name="risk_features",
    ttl=None,
    schema=[
        Field(name="failed_logins_last_hour", dtype=Int64),
        Field(name="avg_login_distance_km", dtype=Float32),
    ],
)
