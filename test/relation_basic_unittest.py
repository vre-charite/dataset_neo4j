import json
import unittest
import requests
import time
import uuid

class TestDataset(unittest.TestCase):

    base_url = "http://0.0.0.0:5062/v1"

    # some node properties
    node_label = "test_label"
    relation_label = "TEST_RELATION"
    start_node = {
        "name": "start_node",
        "test_original_key": "test_original_start"
    }

    end_node = {
        "name": "end_node",
        "test_original_key": "test_original_end"
    }


    def test_01_create_node(self):
        res = requests.post(self.base_url+"/neo4j/nodes/%s"%(self.node_label), json=self.start_node)
        self.assertEqual(res.status_code, 200)
        res = json.loads(res.text)[0]

        self.__class__.start_node = res

        res = requests.post(self.base_url+"/neo4j/nodes/%s"%(self.node_label), json=self.end_node)
        self.assertEqual(res.status_code, 200)
        res = json.loads(res.text)[0]

        self.__class__.end_node = res

    def test_02_create_relation(self):
        payload = {
            "start_id": self.start_node['id'],
            "end_id": self.end_node['id'],
        }

        res = requests.post(self.base_url+"/neo4j/relations/%s"%(self.relation_label), json=payload)
        self.assertEqual(res.status_code, 200)
        # print(res.text)

    def test_03_get_relation(self):
        params = {
            "label":self.relation_label,
            "start_id": self.start_node['id'],
            "end_id": self.end_node['id']
        }

        res = requests.get(self.base_url+"/neo4j/relations", params=params)
        self.assertEqual(res.status_code, 200)

        res = json.loads(res.text)[0]

        # check relationship 
        self.assertEqual(res['r']['type'], self.relation_label)

        # check node in nested child
        path = res['p']
        start_node = path.get('start_node', None)
        self.assertEqual(start_node['id'], self.start_node['id'])

        end_node = start_node['children']['end_node']
        self.assertEqual(end_node['id'], self.end_node['id'])

    def test_04_update_relationship(self):
        payload = {
            "new_label": "new_label",
            "start_id": self.start_node['id'],
            "end_id": self.end_node['id'],
        }

        res = requests.put(self.base_url+"/neo4j/relations/%s"%(self.relation_label), json=payload)
        self.assertEqual(res.status_code, 200)
        self.__class__.relation_label = "new_label"

        # check if the label updated
        params = {
            "start_id": self.start_node['id'],
            "end_id": self.end_node['id']
        }

        res = requests.get(self.base_url+"/neo4j/relations", params=params)
        self.assertEqual(res.status_code, 200)

        res = json.loads(res.text)[0]

        # print(res)

        # check relationship 
        self.assertEqual(res['r']['type'], "new_label")

    def test_05_get_node_by_relation(self):
        # check the end node
        res = requests.get(self.base_url+"/neo4j/relations/%s/node/%d"%(self.relation_label, self.start_node['id']))
        self.assertEqual(res.status_code, 200)
        res = json.loads(res.text)[0]
        self.assertEqual(res['id'], self.end_node['id'])

        # check the start node
        res = requests.get(self.base_url+"/neo4j/relations/%s/node/%d"%(self.relation_label, self.end_node['id']),
            params={"start": False})
        self.assertEqual(res.status_code, 200)
        res = json.loads(res.text)[0]
        self.assertEqual(res['id'], self.start_node['id'])

    def test_06_remove_relation(self):
        payload = {
            "start_id": self.start_node['id'],
            "end_id": self.end_node['id'],
        }

        res = requests.delete(self.base_url+"/neo4j/relations", params=payload)
        self.assertEqual(res.status_code, 200)

        params = {
            "label":self.relation_label,
            "start_id": self.start_node['id'],
            "end_id": self.end_node['id']
        }

        res = requests.get(self.base_url+"/neo4j/relations", params=params)
        self.assertEqual(res.status_code, 200)

        res = json.loads(res.text)
        self.assertEqual(res, [])

    


if __name__ == '__main__':
    unittest.main()
