import os
import requests
from requests.models import HTTPError

srv_namespace = "dataset_neo4j"
CONFIG_CENTER = "http://10.3.7.222:5062" \
    if os.environ.get('env') == "test" \
    else "http://common.utility:5062"


def vault_factory() -> dict:
    url = CONFIG_CENTER + \
        "/v1/utility/config/{}".format(srv_namespace)
    config_center_respon = requests.get(url)
    if config_center_respon.status_code != 200:
        raise HTTPError(config_center_respon.text)
    return config_center_respon.json()['result']


class ConfigClass(object):
    vault = vault_factory()
    env = os.environ.get('env')
    disk_namespace = os.environ.get('namespace')
    version = "0.1.0"

    NEO4J_URL = vault['NEO4J_URL']
    DATAOPS = vault["DATA_OPS_UTIL"]

    NEO4J_USER = os.environ['NEO4J_USER']
    NEO4J_PASS = os.environ['NEO4J_PASS']

    # the packaged modules
    api_modules = ["neo4j_api"]

