from flask_restx import Api, Resource
from flask import request
import math

from neo4j_api.swagger_modules import trashfile_module, file_module, file_query_module
from neo4j_api.neo4j_base import Neo4jClient, Neo4jRelationship
from utils import neo4j_obj_2_json, node_2_json
from . import file_ns


class FileAPI(Resource):
    node_method = Neo4jClient()
    response = """
        [   {   
            'archived': False,
            'file_size': 1024,
            'full_path': '/data/vre-storage/generate/raw/BCD-1234_file_2.aacn',
            'generate_id': 'BCD-1234_2',
            'guid': '5321880a-1a41-4bc8-a5d5-9767323205792',
            'id': 478,
            'labels': ['VRECore', 'File', 'Processed'],
            'name': 'BCD-1234_file_2.aacn',
            'namespace': 'core',
            'path': '/data/vre-storage/generate/raw',
            'process_pipeline': 'greg_testing',
            'time_created': '2021-01-06T18:02:55',
            'time_lastmodified': '2021-01-06T18:02:55',
            'type': 'processed',
            'uploader': 'admin',
            'operator': 'admin'
        }]
    """

    @file_ns.response(200, response)
    @file_ns.expect(file_module)
    def post(self):
        data = request.get_json()
        full_path = data.get("full_path")
        name = full_path.split("/")[-1]
        data["path"] = "/".join(full_path.split("/")[:-1])
        data["archived"] = False
        required_fields = ["full_path", "file_size", "archived", "path", "generate_id", "guid", "namespace", \
                "type", "uploader", "project_id"]
        for i in required_fields:
            if not i in data:
                return f"Missing required field {i}", 400

        if data["type"] == "processed":
            if not "process_pipeline" in data:
                return f"Missing required field {i}", 400
            if not "operator" in data:
                return f"Missing required field {i}", 400

        project_id = data.get("project_id")
        del data["project_id"]

        input_file_id = data.get("input_file_id")
        if input_file_id:
            del data["input_file_id"]

        extra_labels = [] 
        if data["namespace"] == "greenroom":
            extra_labels.append("Greenroom")
        else:
            extra_labels.append("VRECore")

        if data["type"] == "raw":
            extra_labels.append("Raw")
        else:
            extra_labels.append("Processed")
        del data["namespace"]
        del data["type"]
        data["extra_labels"] = extra_labels

        try:
            result = self.node_method.add_node("File", name, data)
            if result:
                result = [node_2_json(result)]
            else:
                result = []

            # Create Dataset to file relation
            self.node_method.add_relation_between_nodes("own", project_id, result[0]["id"])

            # Create input to processed relation
            if input_file_id:
                self.node_method.add_relation_between_nodes(data["process_pipeline"], input_file_id, result[0]["id"])
        except Exception as e:
            return str(e), 403

        return result, 200


class DatasetFileQueryAPI(Resource):
    node_method = Neo4jClient()

    response = """
        {   
            'code': 200,
            'error_msg': '',
            'num_of_pages': 14,
            'page': 1,
            'result': [   {   'archived': False,
                              'description': 'description',
                              'file_size': 0,
                              'full_path': 'test/zy/testzy9.txt',
                              'generate_id': '',
                              'guid': 'f1547da2-8372-4ae3-9e2b-17c80e97f113',
                              'id': 74,
                              'labels': ['Raw', 'File', 'Greenroom'],
                              'name': 'testzy9.txt',
                              'path': 'test/zy',
                              'time_created': '2021-01-08T17:09:51',
                              'time_lastmodified': '2021-01-08T17:09:51',
                              'uploader': 'testzy'},
             'total': 67
         }
    """

    @file_ns.response(200, response)
    @file_ns.expect(file_query_module)
    def post(self, dataset_id):
        data = request.get_json()
        partial = data.pop("partial", False)
        page = data.pop("page", 0)
        page_size = data.pop("page_size", 25)
        order_type = data.pop("order_type", "")
        if not order_type.lower() in ["desc", "asc"]:
            return "Invalid order_type", 400
        page_kwargs = {
            "order_by": data.pop("order_by", ""),
            "order_type": order_type,
            "skip": page * page_size,
            "limit": page_size
        }
        query = data.get("query")
        labels = query.pop("labels", None)
        if not labels:
            return "Missing required attribute labels", 400
        
        if not query:
            query = None
        relations = Neo4jRelationship().get_relation_with_params(
            "own", 
            "Dataset", 
            labels, 
            {"id": int(dataset_id)}, 
            query, 
            partial=partial, 
            page_kwargs=page_kwargs
        )
        nodes = []
        for x in relations:
            nodes.append(neo4j_obj_2_json(x)["end_node"])

        total = Neo4jRelationship().get_relation_with_params(
            "own", 
            "Dataset", 
            labels, 
            {"id": int(dataset_id)}, 
            query, 
            partial=partial, 
            count=True
        )
        total = total.value()[0]
        response = {
            'code': 200,
            'error_msg': '',
            'result': nodes,
            'page': page,
            'total': total,
            'num_of_pages': math.ceil(total / page_size),
        }

        return response, 200


class TrashFileAPI(Resource):
    node_method = Neo4jClient()
    response = """
        {   
            'archived': False,
            'file_size': 1024,
            'full_path': '/data/vre-storage/TRASH/generate/raw/BCD-1234_file_2.aacn',
            'generate_id': 'BCD-1234_2',
            'guid': '5321880a-1a41-4bc8-a5d5-9767323205792',
            'id': 478,
            'labels': ['VRECore', 'TrashFile', 'Processed'],
            'name': 'BCD-1234_file_2.aacn',
            'namespace': 'core',
            'path': '/data/vre-storage/TRASH/generate/raw',
            'time_created': '2021-01-06T18:02:55',
            'time_lastmodified': '2021-01-06T18:02:55',
            'uploader': 'admin',
        }
    """

    @file_ns.response(200, response)
    @file_ns.expect(trashfile_module)
    def post(self):
        data = request.get_json()
        full_path = data.get("full_path")
        trash_full_path = data.get("trash_full_path")
        name = trash_full_path.split("/")[-1]
        trash_path = "/".join(trash_full_path.split("/")[:-1])

        file_node = self.node_method.query_node("File", {"full_path": full_path})[0]
        file_node = node_2_json(file_node)

        labels = file_node.get("labels")
        labels.remove("File")
        trash_file_data = {
            "path": trash_path,
            "full_path": trash_full_path,
            "description": file_node.get("description"),
            "file_size": file_node.get("file_size"),
            "guid": file_node.get("guid"),
            "manifest_id": file_node.get("manifest_id", None),
            "generate_id": file_node.get("generate_id"),
            "archived": True,
            "extra_labels": labels
        } 
        for key, value in file_node.items():
            if key.startswith("attr_"):
                trash_file_data[key] = value 
        try:
            # Create TrashFile
            result = self.node_method.add_node("TrashFile", name, trash_file_data)
            result = node_2_json(result)

            # Get dataset
            relation_results = Neo4jRelationship().get_relation_with_params(
                start_label="Dataset", 
                end_label="File", 
                start_params=None, 
                end_params={"full_path": file_node["full_path"]}
            )
            if not relation_results:
                return "Dataset not found", 500
            dataset_id = [neo4j_obj_2_json(x) for x in relation_results][0]["start_node"]["id"]

            # Create File to TrashFile relation
            self.node_method.add_relation_between_nodes("deleted", file_node["id"], result["id"])
            # Create Dataset to file relation
            self.node_method.add_relation_between_nodes("own", dataset_id, result["id"])
        except Exception as e:
            return str(e), 403
        return result, 200


