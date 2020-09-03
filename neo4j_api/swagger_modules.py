from flask_restx import Api, Resource, fields

from . import module_api

def return_all(res):
    return res

node_module = module_api.model('node_module', {
    "id": fields.Integer(readOnly=True, description='Unique id of neo4j node'),
    # "labels": fields.List(fields.String, readOnly=True, description='The labe of the node'),
    # "name": fields.String(readOnly=True, description='The name of the node(allow duplication)'),
    # "path": fields.String(readOnly=True, description='The path store in nfs'),
    # "time_created": fields.String(readOnly=True, description='Time when node is created'),
    # "time_lastmodified": fields.String(readOnly=True, description='The path store in nfs')
}, mask=return_all)

path_module_simple  = module_api.model('path_module_simple',{
    "id": fields.Integer(readOnly=True, description='Unique id of neo4j node'),
    "children": fields.String(readOnly=True, description='Nested dict')
})
path_module  = module_api.model('path_module',{
    "node_name": fields.Nested(path_module_simple, readOnly=True, description='node info and children info')
})

relation_module = module_api.model('relation_module',{
	"type": fields.String(readOnly=True, description='Label of relationship')
})

# genitic_module

property_module = module_api.model('property_module', {
    "property_key": fields.List(fields.String, readOnly=True, description='List of possible values'),
})

node_update_module = module_api.model('node_update_module', {
    "new_property_1": fields.String(readOnly=True, description='If property does not exist, neo4j will create it'),
    "update_property_2": fields.String(readOnly=True, description='If property exist, neo4j will update value'),
})

node_create_module = module_api.model('node_create_module', {
    "name": fields.String(readOnly=True, description='The name of the node(allow duplication)'),
    "path": fields.String(readOnly=True, description='The path store in nfs'),

    "other_property_1": fields.String(readOnly=True, description='others are the attributes you want to attach to node'),
    "other_property_2": fields.String(readOnly=True, description='others are the attributes you want to attach to node'),
})

node_query_module = module_api.model('node_create_module', {
    "property_key": fields.String(readOnly=True, description='the key value pairs that node has corresponding attribute'),
})


#######################################################################