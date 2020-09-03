# flask configs
import os
class ConfigClass(object):

    # graph database
    NEO4J_URL = "bolt://external-graphdb.utility:7687"
    NEO4J_USER = os.environ['NEO4J_USER']
    NEO4J_PASS = os.environ['NEO4J_PASS']

    # the packaged modules
    api_modules = ["neo4j_api"]
