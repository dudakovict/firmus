from flask_jwt_extended import JWTManager
from prometheus_flask_exporter import RESTfulPrometheusMetrics

jwt = JWTManager()
metrics = RESTfulPrometheusMetrics.for_app_factory()