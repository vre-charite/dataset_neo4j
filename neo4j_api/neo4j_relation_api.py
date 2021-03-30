from flask import request, make_response, jsonify
# from flask_restful import Resource
from flask_restx import Api, Resource, fields

from neo4j_api.neo4j_base import Neo4jRelationship, Neo4jClient
from utils import neo4j_obj_2_json, node_2_json, path_2_json
from . import relationship_ns, module_api
from neo4j_api.swagger_modules import *


class RelationshipActions(Resource):
    neo4j_method = Neo4jClient()

    post_module = module_api.model('relation_add_module', {
        'start_id': fields.Integer(readOnly=True, description='Id of the start node (User)'),
        'end_id': fields.Integer(readOnly=True, description='Id of the end node (Dataset)')
    })

    # recieve the parameter to add edge between two
    @relationship_ns.expect(post_module)
    @relationship_ns.response(200, 'success')
    @relationship_ns.response(403, 'Exception')
    @relationship_ns.doc(params={'label': 'admin/contributor'})
    def post(self, label):
        """
        add the relationship between the two node
        Usage: used for adding user to the project
        """
        post_data = request.get_json()
        # get from the query
        start_id = post_data.get('start_id', None)
        end_id = post_data.get('end_id', None)
        if not start_id and not end_id:
            return 'start_id and end_id are required', 403

        # make the label between node to node
        try:
            self.neo4j_method.add_relation_between_nodes(
                label, start_id, end_id)
        except Exception as e:
            return str(e), 403

        return 'success', 200

    @relationship_ns.expect(post_module)
    @relationship_ns.response(200, 'success')
    @relationship_ns.response(403, 'Exception')
    @relationship_ns.doc(params={'label': 'admin/contributor'})
    def put(self, label):
        """
        Change the relationship between the two node if exist by label
        Usage: used for changing relationship between user and project
        """
        post_data = request.get_json()
        # get from the query
        start_id = post_data.get('start_id', None)
        end_id = post_data.get('end_id', None)
        new_label = post_data.get('new_label', None)
        properties = post_data.get('properties', {})
        if not start_id or not end_id or not new_label:
            return 'start_id, new_label and end_id are required', 403
        
        # also if new and old are the same
        if label == new_label and not properties:
            return 'success', 200
            
        # make the label between node to node
        try:
            res = self.neo4j_method.update_relation(
                label, new_label, start_id, end_id, properties=properties)
        except Exception as e:
            return str(e), 403

        return 'success', 200


class RelationshipActionsLabelOption(Resource):
    neo4j_method = Neo4jClient()

    get_return = """
    [
        {"p": {
            <username>: {
                        "id": <user-id>, 
                        "children": {
                                <projcet-name>: {
                                        "id": <project-id>,
                                        "children": {}
                                                }
                                        }
                                }
                        },
         "r": {"type": <relation-label>},
        }
    ]
    """

    # the start id and end id will be in the query string
    @relationship_ns.response(200, get_return)
    @relationship_ns.response(403, 'Exception')
    @relationship_ns.doc(params={"params":"{'start_id': 'start node id (User)', "
                                          "'end_id': 'end node id (Dataset)', "
                                          "'label': 'relation label (admin/contributor)'}"})
    def get(self):
        """
        Get the relationship between the two node if exist by label
        Usage: get relation between user and project
        """
        # get from the query
        start_id = request.args.get('start_id', None)
        end_id = request.args.get('end_id', None)
        label = request.args.get('label', None)
        if not start_id and not end_id:
            return 'start_id and end_id are required', 403

        try:
            # change to int
            start_id = int(start_id) if start_id else None
            end_id = int(end_id) if end_id else None

            result = self.neo4j_method.get_relation(label, start_id, end_id)
            type = None
            for i in result:
                type = next(iter(i.types()))
            if result:
                result = [{'p': path_2_json(result[0]), 'r': {"type": type, "status": result[0].get("status")}}]

        except Exception as e:
            return str(e), 403

        return result, 200

    @relationship_ns.response(200, 'success')
    @relationship_ns.response(403, 'Exception')
    @relationship_ns.doc(params={"params": "{'start_id': 'start node id', "
                                           "'end_id': 'end node id'}"})
    def delete(self):
        """
        delete the relationship between two nodes
        Usage: remove user from project
        """
        # get from the query
        start_id = request.args.get('start_id', None)
        end_id = request.args.get('end_id', None)
        if not start_id and not end_id:
            return 'start_id and end_id are required', 403

        start_id = int(start_id) if start_id else None
        end_id = int(end_id) if end_id else None

        try:
            res = self.neo4j_method.delete_relation(start_id, end_id)

        except Exception as e:
            return str(e), 403
        return 'success', 200


