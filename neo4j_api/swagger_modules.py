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

    "role": fields.String(readOnly=False, description="(User) user's role in platform"),
    "status": fields.String(readOnly=False, description="(User) The user's status"),

    "name": fields.String(readOnly=False, description='(Dataset) The name of the node(allow duplication)'),
    "code": fields.String(readOnly=False, description='(Dataset) The project code used for creating project'),
    "discoverable": fields.String(readOnly=False,
                                  description='(Dataset) Whether the project should be discovered by all platform user, or only project members'),
    "tags": fields.List(fields.String, readOnly=False, description="(Dataset) The tags added to the project"),

    "new_property_1": fields.String(readOnly=False, description='If property does not exist, neo4j will create it'),
    "update_property_2": fields.String(readOnly=False, description='If property exist, neo4j will update value'),
})


node_create_module = module_api.model('node_create_module', {
    "name": fields.String(readOnly=False, description='The name of the node(allow duplication)'),
    "path": fields.String(readOnly=False, description='The path store in nfs'),

    "email": fields.String(readOnly=False, description='(User) The email that user used for self-registrar'),
    "first_name": fields.String(readOnly=False, description='(User) The first name that user used for self-registrar'),
    "last_name": fields.String(readOnly=False, description='(User) The last name that user used for self-registrar'),
    "role": fields.String(readOnly=False, description="(User) user's role in platform"),
    "status": fields.String(readOnly=False, description="(User) The user's status"),

    "code": fields.String(readOnly=False, description='(Dataset) The project code used for creating project'),
    "discoverable": fields.Boolean(readOnly=False, description='(Dataset) Whether the project should be discovered by all platform user, or only project members'),
    "roles": fields.List(fields.String, readOnly=False, description="(Dataset) The possible roles in the project"),
    "type": fields.String(readOnly=False, description="(Dataset) The type of project, default is 'Usecase'"),
    "tags": fields.List(fields.String, readOnly=False, description="(Dataset) The tags added to the project"),
    "metadatas": fields.Wildcard(fields.String, readOnly=False, description="(Dataset) Default value {}"),


    "other_property_1": fields.String(readOnly=False, description='(optional) others are the attributes you want to attach to node'),
    "other_property_2": fields.String(readOnly=False, description='(optional) others are the attributes you want to attach to node'),
})

node_query_module = module_api.model('node_query_module', {
    "property_key": fields.String(readOnly=True, description='the key value pairs that node has corresponding attribute'),
})


#######################################################################