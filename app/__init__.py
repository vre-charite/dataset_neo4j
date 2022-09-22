# Copyright 2022 Indoc Research
# 
# Licensed under the EUPL, Version 1.2 or – as soon they
# will be approved by the European Commission - subsequent
# versions of the EUPL (the "Licence");
# You may not use this work except in compliance with the
# Licence.
# You may obtain a copy of the Licence at:
# 
# https://joinup.ec.europa.eu/collection/eupl/eupl-text-eupl-12
# 
# Unless required by applicable law or agreed to in
# writing, software distributed under the Licence is
# distributed on an "AS IS" basis,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either
# express or implied.
# See the Licence for the specific language governing
# permissions and limitations under the Licence.
# 

import importlib

from flask import Flask
from flask_cors import CORS
from opentelemetry import trace
from opentelemetry.exporter.jaeger.thrift import JaegerExporter
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from opentelemetry.sdk.resources import SERVICE_NAME
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor

from app.opentelemetry.instrumentation.py2neo import Py2NeoInstrumentor
from config import ConfigClass
from config import get_settings


def create_app() -> Flask:
    """Initialize and configure app."""

    app = Flask(__name__)
    app.config.from_object(__name__ + '.ConfigClass')
    CORS(
        app,
        origins='*',
        allow_headers=['Content-Type', 'Authorization', 'Access-Control-Allow-Credentials'],
        supports_credentials=True,
        intercept_exceptions=False,
    )

    # dynamic add the dataset module by the config we set
    for apis in ConfigClass.API_MODULES:
        api = importlib.import_module(apis)
        api.module_api.init_app(app)

    instrument_app(app)

    return app


def instrument_app(app: Flask) -> None:
    """Instrument the application with OpenTelemetry tracing."""

    settings = get_settings()

    if not settings.OPEN_TELEMETRY_ENABLED:
        return

    tracer_provider = TracerProvider(resource=Resource.create({SERVICE_NAME: settings.APP_NAME}))
    trace.set_tracer_provider(tracer_provider)

    Py2NeoInstrumentor().instrument()
    FlaskInstrumentor().instrument_app(app)

    jaeger_exporter = JaegerExporter(
        agent_host_name=settings.OPEN_TELEMETRY_HOST, agent_port=settings.OPEN_TELEMETRY_PORT
    )

    tracer_provider.add_span_processor(BatchSpanProcessor(jaeger_exporter))