class ActionOnNodeByRelationships(Resource):
    neo4j_method = Neo4jRelationship()


    get_return = """
    [
        {
            "id": <ID>,
            "labels": [
                <node-label>
            ],
            "path": <nfs-path>,
            "time_lastmodified": <time-string>,
            "name": <node-name>,
            "time_created": <time-string>
        }
    ]
    """

    @relationship_ns.deprecated
    @relationship_ns.response(200, get_return)
    @relationship_ns.response(403, 'Exception')
    @relationship_ns.doc(params={'label': 'PARENT/CHILDREN', 'id': 'Node ID'})
    def get(self, label, id):
        """
        Get the nodes along the relationship
        Git:
        https://git.indocresearch.org/charite/core/blob/k8s-dev/portal/backend/api/api_dataset/dataset_operation_neo4j.py#L274
        """
        # get from the query
        start = request.args.get('start', True)
        if start == 'False':
            start = False
        else:
            start = True

        try:
            res = self.neo4j_method.get_node_along_relation(
                label, int(id), start)
            result = [neo4j_obj_2_json(x).get('node') for x in res]
        except Exception as e:
            return str(e), 403

        return result, 200


class ActionOnRelationshipByQuery(Resource):
    neo4j_method = Neo4jRelationship()

    post_module = module_api.model('relation_query_module', {
        'label': fields.String(readOnly=True, description='Label of relationship'),
        'start_label': fields.String(readOnly=True, description="Label of start node, normally use as 'User'"),
        'end_label': fields.String(readOnly=True, description="Label of end node, normally use as 'Dataset"),
        'start_params': fields.Raw(readOnly=True, description='Json attributes start node has, such as id, name, email and so on'),
        'end_params': fields.Raw(readOnly=True, description='Json attributes end node has, such as id, code, name and so on')
    })

    complex_query_return = """
    [
        {'end_node': {
                'id': <node-id>, 
                'labels': ['Dataset'], 
                'path': <nfs-path>, 
                'code': <project-code>, 
                'time_lastmodified': <time-string>, 
                'discoverable': True, 
                'roles': [<project-role>], 
                'name': <project-name>, 
                'time_created': <time-string>,
                'description: <project-description> 
                'admin': ['admin'], 
                'type': 'Usecase',
                'tags': [<tags>]
                        }, 
         'p': {
                'admin': {
                        'id': 0,
                        'children': {
                                'NOV-1130-2': {
                                        'id': 259, 
                                        'children': {}
                                                }
                                    }
                        }
                }, 
         'r': {'type': <relation-label>},
         'start_node': {
                'id': <node-id>,
                'labels': ['User'],
                'path': 'users',
                'time_lastmodified': <time-string>,
                'role': 'admin', 
                'last_login': '2020-12-01T16:13:30.103658', 
                'name': 'admin', 
                'last_name': 'admin', 
                'first_name': 'admin', 
                'email': 'siteadmin.test@vre.com', 
                'status': 'active'
                        }
        }, 
    ]
    """

    @relationship_ns.expect(post_module)
    @relationship_ns.response(200, complex_query_return)
    @relationship_ns.response(403, 'Exception')
    def post(self):
        """
        Get the relationship by the properties of node
        Usage: used for getting all users in the project, or getting all admins, or check if relationship exists
        """

        # get the detail of the node infomation
        post_data = request.get_json()
        # to see the end label and start label and also payload
        label = post_data.get('label', None)
        start_label = post_data.get('start_label', None)
        end_label = post_data.get('end_label', None)
        start_params = post_data.get('start_params', None)
        end_params = post_data.get('end_params', None)
        sort_node = post_data.get('sort_node', 'end')
        partial = post_data.get('partial', False)
        extra_query = post_data.get('extra_query', "")
        page_kwargs = {
            "limit": post_data.get("limit", None),
            "skip": post_data.get("skip", None),
            "order_by": post_data.get("order_by"),
            "order_type": post_data.get("order_type"),
        }

        # then call the function to see if we can get the infomation
        try:
            res = self.neo4j_method.get_relation_with_params(
                label, 
                start_label, 
                end_label, 
                start_params, 
                end_params, 
                partial=partial, 
                page_kwargs=page_kwargs,
                extra_query=extra_query,
                sort_node=sort_node,
            )
        except Exception as e:
            return str(e), 403
        result = []
        for x in res:
            result.append(neo4j_obj_2_json(x))

        return result, 200


