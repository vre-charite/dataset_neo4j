from flask import request, make_response, jsonify
# from flask_restful import Resource
from flask_restx import Api, Resource, fields

from neo4j_api.neo4j_base import Neo4jRelationship
from utils import neo4j_obj_2_json
from . import relationship_ns, module_api
from neo4j_api.swagger_modules import *


class RelationshipActions(Resource):
    neo4j_method = Neo4jRelationship()

    post_module = module_api.model('id_payload', {
        'start_id': fields.Integer(readOnly=True, description='Id of the start node'),
        'end_id': fields.Integer(readOnly=True, description='Id of the end node')
    })

    # recieve the parameter to add edge between two
    @relationship_ns.expect(post_module)
    def post(self, label):
        """
        add the relationship between the two node
        """
        post_data = request.get_json()
        # get from the query
        start_id = post_data.get('start_id', None)
        end_id = post_data.get('end_id', None)
        if not start_id and not end_id:
            return 'start_id and end_id are required', 403

        # make the label between node to node
        try:
            res = self.neo4j_method.add_relation_between_nodes(
                label, start_id, end_id)
        except Exception as e:
            return str(e), 403

        return 'success', 200

    @relationship_ns.expect(post_module)
    def put(self, label):
        """
        Change the relationship between the two node if exist by label
        """
        post_data = request.get_json()
        # get from the query
        start_id = post_data.get('start_id', None)
        end_id = post_data.get('end_id', None)
        new_label = post_data.get('new_label', None)
        if not start_id or not end_id or not new_label:
            return 'start_id, new_label and end_id are required', 403
        
        # also if new and old are the same
        if label == new_label:
            return 'success', 200
            
        print(start_id, end_id, new_label)

        # make the label between node to node
        try:
            res = self.neo4j_method.update_relation(
                label, new_label, start_id, end_id)
        except Exception as e:
            return str(e), 403

        return 'success', 200


class RelationshipActionsLabelOption(Resource):
    neo4j_method = Neo4jRelationship()

    get_return = """
    [
        {
            "p": {
                "test_grand_parent_dataset_0b42d471-63c8-4869-8972-26223806e9b4": {
                    "id": 171,
                    "children": {
                        "test_parent_dataset_0b42d471-63c8-4869-8972-26223806e9b4": {
                            "id": 170,
                            "children": {}
                        }
                    }
                }
            },
            "r": {
                "type": "PARENT"
            },
            "node":{
                "id": <ID>,
                "labels": [
                    <node-label>
                ],
                "path": <nfs-path>,
                "time_lastmodified": <time-string>,
                "name": <node-name>,
                "time_created": <time-string>,
                "other_property": "xxxx",
                "other_property_2": "xxxx"
            }
        }
    ]
    """

    # the start id and end id will be in the query string
    @relationship_ns.response(200, get_return)
    def get(self):
        """
        Get the relationship between the two node if exist by label
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

        except Exception as e:
            return str(e), 403

        print(result)
        return result, 200


    def delete(self):
        """
        delete the relationship between two nodes
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

    @relationship_ns.response(200, get_return)
    def get(self, label, id):
        """
        Get the nodes along the relationship
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

    post_module = module_api.model('query_on_relation_between_nodes', {
        'label': fields.String(readOnly=True, description='Label of relationship'),
        'start_label': fields.String(readOnly=True, description='Label of start node'),
        'end_label': fields.String(readOnly=True, description='Label of end node'),
        'start_params': fields.Nested(node_query_module, readOnly=True, description='Json attributes start node has'),
        'end_params': fields.Nested(node_query_module, readOnly=True, description='Json attributes end node has')
    })

    complex_query_return = """
    [
        {
            "p": {
                "test_grand_parent_dataset_0b42d471-63c8-4869-8972-26223806e9b4": {
                    "id": 171,
                    "children": {
                        "test_parent_dataset_0b42d471-63c8-4869-8972-26223806e9b4": {
                            "id": 170,
                            "children": {}
                        }
                    }
                }
            },
            "r": {
                "type": "PARENT"
            },
            "node":{
                "id": <ID>,
                "labels": [
                    <node-label>
                ],
                "path": <nfs-path>,
                "time_lastmodified": <time-string>,
                "name": <node-name>,
                "time_created": <time-string>,
                "other_property": "xxxx",
                "other_property_2": "xxxx"
            }
        }
    ]
    """

    @relationship_ns.expect(post_module)
    @relationship_ns.response(200, complex_query_return)
    def post(self):
        """
        Get the relationship by the properties of node
        """

        # get the detail of the node infomation
        post_data = request.get_json()
        # to see the end label and start label and also payload
        label = post_data.get('label', None)
        start_label = post_data.get('start_label', None)
        end_label = post_data.get('end_label', None)
        start_params = post_data.get('start_params', None)
        end_params = post_data.get('end_params', None)

        # then call the function to see if we can get the infomation
        try:
            res = self.neo4j_method.get_relation_with_params(
                label, start_label, end_label, start_params, end_params)
        except Exception as e:
            return str(e), 403

        result = []
        for x in res:
            # print(x)
            result.append(neo4j_obj_2_json(x))

        return result, 200


class ActionOnNodeBeyondRelationship(Resource):
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

    @relationship_ns.response(200, get_return)
    def get(self, label, id):
        """
        Get the nodes by the properties of node
        """
        try:
            res = self.neo4j_method.get_nodes_outside_relation(label, int(id))
            result = [neo4j_obj_2_json(x).get('node') for x in res]
        except Exception as e:
            print(e)
            return str(e), 403

        return result, 200
