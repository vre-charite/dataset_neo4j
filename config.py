import os
from functools import lru_cache
from typing import Any
from typing import Dict
from typing import List

import requests
from pydantic import BaseSettings
from pydantic import Extra
from requests.models import HTTPError

SRV_NAMESPACE = os.environ.get('APP_NAME', 'dataset_neo4j')
CONFIG_CENTER_ENABLED = os.environ.get('CONFIG_CENTER_ENABLED', 'false')
CONFIG_CENTER_BASE_URL = os.environ.get('CONFIG_CENTER_BASE_URL', 'NOT_SET')


def load_vault_settings(settings: BaseSettings) -> Dict[str, Any]:
    if CONFIG_CENTER_ENABLED == 'false':
        return {}

    return vault_factory(CONFIG_CENTER_BASE_URL)


def vault_factory(config_center: str) -> Dict[Any, Any]:
    url = f'{config_center}/v1/utility/config/{SRV_NAMESPACE}'
    config_center_response = requests.get(url)

    if config_center_response.status_code != 200:
        raise HTTPError(config_center_response.text)

    return config_center_response.json()['result']


class Settings(BaseSettings):
    """Store service configuration settings."""

    PORT: int = 5062
    HOST: str = '0.0.0.0'
    LOGLEVEL: str = 'info'
    WORKERS: int = 4
    THREADS: int = 2
    WORKER_CONNECTIONS: int = 5
    DEBUG: bool = True
    NEO4J_URL: str
    NEO4J_USER: str
    NEO4J_PASS: str
    DATA_OPS_UTIL: str
    API_MODULES: List[str] = ['neo4j_api']

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'
        extra = Extra.allow

        @classmethod
        def customise_sources(cls, init_settings, env_settings, file_secret_settings):
            return load_vault_settings, env_settings, init_settings, file_secret_settings


@lru_cache(1)
def get_settings():
    """Return service settings."""

    settings = Settings()
    return settings


class ConfigClass:
    settings = get_settings()
    version = '0.1.0'
    NEO4J_URL = settings.NEO4J_URL
    NEO4J_USER = settings.NEO4J_USER
    NEO4J_PASS = settings.NEO4J_PASS
    DATAOPS = settings.DATA_OPS_UTIL
    API_MODULES = settings.API_MODULES
