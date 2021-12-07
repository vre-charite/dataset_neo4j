import importlib

from flask import Flask
from flask_cors import CORS

from config import ConfigClass


def create_app():
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

    return app
