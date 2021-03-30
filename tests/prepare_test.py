from neo4j_api.neo4j_base import Neo4jNode


from app import create_app

class SetUpTest:

    def __init__(self, log):
        self.log = log
        self.app = self.create_test_client()

    def create_test_client(self):
        app = create_app()
        app.config['TESTING'] = True
        app.config['DEBUG'] = True
        test_client = app.test_client(self)
        return test_client

    def create_node(self, label, attribute):
        res = self.app.post("/v1/neo4j/nodes/%s" % label, json=attribute)
        self.log.info(f"{res}")
        response = res.json[0]
        # Retrieve current node information by ID
        self.log.info(f"Create node response {response}")
        res_creation = self.app.get("/v1/neo4j/nodes/%s/node/%d" % (label, response.get('id', None)))
        assert res_creation.status_code == 200
        self.log.info(f"TESTING NODE {label} CREATED WITH ATTRIBUTES {attribute}")
        return response.get('id', None)


    def delete_node(self, node_id, label):
        '''
        self.log.info("Delete the testing node".center(50, '='))
        node_method = Neo4jNode()
        # Call delete_node function to delete node recursively by ID
        node_method.delete_node(node_id)
        self.log.warning(f"DELETING TESTING NODE: {node_id}")
        # Retrieve current node information again to make sure it had been deleted
        response = self.app.get("/v1/neo4j/nodes/%s/node/%d" % (label, node_id))
        self.log.info(f'The testing node {node_id} has been deleted, record: {response.data}"')
        '''
        self.log.warning(f"DELETING TESTING NODE: {node_id}")
        res = self.app.delete("/v1/neo4j/nodes/%s/node/%d" % (label, node_id))
        self.log.info(f"{res}")
        self.log.info(f"COMPARING: {res.status_code} VS {200}")
        assert res.status_code == 200
        response = self.app.get("/v1/neo4j/nodes/%s/node/%d" % (label, node_id))
        content = response.data
        assert b'[]' in content 
        self.log.info(f'The testing node {node_id} has been deleted, record: {content}"')
