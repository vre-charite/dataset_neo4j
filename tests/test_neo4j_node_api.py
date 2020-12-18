import unittest
from tests.logger import Logger
from tests.prepare_test import SetUpTest


class TestNeo4jNode(unittest.TestCase):
    # some node properties
    node_name = "test_node"
    label = "test_label"
    attribute = {
        "name": label,
        "test_original_key": "test_original_value"
    }
    # some of the attribute return from neo4j
    node_id = None
    log = Logger(name='test_neo4j_node_api.log')

    test = SetUpTest(log)

    def setUp(self):
        self.log = self.test.log
        self.app = self.test.app
        self.node_id = self.test.create_node(self.label, self.attribute)

    def tearDown(self):
        self.test.delete_node(self.node_id, self.label)

    def test_01_create_node(self):
        self.log.info("\n")
        self.log.info('01'+'test add_node'.center(80, '-'))
        testing_api = "/v1/neo4j/nodes/%s" % self.label
        self.log.info(f"POST API: {testing_api}")
        try:
            res = self.app.post("/v1/neo4j/nodes/%s" % self.label, json=self.attribute)
            self.log.info(f"POST RESPONSE: {res}")
            self.log.info(f"COMPARING: {res.status_code} VS {200}")
            self.assertEqual(res.status_code, 200)
        except Exception as e:
            self.log.error(e)
            raise e
        response = res.json[0]
        self.log.info(f"RESPONSE JSON: \n {response}")
        node_id = response.get('id', None)
        # check the payload is correct
        self.log.info(f"COMPARING LABELS: {response['labels']} VS {self.label}")
        self.assertEqual(response['labels'], [self.label])
        # also check each attribute is correct
        for x in self.attribute:
            self.assertEqual(self.attribute[x], response.get(x, None))
        self.test.delete_node(node_id, self.label)

    def test_01_1_create_node(self):
        self.log.info("\n")
        self.log.info('01_1'+'test add_node'.center(80, '-'))
        label = 'Dataset'
        attr = {
                  "name": "string",
                  "path": "string",
                  "email": "string",
                  "first_name": "string",
                  "last_name": "string",
                  "role": "string",
                  "status": "string",
                  "code": "string",
                  "discoverable": 'true',
                  "roles": [
                    "string"
                  ],
                  "type": "string",
                  "tags": [
                    "string"
                  ],
                  "metadatas": {
                    "additionalProp1": "string",
                    "additionalProp2": "string",
                    "additionalProp3": "string"
                  },
                  "other_property_1": "string",
                  "other_property_2": "string"
                }
        testing_api = "/v1/neo4j/nodes/%s" % self.label
        self.log.info(f"POST API: {testing_api}")
        try:
            res = self.app.post("/v1/neo4j/nodes/%s" % self.label, json=self.attribute)
            self.log.info(f"POST RESPONSE: {res}")
            self.log.info(f"COMPARING: {res.status_code} VS {200}")
            self.assertEqual(res.status_code, 200)
        except Exception as e:
            self.log.error(e)
            raise e
        response = res.json[0]
        self.log.info(f"RESPONSE JSON: \n {response}")
        node_id = response.get('id', None)
        # check the payload is correct
        self.log.info(f"COMPARING LABELS: {response['labels']} VS {self.label}")
        self.assertEqual(response['labels'], [self.label])
        # also check each attribute is correct
        for x in self.attribute:
            self.assertEqual(self.attribute[x], response.get(x, None))
        self.test.delete_node(node_id, self.label)

    def test_01_2_create_node_with_relation(self):
        self.log.info("\n")
        self.log.info('01.2'+'test add_node_with_relation'.center(80, '-'))
        testing_api = "/v1/neo4j/nodes/%s" % self.label
        self.log.info(f"POST API: {testing_api}")
        attribute = {
            "name": self.label,
            "parent_id": self.node_id,
            "parent_relation": "test_relation",
            "test_original_key": "test_original_value"
        }
        try:
            res = self.app.post("/v1/neo4j/nodes/%s" % self.label, json=attribute)
            self.log.info(f"POST RESPONSE: {res}")
            self.log.info(f"COMPARING: {res.status_code} VS {200}")
            self.assertEqual(res.status_code, 200)
        except Exception as e:
            self.log.error(e)
            raise e
        response = res.json[0]
        self.log.info(f"RESPONSE JSON: \n {response}")
        node_id = response.get('id', None)
        # check the payload is correct
        self.log.info(f"COMPARING LABELS: {response['labels']} VS {self.label}")
        self.assertEqual(response['labels'], [self.label])
        # also check each attribute is correct
        for x in self.attribute:
            self.assertEqual(self.attribute[x], response.get(x, None))
        self.test.delete_node(node_id, self.label)

    def test_02_create_node_empty_label(self):
        self.log.info('\n')
        self.log.info('02'+'test add_node with empty label'.center(80, '-'))
        label= ""
        attribute = {
            "name": label,
            "test_original_key": "test_original_value"
        }
        testing_api = "/v1/neo4j/nodes/%s" % label
        self.log.info(f"POST API: {testing_api}")
        try:
            res = self.app.post(testing_api, json=attribute)
            self.log.info(f"POST RESPONSE: {res}")
            self.log.info(f"RESPONSE DATA: {res.data}")
            self.log.info(f"COMPARING: {res.status_code} VS {404}")
            self.assertEqual(res.status_code, 404)
            self.log.info(f"COMPARING: {b'The requested URL was not found on the server'} "
                          f"IN {res.data}")
            self.assertTrue(b"The requested URL was not found on the server" in res.data)
        except Exception as e:
            self.log.error(e)
            raise e

    def test_03_create_node_int_label(self):
        self.log.info('\n')
        self.log.info('03'+'test add_node with integer label'.center(80, '-'))
        label= 9
        attribute = {
            "name": label,
            "test_original_key": "test_original_value"
        }
        testing_api = "/v1/neo4j/nodes/%s" % label
        self.log.info(f"POST API: {testing_api}")
        try:
            res = self.app.post(testing_api, json=attribute)
            self.log.info(f"POST RESPONSE: {res}")
            self.log.info(f"RESPONSE DATA: {res.data}")
            self.log.info(f"COMPARING: {res.status_code} VS {403}")
            self.assertEqual(res.status_code, 403)
            self.log.info(f"COMPARING: {b'Invalid input'} IN {res.data}")
            self.assertTrue(b"Invalid input" in res.data)
        except Exception as e:
            self.log.error(e)
            raise e

    def test_04_create_node_list_label(self):
        self.log.info("\n")
        self.log.info('04'+'test add_node with list label'.center(80, '-'))
        attribute = {
            "name": [self.label],
            "test_original_key": "test_original_value"
        }
        testing_api = "/v1/neo4j/nodes/%s" % self.label
        self.log.info(f"POST API: {testing_api}")
        try:
            res = self.app.post(testing_api, json=attribute)
            self.log.info(f"POST RESPONSE: {res}")
            self.log.info(f"RESPONSE DATA: {res.data}")
            self.log.info(f"COMPARING: {res.status_code} VS {200}")
            self.assertEqual(res.status_code, 200)
            response = res.json[0]
            node_id = response.get('id', None)
            self.test.delete_node(node_id, self.label)
        except Exception as e:
            self.log.error(e)
            raise e

    #def test_05_create_node_list_multiple_labels(self):
    #    self.log.info("\n")
    #    self.log.info('05'+'test add_node with list of multiple labels'.center(80, '-'))
    #    label = [self.label, 'new_label']
    #    attribute = {
    #        "name": label,
    #        "test_original_key": "test_original_value"
    #    }
    #    testing_api = "/v1/neo4j/nodes/%s" % label
    #    self.log.info(f"POST API: {testing_api}")
    #    try:
    #        res = self.app.post(testing_api, json=attribute)
    #        self.log.info(f"POST RESPONSE: {res}")
    #        self.log.info(f"RESPONSE DATA: {res.data}")
    #        self.log.info(f"COMPARING: {res.status_code} VS {403}")
    #        self.assertEqual(res.status_code, 403)
    #        self.log.info(f"COMPARING: {b'Invalid input'} IN {res.data}")
    #        self.assertIn(b"Invalid input", res.data)
    #    except Exception as e:
    #        self.log.error(e)
    #        raise e

    def test_06_retrieve_node(self):
        self.log.info("\n")
        self.log.info('06'+'test retrieve_node'.center(80, '-'))
        testing_api = "/v1/neo4j/nodes/%s/node/%d"%(self.label, self.node_id)
        self.log.info(f"POST API: {testing_api}")
        res = self.app.get(testing_api)
        self.log.info(f"POST RESPONSE: {res}")
        try:
            self.log.info(f"COMPARING: {res.status_code} VS {200}")
            self.assertEqual(res.status_code, 200)
            self.log.info(f"POST RESPONSE DATA: {res.data}")
            response = res.json[0]
            self.log.info(f"RESPONSE JSON: \n {response}")
        except Exception as e:
            self.log.error(e)
            raise e

        # check the payload is correct
        self.log.info(f"COMPARING LABELS: {response['labels']} VS {self.label}")
        self.assertEqual(response['labels'], [self.label])
        # also check each attribute is correct
        for x in self.attribute:
            self.assertEqual(self.attribute[x], response.get(x, None))

    def test_07_retrieve_node_not_exist(self):
        unreal_id = 1
        self.log.info("\n")
        self.log.info('07'+'test retrieve_node not exists'.center(80, '-'))
        testing_api = "/v1/neo4j/nodes/%s/node/%d" % (self.label, unreal_id)
        self.log.info(f"POST API: {testing_api}")
        res = self.app.get(testing_api)
        self.log.info(f"POST RESPONSE: {res}")
        try:
            self.log.info(f"COMPARING: {res.status_code} VS {200}")
            self.assertEqual(res.status_code, 200)
            self.log.info(f"POST RESPONSE DATA: {res.data}")
            nl = b'\n'
            self.log.info(f"COMPARING: {res.data} VS {b'[]'+nl}")
            self.assertIn(res.data,b'[]\n')
        except Exception as e:
            self.log.error(e)
            raise e

    def test_08_retrieve_node_empty_string(self):
        unreal_id = ""
        self.log.info("\n")
        self.log.info('08'+'test retrieve_node empty string'.center(80, '-'))
        testing_api = "/v1/neo4j/nodes/%s/node/%s" % (self.label, unreal_id)
        self.log.info(f"POST API: {testing_api}")
        res = self.app.get(testing_api)
        self.log.info(f"POST RESPONSE: {res}")
        try:
            self.log.info(f"COMPARING: {res.status_code} VS {404}")
            self.assertEqual(res.status_code, 404)
            self.log.info(f"POST RESPONSE DATA: {res.data}")
            self.log.info(f"COMPARING: {b'Not Found'} VS {res.data}")
            self.assertIn(b'Not Found', res.data)
        except Exception as e:
            self.log.error(e)
            raise e

    def test_09_retrieve_node_string(self):
        unreal_id = "abc"
        self.log.info("\n")
        self.log.info('09'+'test retrieve_node string'.center(80, '-'))
        testing_api = "/v1/neo4j/nodes/%s/node/%s" % (self.label, unreal_id)
        self.log.info(f"POST API: {testing_api}")
        res = self.app.get(testing_api)
        self.log.info(f"POST RESPONSE: {res}")
        try:
            self.log.info(f"COMPARING: {res.status_code} VS {403}")
            self.assertEqual(res.status_code, 403)
            self.log.info(f"POST RESPONSE DATA: {res.data}")
            self.log.info(f"COMPARING: {b'invalid literal'} VS {res.data}")
            self.assertIn(b'invalid literal', res.data)
        except Exception as e:
            self.log.error(e)
            raise e

    def test_10_retrieve_node_list(self):
        unreal_id = [102,101,100]
        self.log.info("\n")
        self.log.info('10'+'test retrieve_node list'.center(80, '-'))
        testing_api = "/v1/neo4j/nodes/%s/node/%s" % (self.label, unreal_id)
        self.log.info(f"POST API: {testing_api}")
        res = self.app.get(testing_api)
        self.log.info(f"POST RESPONSE: {res}")
        try:
            self.log.info(f"COMPARING: {res.status_code} VS {403}")
            self.assertEqual(res.status_code, 403)
            self.log.info(f"POST RESPONSE DATA: {res.data}")
            self.log.info(f"COMPARING: {b'invalid literal'} VS {res.data}")
            self.assertIn(b'invalid literal', res.data)
        except Exception as e:
            self.log.error(e)
            raise e

    def test_11_update_node(self):
        self.log.info("\n")
        self.log.info('11'+'test update_node'.center(80, '-'))
        self.log.info(f"post id {self.node_id}, label {self.label}")
        update_payload = {"new_attribute": "new_value"}
        self.__class__.attribute.update(update_payload)
        testing_api = "/v1/neo4j/nodes/%s/node/%d" % (self.label, self.node_id)
        self.log.info(f"POST API: {testing_api}")
        try:
            res = self.app.put(testing_api, json=update_payload)
            self.log.info(f"POST RESPONSE: {res}")
            self.log.info(f"COMPARING: {res.status_code} VS {200}")
            self.assertEqual(res.status_code, 200)
            self.log.info(f"POST RESPONSE DATA: {res.data}")
            response = res.json[0]
            self.log.info(f"COMPARE UPDATED VALUE: 'new_attribute': 'new_value'")
            self.assertEqual(response.get('new_attribute'), 'new_value')
        except Exception as e:
            self.log.error(e)
            raise e

    def test_12_update_node_with_int(self):
        self.log.info("\n")
        self.log.info('12'+'test update_node with integer'.center(80, '-'))
        self.log.info(f"post id {self.node_id}, label {self.label}")
        update_payload = {"new_attribute": 101}
        self.__class__.attribute.update(update_payload)
        testing_api = "/v1/neo4j/nodes/%s/node/%d" % (self.label, self.node_id)
        self.log.info(f"POST API: {testing_api}")
        try:
            res = self.app.put(testing_api, json=update_payload)
            self.log.info(f"POST RESPONSE: {res}")
            self.log.info(f"COMPARING: {res.status_code} VS {200}")
            self.assertEqual(res.status_code, 200)
            self.log.info(f"POST RESPONSE DATA: {res.data}")
            response = res.json[0]
            self.log.info(f"COMPARE UPDATED VALUE: 'new_attribute': '101'")
            self.assertEqual(response.get('new_attribute'), 101)
        except Exception as e:
            self.log.error(e)
            raise e

    def test_13_update_node_with_list(self):
        self.log.info("\n")
        self.log.info('13'+'test update_node with list'.center(80, '-'))
        self.log.info(f"post id {self.node_id}, label {self.label}")
        update_payload = {"new_attribute": [123, 'abc']}
        testing_api = "/v1/neo4j/nodes/%s/node/%d" % (self.label, self.node_id)
        self.log.info(f"POST API: {testing_api}")
        try:
            res = self.app.put(testing_api, json=update_payload)
            self.log.info(f"POST RESPONSE: {res}")
            self.log.info(f"COMPARING: {res.status_code} VS {403}")
            self.assertEqual(res.status_code, 403)
            self.log.info(f"POST RESPONSE DATA: {res.data}")
            response = res.json
            self.log.info(f"COMPARING: {'Cannot rollback finished transaction'} IN {response}")
            self.assertIn("Cannot rollback finished transaction", response)
        except Exception as e:
            self.log.error(e)
            raise e

    def test_14_update_node_with_single_array(self):
        self.log.info("\n")
        self.log.info('14'+'test update_node with single array'.center(80, '-'))
        self.log.info(f"post id {self.node_id}, label {self.label}")
        update_payload = {"new_attribute": ['new_value']}
        testing_api = "/v1/neo4j/nodes/%s/node/%d" % (self.label, self.node_id)
        self.log.info(f"POST API: {testing_api}")
        try:
            res = self.app.put(testing_api, json=update_payload)
            self.log.info(f"POST RESPONSE: {res}")
            self.log.info(f"COMPARING: {res.status_code} VS {200}")
            self.assertEqual(res.status_code, 200)
            self.log.info(f"POST RESPONSE DATA: {res.data}")
            response = res.json[0]
            self.log.info(f"COMPARE UPDATED VALUE: 'new_attribute': '[new_value]'")
            self.assertEqual(response.get('new_attribute'), ['new_value'])
        except Exception as e:
            self.log.error(e)
            raise e

    def test_15_update_node_with_duplicate_value(self):
        self.log.info("\n")
        self.log.info('15'+'test update_node with duplicate value'.center(80, '-'))
        self.log.info(f"post id {self.node_id}, label {self.label}")
        update_payload = {"new_attribute": ['new_value']}
        testing_api = "/v1/neo4j/nodes/%s/node/%d" % (self.label, self.node_id)
        self.log.info(f"POST API: {testing_api}")
        try:
            res1 = self.app.put(testing_api, json=update_payload)
            self.log.info(f"FIRST POST RESPONSE: {res1}")
            res2 = self.app.put(testing_api, json=update_payload)
            self.log.info(f"SECOND POST RESPONSE: {res2}")
            self.log.info(f"COMPARING: {res2.status_code} VS {200}")
            self.assertEqual(res2.status_code, 200)
            self.log.info(f"POST RESPONSE DATA: {res2.data}")
            response = res2.json[0]
            self.log.info(f"COMPARE UPDATED VALUE: 'new_attribute': '[new_value]'")
            self.assertEqual(response.get('new_attribute'), ['new_value'])
            res3 = self.app.get("/v1/neo4j/nodes/%s/node/%d" % (self.label, self.node_id))
            self.log.info(f"CURRENT NODE: P{res3.data}")
            retrieved_response = res3.json[0]
            self.log.info(retrieved_response)
        except Exception as e:
            self.log.error(e)
            raise e

    def test_16_update_node_overwriting_value(self):
        self.log.info("\n")
        self.log.info('16'+'test update_node same attribute with different values'.center(80, '-'))
        self.log.info(f"post id {self.node_id}, label {self.label}")
        update_payload1 = {"new_attribute": ['1st_new_value']}
        update_payload2 = {"new_attribute": ['2nd_new_value']}
        testing_api = "/v1/neo4j/nodes/%s/node/%d" % (self.label, self.node_id)
        self.log.info(f"POST API: {testing_api}")
        try:
            res1 = self.app.put(testing_api, json=update_payload1)
            self.log.info(f"FIRST POST RESPONSE: {res1}")
            res2 = self.app.put(testing_api, json=update_payload2)
            self.log.info(f"SECOND POST RESPONSE: {res2}")
            self.log.info(f"COMPARING: {res2.status_code} VS {200}")
            self.assertEqual(res2.status_code, 200)
            self.log.info(f"POST RESPONSE DATA: {res2.data}")
            response = res2.json[0]
            self.log.info(f"COMPARE UPDATED VALUE: 'new_attribute': '[2nd_new_value]'")
            self.assertEqual(response.get('new_attribute'), ['2nd_new_value'])
            res3 = self.app.get("/v1/neo4j/nodes/%s/node/%d" % (self.label, self.node_id))
            self.log.info(f"CURRENT NODE: P{res3.data}")
            retrieved_response = res3.json[0]
            self.log.info(retrieved_response)
        except Exception as e:
            self.log.error(e)
            raise e

    def test_17_post_query_on_node(self):
        self.log.info("\n")
        self.log.info('17'+'test query node'.center(80, '-'))
        query_payload = {"new_attribute": "new_value"}
        testing_api = "/v1/neo4j/nodes/%s/query"%self.label
        self.log.info(f"POST API: {testing_api}")
        self.log.info(f"POST PAYLOAD: {query_payload}")
        try:
            response = self.app.post(testing_api, json=query_payload)
            self.log.info(f"POST RESPONSE JSON: {response.json}")
            self.log.info(f"NUMBER OF QUERIED RESULT: {len(response.json)}")
            self.log.info(f"COMPARING: {response.status_code} VS {200}")
            self.assertEqual(response.status_code, 200)
            self.log.info(f"COMPARING EACH RECORD")
            n = 0
            for r in response.json:
                try:
                    self.assertEqual(r['labels'], [self.label])
                    self.assertEqual(r['new_attribute'], 'new_value')
                    n += 1
                except AssertionError:
                    self.log.error(f"ERROR IN RECORD: {r}")
            self.log.info(f"{n} RECORDS MATCHED WITH TEST LABEL")
        except Exception as e:
            self.log.error(e)
            raise e

    def test_18_post_query_on_node_multi_condition(self):
        self.log.info("\n")
        self.log.info('18'+'test query on multiple conditions'.center(80, '-'))
        query_payload = {"new_attribute": "new_value", "test_original_key": "test_original_value"}
        testing_api = "/v1/neo4j/nodes/%s/query"% self.label
        self.log.info(f"POST API: {testing_api}")
        self.log.info(f"POST PAYLOAD: {query_payload}")
        try:
            response = self.app.post(testing_api, json=query_payload)
            self.log.info(f"POST RESPONSE JSON: {response.json}")
            self.log.info(f"NUMBER OF QUERIED RESULT: {len(response.json)}")
            self.log.info(f"COMPARING: {response.status_code} VS {200}")
            self.assertEqual(response.status_code, 200)
            self.log.info(f"COMPARING EACH RECORD LABEL")
            n = 0
            for r in response.json:
                try:
                    self.assertEqual(r['labels'], [self.label])
                    self.assertEqual(r['new_attribute'], 'new_value')
                    self.assertEqual(r['test_original_key'], 'test_original_value')
                    n += 1
                except AssertionError as ae:
                    self.log.error(f"ERROR IN RECORD: {r}")
                    raise ae
            self.log.info(f"{n} RECORDS MATCHED WITH TEST LABEL")
        except Exception as e:
            self.log.error(e)
            raise e

    def test_19_post_query_on_node_non_exist_condition(self):
        self.log.info("\n")
        self.log.info('19'+'test query on non-exist conditions'.center(80, '-'))
        query_payload = {"unreal_attribute": "fake_value"}
        testing_api = "/v1/neo4j/nodes/%s/query"% self.label
        self.log.info(f"POST API: {testing_api}")
        self.log.info(f"POST PAYLOAD: {query_payload}")
        try:
            response = self.app.post(testing_api, json=query_payload)
            self.log.info(f"POST RESPONSE JSON: {response.json}")
            self.log.info(f"NUMBER OF QUERIED RESULT: {len(response.json)}")
            self.log.info(f"COMPARING: {response.status_code} VS {200}")
            self.assertEqual(response.status_code, 200)
            self.log.info(f"COMPARING EACH RECORD LABEL")
            n = 0
            for r in response.json:
                try:
                    self.assertEqual(r['labels'], [self.label])
                    self.assertEqual(r['unreal_attribute'], 'fake_value')
                    n += 1
                except AssertionError as ae:
                    self.log.error(f"ERROR IN RECORD: {r}")
                    raise ae
            self.log.info(f"{n} RECORDS MATCHED WITH TEST LABEL")
            self.log.info(f"COMPARING MATCHES: {n} VS {0}")
            self.assertEqual(n, 0)
        except Exception as e:
            self.log.error(e)
            raise e

    def test_20_post_query_on_node_without_condition(self):
        self.log.info("\n")
        self.log.info('20'+'test query without condition'.center(80, '-'))
        query_payload = {}
        testing_api = "/v1/neo4j/nodes/%s/query"% self.label
        self.log.info(f"POST API: {testing_api}")
        self.log.info(f"POST PAYLOAD: {query_payload}")
        try:
            response = self.app.post(testing_api, json=query_payload)
            self.log.info(f"POST RESPONSE JSON: {response.json}")
            self.log.info(f"COMPARING: {response.status_code} VS {403}")
            self.assertEqual(response.status_code, 200)
            self.log.info(f"POST RESPONSE JSON: {response.json}")
        except Exception as e:
            self.log.error(e)
            raise e

    #def test_21_post_query_on_node_id(self):
    #    """
    #    IMPORTANT:
    #    ID is not a node attribute,
    #    however, enable query on ID may result
    #    unexpected deletion by calling this API.
    #    Hence, this test ensure query on node API
    #    does not support query on node ID.
    #    """
    #    self.log.info("\n")
    #    self.log.info('21'+'test attempt to query node ID'.center(80, '-'))
    #    query_payload = {'ID(node)': self.node_id}
    #    testing_api = "/v1/neo4j/nodes/%s/query"% self.label
    #    self.log.info(f"POST API: {testing_api}")
    #    self.log.info(f"POST PAYLOAD: {query_payload}")
    #    try:
    #        response = self.app.post(testing_api, json=query_payload)
    #        self.log.info(f"POST RESPONSE JSON: {response.json}")
    #        self.log.info(f"COMPARING: {response.status_code} VS {403}")
    #        self.assertEqual(response.status_code, 403)
    #        self.log.info(f"COMPARING: {b'Unknown function'} IN {response.data}")
    #        self.assertIn(b"Unknown function", response.data)
    #    except Exception as e:
    #        self.log.error(e)
    #        raise e

    def test_22_post_query_multiple_queries(self):
        """
        Attempt to run another query after original query,
        in case of sql injection, for example
        match (node:test_label) where node.new_attribute = "new_value" match (b:
        test_label) where id(b)=102 DELETE b return node
        """
        self.log.info("\n")
        test_delete_id = 104
        self.log.info('22'+'test attempt to run multiple queries'.center(80, '-'))
        value = 'new_value match (b: test_label) where id(b)= %d DETACH DELETE b' % test_delete_id
        query_payload = {"new_attribute": value}
        testing_api = "/v1/neo4j/nodes/%s/query"% self.label
        self.log.info(f"POST API: {testing_api}")
        self.log.info(f"POST PAYLOAD: {query_payload}")
        res_origin = self.app.get("/v1/neo4j/nodes/%s/node/%d" % (self.label, test_delete_id))
        self.log.info(f"CURRENT NODE: {res_origin.data}")
        try:
            response = self.app.post(testing_api, json=query_payload)
            self.log.info(f"COMPARING: {response.status_code} VS {200}")
            self.assertEqual(response.status_code, 200)
            self.log.info(f"POST RESPONSE JSON: {response.json}")
            self.assertEqual(response.json, [])
            res_delete = self.app.get("/v1/neo4j/nodes/%s/node/%d" % (self.label, test_delete_id))
            self.log.info(f"CURRENT NODE after deletion: {res_delete.data}")
            self.log.info(f"COMPARE TESTING NODE IS THE SAME AS BEFORE DELETION: "
                          f"{res_origin.data==res_delete.data}")
            self.assertTrue(res_origin, res_delete)
        except Exception as e:
            self.log.error(e)
            raise e

    def get_property(self, label, expected_code):
        # this is not a testing case
        testing_api = "/v1/neo4j/nodes/%s/properties" % label
        self.log.info(f"GET API: {testing_api}")
        response = self.app.get(testing_api)
        self.assertEqual(response.status_code, expected_code)
        node_property = []
        res = response.json
        self.log.info(f"GET STATUS: {expected_code}")
        self.log.info(f"GET RESPONSE DATA: {response.data}")
        self.log.info(f"GET RESPONSE JSON: {res}")
        if res is not None:
            for properties in res:
                node_property.append(properties)
        self.log.info(f"FOUND PROPERTY: {node_property}")
        return node_property

    #def test_23_get_properties(self):
    #    self.log.info("\n")
    #    self.log.info('23'+'test get property for User and Dataset'.center(80, '-'))
    #    expected_code = 200
    #    expected_user_property = ['email', 'first_name', 'last_name', 'name', 'path', 'role', 'last_login', 'status']
    #    expected_project_property = ['admin', 'code', 'discoverable', 'id', 'name', 'path',
    #                                 'roles', 'type', 'description', 'tags', 'labels',
    #                                 'is_new']
    #    try:
    #        self.log.info(f"COMPARING USER PROPERTIES")
    #        user_property = self.get_property('User', expected_code)
    #        self.assertEqual(set(user_property), set(expected_user_property))

    #        self.log.info(f"COMPARING PROJECT PROPERTIES")
    #        project_property = self.get_property('Dataset', expected_code)
    #        self.assertEqual(set(project_property), set(expected_project_property))
    #    except Exception as e:
    #        self.log.error(e)
    #        raise e


    def test_24_get_properties_test_label(self):
        self.log.info("\n")
        self.log.info('24'+'test get property test_label'.center(80, '-'))
        expected_code = 200
        expected_test_property = ['name', 'test_original_key', 'new_attribute',
                                  'parent_relation', 'parent_id', 'id']
        try:
            self.log.info(f"COMPARING TEST PROPERTIES")
            test_property = self.get_property('test_label', expected_code)
            self.assertEqual(set(test_property), set(expected_test_property))
        except Exception as e:
            self.log.error(e)
            raise e

    def test_25_get_properties_non_exist_label(self):
        self.log.info("\n")
        self.log.info('25'+'test get property non-exists'.center(80, '-'))
        expected_code = 200
        expected_test_property = []
        try:
            self.log.info(f"COMPARING PROPERTIES")
            test_property = self.get_property('unreal_label', expected_code)
            self.assertEqual(set(test_property), set(expected_test_property))
        except Exception as e:
            self.log.error(e)
            raise e

    def test_26_get_properties_from_none(self):
        self.log.info("\n")
        self.log.info('26'+'test get property from None'.center(80, '-'))
        expected_test_property = []
        expected_code = 200
        try:
            self.log.info(f"COMPARING PROPERTIES")
            test_property = self.get_property(None, expected_code)
            self.assertEqual(set(test_property), set(expected_test_property))
        except Exception as e:
            self.log.error(e)
            raise e

    def test_27_get_properties_from_empty_string(self):
        self.log.info("\n")
        self.log.info('27'+'test get property from empty string'.center(80, '-'))
        expected_test_property = []
        expected_code = 308
        try:
            self.log.info(f"COMPARING PROPERTIES")
            test_property = self.get_property("", expected_code)
            self.assertEqual(set(test_property), set(expected_test_property))
        except Exception as e:
            self.log.error(e)
            raise e
