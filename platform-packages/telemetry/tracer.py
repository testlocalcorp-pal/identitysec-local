"""OpenTelemetry setup shared across Python services."""
from opentelemetry import trace

tracer = trace.get_tracer("identitysec.platform")
