# flask configs
import os
class ConfigClass(object):

    # graph database
    if os.environ['env'] == 'test':
        NEO4J_URL = "bolt://10.3.7.219:7687"
    else:
        NEO4J_URL = "bolt://neo4j-db.utility:7687"

    NEO4J_USER = os.environ['NEO4J_USER']
    NEO4J_PASS = os.environ['NEO4J_PASS']

    # the packaged modules
    api_modules = ["neo4j_api"]

