# flask configs
import os
class ConfigClass(object):

    # graph database
    NEO4J_URL = "bolt://neo4j-db.utility:7687"
    if os.environ['env'] == 'test':
        NEO4J_URL = "bolt://10.3.7.229:7687"
        DATAOPS = "http://10.3.7.239:5063"

    NEO4J_USER = os.environ['NEO4J_USER']
    NEO4J_PASS = os.environ['NEO4J_PASS']

    # the packaged modules
    api_modules = ["neo4j_api"]
