import json
import unittest
import requests
import time
import uuid

class TestDataset(unittest.TestCase):

    base_url = "http://0.0.0.0:5062/v1"

    # some node properties
    node_name = "test_node"
    label = "test_label"
    attribute = {
        "name": label,
        "test_original_key": "test_original_value"
    }

    # some of the attribute return from neo4j
    node_id = None

    def test_01_create_node(self):
        res = requests.post(self.base_url+"/neo4j/nodes/%s"%(self.label), json=self.attribute)
        self.assertEqual(res.status_code, 200)
        res = json.loads(res.text)[0]

        self.__class__.node_id = res.get('id', None)

        # check the payload is correct
        self.assertEqual(res['labels'], [self.label])
        # also check each attribute is correct
        for x in self.attribute:
            self.assertEqual(self.attribute[x], res.get(x, None))

    def test_02_retrieve_node(self):
        res = requests.get(self.base_url+"/neo4j/nodes/%s/node/%d"%(self.label, self.node_id))
        self.assertEqual(res.status_code, 200)
        res = json.loads(res.text)[0]

        # check the payload is correct
        self.assertEqual(res['labels'], [self.label])
        # also check each attribute is correct
        for x in self.attribute:
            self.assertEqual(self.attribute[x], res.get(x, None))

    def test_03_update_node(self):
        update_payload = {"new_attribute": "new_value"}
        self.__class__.attribute.update(update_payload)

        res = requests.put(self.base_url+"/neo4j/nodes/%s/node/%d"%(self.label, self.node_id), json=update_payload)
        self.assertEqual(res.status_code, 200)
        res = json.loads(res.text)[0]

        # also check each attribute is correct
        for x in self.attribute:
            self.assertEqual(self.attribute[x], res.get(x, None))


    def test_04_retrieve_node(self):
        res = requests.get(self.base_url+"/neo4j/nodes/%s/node/%d"%(self.label, self.node_id))
        self.assertEqual(res.status_code, 200)
        res = json.loads(res.text)[0]

        print(res)

        # check the payload is correct
        self.assertEqual(res['labels'], [self.label])
        # also check each attribute is correct
        for x in self.attribute:
            self.assertEqual(self.attribute[x], res.get(x, None))


    def test_05_post_query_on_node(self):
        query_payload = {"new_attribute": "new_value"}
        res = requests.post(self.base_url+"/neo4j/nodes/%s/query"%(self.label), json=query_payload)
        self.assertEqual(res.status_code, 200)
        res = json.loads(res.text)[0]

        # check the payload is correct
        self.assertEqual(res['labels'], [self.label])
        # also check each attribute is correct
        for x in self.attribute:
            self.assertEqual(self.attribute[x], res.get(x, None))


    def test_06_get_properties(self):
        res = requests.get(self.base_url+"/neo4j/nodes/%s/properties"%(self.label))
        self.assertEqual(res.status_code, 200)
        res = json.loads(res.text)

        print(res)

        # all the answer to array
        for x in self.attribute:
            self.assertEqual([self.attribute[x]], res.get(x, None))



if __name__ == '__main__':
    unittest.main()
