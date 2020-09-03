#
# so as the neo4j it requires the connection
# as the mandetory parameter in the config file
#

# from flask_restful import Api
from flask_restx import Api, Resource, fields
from config import ConfigClass
from neo4j import GraphDatabase

# first check the necessary config parameter
required_parameters = ["NEO4J_URL", "NEO4J_PASS", "NEO4J_USER"]
for x in required_parameters:
	if not getattr(ConfigClass, x, None):
		raise Exception("Error: Missing the attribute %s in config."%x)


neo4j_connection = GraphDatabase.driver(ConfigClass.NEO4J_URL, 
	auth=(ConfigClass.NEO4J_USER, ConfigClass.NEO4J_PASS),encrypted=False)


module_api = Api(version='1.0', title='Neo4j API',
    description='Neo4j API', doc='/v1/api-doc'
)

# create namespace for node
node_ns = module_api.namespace('Node Actions', description='Operation on Neo4j Nodes', path ='/')
# create namespace for relationship
relationship_ns = module_api.namespace('Relationship Actions', description='Operation on Neo4j Relationship', path ='/')


from .neo4j_node_api import (
	ActionOnNodeById, 
	CreateNode, 
	ActionOnNodeByQuery, 
	ActionOnProperty
)
from .neo4j_relation_api import (
	RelationshipActions, 
	RelationshipActionsLabelOption, 
	ActionOnRelationshipByQuery,
	ActionOnNodeByRelationships,
	ActionOnNodeBeyondRelationship
)


node_ns.add_resource(ActionOnNodeById, '/v1/neo4j/nodes/<label>/node/<id>')
node_ns.add_resource(CreateNode, '/v1/neo4j/nodes/<label>')
node_ns.add_resource(ActionOnNodeByQuery, '/v1/neo4j/nodes/<label>/query')

node_ns.add_resource(ActionOnProperty, '/v1/neo4j/nodes/<label>/properties')

relationship_ns.add_resource(RelationshipActions, '/v1/neo4j/relations/<label>')
relationship_ns.add_resource(RelationshipActionsLabelOption, '/v1/neo4j/relations')

relationship_ns.add_resource(ActionOnRelationshipByQuery, '/v1/neo4j/relations/query')
relationship_ns.add_resource(ActionOnNodeByRelationships, '/v1/neo4j/relations/<label>/node/<id>')

relationship_ns.add_resource(ActionOnNodeBeyondRelationship, '/v1/neo4j/relations/<label>/node/<id>/none')

# # Actions on specific dataset
# module_api.add_resource(dataset, '/v1/datasets/<dataset_id>')

# # relationship between dataset and dataset
# module_api.add_resource(dataset_relation_child, '/v1/datasets/<dataset_id>/relations/children')
# module_api.add_resource(dataset_relation_parent, '/v1/datasets/<dataset_id>/relations/parent')
# module_api.add_resource(dataset_relation_none, '/v1/datasets/<dataset_id>/relations/none')

# module_api.add_resource(files, '/v1/<dataset_id>/files')

# # Actions on multiple users
# module_api.add_resource(dataset_users, '/v1/datasets/<dataset_id>/users')

# # Actions on the specific user
# module_api.add_resource(dataset_user, '/v1/datasets/<dataset_id>/users/<username>')


# module_api.add_resource(users, '/v1/users')
# module_api.add_resource(user_dataset_query, '/v1/users/<username>/datasets')

# test for the general neo4j api
# module_api.add_resource(neo4j_node, '/v1/neo4j/node')
