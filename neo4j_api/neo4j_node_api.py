from flask import request, make_response, jsonify
# from flask_restful import Resource
from flask_restx import Api, Resource

from neo4j_api.neo4j_base import Neo4jNode, Neo4jClient
from utils import neo4j_obj_2_json, node_2_json
from . import node_ns
from neo4j_api.swagger_modules import (
    node_update_module, node_create_module,
    node_query_module)


class ActionOnNodeById(Resource):
    # initialize the class for using the method
    node_method = Neo4jClient()

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
    @node_ns.response(403, """Exception""")
    def get(self, label, id):
        """
        Get the Node by Input Id
        """
        try:
            result = self.node_method.get_node(label, int(id))
            if result:
                result = [node_2_json(result)]
            else:
                result = []
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
    @node_ns.response(403, 'Exception')
    def put(self, label, id):
        """
        Update the Node by Input Id
        """
        post_data = request.get_json()

        try:
            if len(post_data.keys()) == 1 and  "last_login" in post_data.keys():
                res = self.node_method.update_node(label, int(id), post_data, update_modified_time=False)
            else:
                res = self.node_method.update_node(label, int(id), post_data)
            result = [node_2_json(res)]
        except Exception as e:
            return str(e), 403

        return result, 200


class CreateNode(Resource):
    # initialize the class for using the method
    node_method = Neo4jClient()

    post_returns = """
    Dataset response:
    {
        "result": {
            "parent_relation": <relation-label>,
            "admin": [
                <admin-username>
            ],
            "time_lastmodified": <time-string>,
            "_key2": "value2",
            "path": <nfs-path/project/code>,
            "id": <ID>>,
            "time_created": <time-string>,
            "name": <node-name>
            "labels": [
                "Dataset"
            ],
            "_key1": "value1",
            "parent_id": <parent-id>,
            "tags": [
                "tag1",
                "tag2"
            ],
            "type": "Dataset"
        }
    }\n
    User response:
    {
        result: {
            "time_created": "2020-07-03T18:23:15",
            "first_name": <first-name>,
            "name": <user-name>,
            "time_lastmodified": <time-string>,
            "last_name": <last-name>,
            "path": "users",
            "role": <plstform-role>,
            "labels": [
                "User"
            ],
            "id": <ID>
        }
    }\n
    Other response:
    {'id': <ID>, 
    'labels': ['test_label'],
    'name': <node-name>,
    "time_created": <time-string>,
    "time_lastmodified": <time-string>,
    "parent_relation":  <relation>,
    "parent_id": <parent-node-ID>,
    "other_property": "xxxx"}
    """

    @node_ns.expect(node_create_module)
    @node_ns.response(200, post_returns)
    @node_ns.response(403, """Exception""")
    def post(self, label):
        """
        Create New Node with Given Label
        """
        post_data = request.get_json()

        # node name is required
        node_name = post_data.pop("name", None)
        try:
            res = self.node_method.add_node(label, node_name, post_data)
            result = [node_2_json(res)]
        except Exception as e:
            return str(e), 403

        return result, 200


class ActionOnNodeByQuery(Resource):
    # initialize the class for using the method
    node_method = Neo4jClient()

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
    @node_ns.response(403, """Exception""")
    def post(self, label):
        """
        Make a Complex Query by Its Payload
        """
        post_data = request.get_json()
        limit = None
        skip = None
        partial = False
        order_by = None
        order_type = None
        if post_data:
            if "partial" in post_data:
                partial = post_data["partial"]
                del post_data["partial"]
            if "limit" in post_data:
                limit = post_data["limit"] 
                del post_data["limit"]
            if "skip" in post_data:
                skip = post_data["skip"] 
                del post_data["skip"]
            if "order_by" in post_data:
                order_by = post_data["order_by"] 
                del post_data["order_by"]
            if "order_type" in post_data:
                order_type = post_data["order_type"] 
                del post_data["order_type"]

        try:
            nodes = self.node_method.query_node(
                label, 
                post_data, 
                limit=limit, 
                skip=skip, 
                partial=partial, 
                order_by=order_by,
                order_type=order_type
            )
            result = [node_2_json(x) for x in nodes]
        except Exception as e:
            return str(e), 403

        return result, 200


class CountActionOnNodeByQuery(Resource):
    # initialize the class for using the method
    node_method = Neo4jClient()

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

    @node_ns.expect(node_query_module)
    @node_ns.response(200, post_returns)
    @node_ns.response(403, """Exception""")
    def post(self, label):
        """
        Make a Complex Query by Its Payload
        """
        post_data = request.get_json()
        partial = False
        if "count" in post_data:
            del post_data["count"]
        if "partial" in post_data:
            partial = post_data["partial"]
            del post_data["partial"]

        try:
            res = self.node_method.query_node(label, post_data, count=True, partial=partial)
        except Exception as e:
            return str(e), 403

        return {"count": int(res)}, 200


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
    @node_ns.response(403, """Exception""")
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