class CountActionOnRelationshipByQuery(Resource):
    neo4j_method = Neo4jRelationship()

    post_returns = """
            {"count": <number-of-records>}
        """

    relation_query_module_count = module_api.model('relation_query_module_count', {
        "count": fields.Boolean(readOnly=True, description='number of records'),
        "partial": fields.Boolean(readOnly=True, description='whether enable partial search'),
        "start_label": fields.String(readOnly=True,
                                         description="Label of start node, normally use 'User'"),
        "end_label": fields.String(readOnly=True,
                                          description="Label of end node, normally use 'Dataset'"),
        'start_params': fields.Raw(readOnly=True,
                                        description="start_node(User) attributes, such as {'name': <user-name>} or {'email': <user-email>}"),
        'end_params': fields.Raw(readOnly=True,
                                      description="end_node(Dataset) attributes, such as {'code': <project-code>}")
    })

    @relationship_ns.expect(relation_query_module_count)
    @relationship_ns.response(200, post_returns)
    @relationship_ns.response(403, 'Exception')
    def post(self):
        """
        Count the number of relationships by the properties of node
        Usage: used for getting number of pages in the project
        """
        # get the detail of the node infomation
        post_data = request.get_json()
        # to see the end label and start label and also payload
        label = post_data.get('label', None)
        start_label = post_data.get('start_label', None)
        end_label = post_data.get('end_label', None)
        start_params = post_data.get('start_params', None)
        end_params = post_data.get('end_params', None)
        partial = post_data.get('partial', False)
        extra_query = post_data.get('extra_query', "")

        # then call the function to see if we can get the infomation
        try:
            res = self.neo4j_method.get_relation_with_params(
                label, start_label, end_label, start_params, end_params, partial=partial, count=True, extra_query=extra_query)
        except Exception as e:
            return str(e), 403

        return {"count": res.value()[0]}, 200


class RelationshipQueryV2(Resource):
    client = Neo4jRelationship()

    def post(self):
        post_data = request.get_json()
        start_label = post_data.get("start_label", None)
        end_labels = post_data.get("end_labels", None)
        query = post_data.get("query", {})
        page_kwargs = {
            "limit": post_data.get("limit", None),
            "skip": post_data.get("skip", None),
            "order_by": post_data.get("order_by"),
            "order_type": post_data.get("order_type"),
        }
        if not query.get("start_params"):
            return "start_params required", 400 
        result = []
        try:
            res, total = self.client.relation_query_multiple_labels(start_label, end_labels, query_params=query, page_kwargs=page_kwargs)
            for x in res:
                result.append(neo4j_obj_2_json(x)["end_node"])
        except Exception as e:
            return str(e), 403
        response = {
            "results": result,
            "total": total,
        }
        return response 

class RelationConnected(Resource):
    client = Neo4jRelationship()

    get_return = """
    {
        "result": [
            {
                "id": 4637,
                "labels": [
                    "Greenroom",
                    "Folder"
                ],
                "global_entity_id": "ebba4426-8b3a-11eb-8a88-eaff9e667817-1616437074",
                "folder_level": 2,
                "folder_relative_path": "a/b",
                "time_lastmodified": "2021-03-22T18:17:54",
                "uploader": "zhengyang",
                "name": "c",
                "time_created": "2021-03-22T18:17:54",
                "project_code": "gregtest",
                "priority": 0,
                "tags": []
            },
            {
                "id": 4693,
                "labels": [
                    "Greenroom",
                    "Folder"
                ],
                "global_entity_id": "eb4e43ac-8b3a-11eb-99fe-eaff9e667817-1616437073",
                "folder_level": 1,
                "folder_relative_path": "a",
                "time_lastmodified": "2021-03-22T18:17:53",
                "uploader": "zhengyang",
                "name": "b",
                "time_created": "2021-03-22T18:17:53",
                "project_code": "gregtest",
                "priority": 0,
                "tags": []
            },
            {
                "id": 4690,
                "labels": [
                    "Greenroom",
                    "Folder"
                ],
                "global_entity_id": "eb247a72-8b3a-11eb-be94-eaff9e667817-1616437073",
                "folder_level": 0,
                "folder_relative_path": "",
                "time_lastmodified": "2021-03-22T18:17:53",
                "uploader": "zhengyang",
                "name": "a",
                "time_created": "2021-03-22T18:17:53",
                "project_code": "gregtest",
                "priority": 0,
                "tags": []
            },
            {
                "id": 21,
                "labels": [
                    "Dataset"
                ],
                "global_entity_id": "dataset-4f640b7e-85be-11eb-99fe-eaff9e667817-1615833798",
                "path": "gregtest",
                "code": "gregtest",
                "time_lastmodified": "2021-03-15T18:43:18",
                "system_tags": [
                    "copied-to-core"
                ],
                "discoverable": true,
                "name": "gregtest",
                "time_created": "2021-02-01T16:04:13",
                "description": "test",
                "type": "Usecase"
            }
        ]
    }
    """

    @relationship_ns.response(200, get_return)
    def get(self, geid):
        client = Neo4jRelationship()
        """
        Get the nodes by the properties of node
        """
        try:
            res = self.client.get_connected_nodes(geid)
            result = []
            for x in res:
                result.append(neo4j_obj_2_json(x)["node"])
            return {"result": result}, 200
        except Exception as e:
            print(e)
            return str(e), 403
