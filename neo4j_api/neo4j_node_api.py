from flask import request, make_response, jsonify
# from flask_restful import Resource
from flask_restx import Api, Resource

from neo4j_api.neo4j_base import Neo4jNode
from utils import neo4j_obj_2_json
from . import node_ns
from neo4j_api.swagger_modules import (
    node_update_module, node_create_module,
    node_query_module)


class ActionOnNodeById(Resource):
    # initialize the class for using the method
    node_method = Neo4jNode()

    get_returns = """
        [
            {
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
        ]

    """

    @node_ns.response(200, get_returns)
    def get(self, label, id):
        """
        Get the Node by Input Id
        """
        try:
            res = self.node_method.get_node(label, int(id))
            result = [neo4j_obj_2_json(x).get("node") for x in res]
        except Exception as e:
            return str(e), 403

        return result, 200


    put_returns = """
        # Note: Please pass the entire attribute here
        # if you want to delete the attribute then you can remove it from json.
        # if you want to add the new attribtue then add key-value into json
        [
            {
                "id": <ID>,
                "labels": [
                    <node-label>
                ],
                "path": <nfs-path>,
                "time_lastmodified": <time-string>,
                "name": <node-name>,
                "time_created": <time-string>,
                "other_property": "xxxx",
                "other_property_2": "xxxx",
                "new_attribute":"new_value"
            }
        ]
    """

    @node_ns.expect(node_update_module)
    @node_ns.response(200, put_returns)
    def put(self, label, id):
        """
        Update the Node by Input Id
        """
        post_data = request.get_json()

        try:
            res = self.node_method.update_node(label, int(id), post_data)
            result = [neo4j_obj_2_json(x).get("node") for x in res]
        except Exception as e:
            return str(e), 403

        return result, 200


class CreateNode(Resource):
    # initialize the class for using the method
    node_method = Neo4jNode()

    post_returns = """
        [
            {
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
        ]

    """

    @node_ns.expect(node_create_module)
    @node_ns.response(200, post_returns)
    def post(self, label):
        """
        Create New Node with Given Label
        """
        post_data = request.get_json()

        # node name is required
        node_name = post_data.pop("name", None)
        try:
            res = self.node_method.add_node(label, node_name, post_data)
            result = [neo4j_obj_2_json(x).get("node") for x in res]
        except Exception as e:
            return str(e), 403

        return result, 200


class ActionOnNodeByQuery(Resource):
    # initialize the class for using the method
    node_method = Neo4jNode()

    post_returns = """
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

    # because we will pass the payload to search so I have to
    # use the post to get the nodes
    @node_ns.expect(node_query_module)
    @node_ns.response(200, post_returns)
    def post(self, label):
        """
        Make a Complex Query by Its Payload
        """
        post_data = request.get_json()

        try:
            res = self.node_method.query_node(label, post_data)
            result = [neo4j_obj_2_json(x).get("node") for x in res]
        except Exception as e:
            return str(e), 403

        return result, 200


class ActionOnProperty(Resource):
    # initialize the class for using the method
    node_method = Neo4jNode()

    get_returns = """
        {
            "attribute_1":["all possible value"],
            "attribute_2":["all possible value"],
        }
    """

    @node_ns.response(200, get_returns)
    def get(self, label):
        """
        Retreive the All the Property and Possible Value with Given Label
        """
        try:
            res = self.node_method.get_property_by_label(label)

            result = {}
            for x in res:
                temp = dict(x)
                result.update({temp["key"]: temp["options"]})
            
            # pop out the time type
            result.pop("time_lastmodified", None)
            result.pop("time_created", None)
        except Exception as e:
            return str(e), 403

        return result, 200
