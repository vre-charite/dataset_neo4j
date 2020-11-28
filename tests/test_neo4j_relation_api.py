import unittest
from tests.logger import Logger
from tests.prepare_test import SetUpTest

class TestNeo4jRelation(unittest.TestCase):
    # some node properties
    node_label = "test_label"
    relation_label = "TEST_RELATION"
    start_node_attribute = {
        "name": "start_node",
        "test_original_key": "test_original_start"
    }
    end_node_attribute = {
        "name": "end_node",
        "test_original_key": "test_original_end"
    }
    start_node_id = None
    end_node_id = None
    log = Logger(name='test_neo4j_relation_api.log')
    test = SetUpTest(log)

    @classmethod
    def setUpClass(cls):
        cls.log = cls.test.log
        cls.app = cls.test.app
        cls.start_node_id = cls.test.create_node(cls.node_label, cls.start_node_attribute)
        cls.end_node_id = cls.test.create_node(cls.node_label, cls.end_node_attribute)

    @classmethod
    def tearDownClass(cls):
        cls.log.info("\n")
        cls.test.delete_node(cls.start_node_id, cls.node_label)
        cls.test.delete_node(cls.end_node_id, cls.node_label)

    def test_01_create_relation(self):
        self.log.info("\n")
        self.log.info('01' + 'test create_relation'.center(80, '-'))
        payload = {
            "start_id": self.start_node_id,
            "end_id": self.end_node_id,
        }
        testing_api = "/v1/neo4j/relations/%s" % self.relation_label
        self.log.info(f"POST API: {testing_api}")
        self.log.info(f"POST PAYLOAD: {payload}")
        try:
            res = self.app.post(testing_api, json=payload)
            self.log.info(f"COMPARING: {res.status_code} VS {200}")
            self.assertEqual(res.status_code, 200)
            self.log.info(f"POST RESPONSE: {res.data}")
            response = res.json[0]
            self.log.info(f"RESPONSE JSON: \n {response}")
        except Exception as e:
            self.log.error(e)
            raise e

    def test_01_2_create_relation_list(self):
        self.log.info("\n")
        self.log.info('01.2' + 'test create_relation_list'.center(80, '-'))
        payload = {
            "start_id": [self.start_node_id],
            "end_id": [self.end_node_id],
        }
        testing_api = "/v1/neo4j/relations/%s" % self.relation_label
        self.log.info(f"POST API: {testing_api}")
        self.log.info(f"POST PAYLOAD: {payload}")
        try:
            res = self.app.post(testing_api, json=payload)
            self.log.info(f"COMPARING: {res.status_code} VS {403}")
            self.assertEqual(res.status_code, 403)
            self.log.info(f"POST RESPONSE: {res.data}")
            response = res.json
            self.log.info(f"RESPONSE JSON: \n {response}")
            self.log.info(f"COMPARING: {'Both start_id and end_id can be the list'} VS {response}")
            self.assertIn('Both start_id and end_id can be the list', response)
        except Exception as e:
            self.log.error(e)
            raise e

    def test_01_3_create_relation_for_self(self):
        self.log.info("\n")
        self.log.info('01.3' + 'test create_relation_for_self'.center(80, '-'))
        testing_api = "/v1/neo4j/relations/%s" % self.relation_label
        payload = {
            "start_id": self.start_node_id,
            "end_id": self.start_node_id,
        }
        self.log.info(f"POST API: {testing_api}")
        self.log.info(f"POST PAYLOAD: {payload}")
        try:
            res = self.app.post(testing_api, json=payload)
            self.log.info(f"COMPARING: {res.status_code} VS {403}")
            self.assertEqual(res.status_code, 403)
            self.log.info(f"POST RESPONSE: {res.data}")
            self.log.info(f"COMPARING: {'Error cannot add yourself as parent/child'} VS {res.data}")
            self.assertIn(b"Error cannot add yourself as parent/child", res.data)
        except Exception as e:
            self.log.error(e)
            raise e


    def test_02_create_relation_without_start_node_id(self):
        self.log.info("\n")
        self.log.info('02' + 'test create_relation_without_start_node_id'.center(80, '-'))
        payload = {
            "start_id": None,
            "end_id": self.end_node_id,
        }
        testing_api = "/v1/neo4j/relations/%s" % self.relation_label
        self.log.info(f"POST API: {testing_api}")
        self.log.info(f"POST PAYLOAD: {payload}")
        try:
            res = self.app.post(testing_api, json=payload)
            self.log.info(f"COMPARING: {res.status_code} VS {200}")
            self.assertEqual(res.status_code, 403)
            self.log.info(f"POST RESPONSE: {res}")
            self.log.info(f"POST RESPONSE: {res.data}")
            response = res.json
            self.log.info(f"RESPONSE JSON: \n {response}")
        except Exception as e:
            self.log.error(e)
            raise e

    def test_02_1_create_relation_without_id(self):
        self.log.info("\n")
        self.log.info('02.1' + 'test create_relation_without_id'.center(80, '-'))
        payload = {
            "start_id": None,
            "end_id": None,
        }
        testing_api = "/v1/neo4j/relations/%s" % self.relation_label
        self.log.info(f"POST API: {testing_api}")
        self.log.info(f"POST PAYLOAD: {payload}")
        try:
            res = self.app.post(testing_api, json=payload)
            self.log.info(f"COMPARING: {res.status_code} VS {403}")
            self.assertEqual(res.status_code, 403)
            self.log.info(f"POST RESPONSE: {res.data}")
            self.log.info(f"COMPARING: {'start_id and end_id are required'} VS {res.data}")
            self.assertIn(b'start_id and end_id are required', res.data)
        except Exception as e:
            self.log.error(e)
            raise e

    #def test_03_create_relation_with_non_exist_node_id(self):
    #    self.log.info("\n")
    #    self.log.info('03' + 'test create_relation_with_non_exist_node_id'.center(80, '-'))
    #    payload = {
    #        "start_id": 1,
    #        "end_id": self.end_node_id,
    #    }
    #    testing_api = "/v1/neo4j/relations/%s" % self.relation_label
    #    self.log.info(f"POST API: {testing_api}")
    #    self.log.info(f"POST PAYLOAD: {payload}")
    #    try:
    #        res = self.app.post(testing_api, json=payload)
    #        self.log.info(f"COMPARING: {res.status_code} VS {200}")
    #        self.assertEqual(res.status_code, 200)
    #        self.log.info(f"POST RESPONSE: {res.data}")
    #        response = res.json[0]
    #        self.log.info(f"RESPONSE JSON: \n {response}")
    #    except Exception as e:
    #        self.log.error(e)
    #        raise e

    def test_04_create_relation_for_exist_node_id(self):
        self.log.info("\n")
        self.log.info('04' + 'test create_relation_for_exist_node_id'.center(80, '-'))
        payload = {
            "start_id": self.start_node_id,
            "end_id": self.end_node_id,
        }
        testing_api = "/v1/neo4j/relations/%s" % self.relation_label
        self.log.info(f"POST API: {testing_api}")
        self.log.info(f"POST PAYLOAD: {payload}")
        try:
            res = self.app.post(testing_api, json=payload)
            self.log.info(f"COMPARING: {res.status_code} VS {403}")
            self.assertEqual(res.status_code, 403)
            self.log.info(f"POST RESPONSE: {res.data}")
            response = res.json[0]
            self.log.info(f"RESPONSE JSON: \n {response}")
            self.log.info(f"COMPARING: {b'already be the parent(s)'} "
                          f"IN {res.data}")
            self.assertIn(b"already be the parent(s)", res.data)
        except Exception as e:
            self.log.error(e)
            raise e

    def test_05_get_relation(self):
        self.log.info("\n")
        self.log.info('05' + 'test get_relation'.center(80, '-'))
        params = {
            "label": self.relation_label,
            "start_id": self.start_node_id,
            "end_id": self.end_node_id
        }
        testing_api = "/v1/neo4j/relations"
        self.log.info(f"GET API: {testing_api}")
        self.log.info(f"GET PARAMS: {params}")
        try:
            # Test client can only take 'query_string' as url parameters
            res = self.app.get(testing_api, query_string=params)
            self.log.info(f"GET RESPONSE: {res}")
            self.assertEqual(res.status_code, 200)
            res = res.json[0]
            self.log.info(f"RESPONSE JSON: {res}")
            self.log.info(f"CHECK RELATION TYPE: {res['r']['type']} VS {self.relation_label}")
            self.assertEqual(res['r']['type'], self.relation_label)
            path = res['p']
            start_node = path.get('start_node', None)
            self.log.info(f"CHECK RELATION PARENT ID: {start_node['id']} VS {self.start_node_id}")
            self.assertEqual(start_node['id'], self.start_node_id)
            end_node = start_node['children']['end_node']
            self.log.info(f"CHECK RELATION CHILD ID: {end_node['id']} VS {self.end_node_id}")
            self.assertEqual(end_node['id'], self.end_node_id)
        except Exception as e:
            self.log.error(e)
            raise e

    def test_06_get_relation_with_wrong_label(self):
        self.log.info("\n")
        self.log.info('06' + 'test get_relation_with_wrong_label'.center(80, '-'))
        params = {
            "label": self.node_label,
            "start_id": self.start_node_id,
            "end_id": self.end_node_id
        }
        testing_api = "/v1/neo4j/relations"
        self.log.info(f"GET API: {testing_api}")
        self.log.info(f"GET PARAMS: {params}")
        try:
            # Test client can only take 'query_string' as url parameters
            res = self.app.get(testing_api, query_string=params)
            self.log.info(f"GET RESPONSE: {res}")
            self.assertEqual(res.status_code, 200)
            self.log.info(f"RESPONSE DATA: {res.data}")
            self.log.info(f"COMPARING RESPONSE: {res.json} VS {[]}")
            self.assertEqual(res.json, [])
        except Exception as e:
            self.log.error(e)
            raise e

    def test_07_get_relation_with_reverse_id(self):
        self.log.info("\n")
        self.log.info('07' + 'test get_relation_with_reverse_id'.center(80, '-'))
        params = {
            "label": self.relation_label,
            "start_id": self.end_node_id,
            "end_id": self.start_node_id
        }
        testing_api = "/v1/neo4j/relations"
        self.log.info(f"GET API: {testing_api}")
        self.log.info(f"GET PARAMS: {params}")
        try:
            # Test client can only take 'query_string' as url parameters
            res = self.app.get(testing_api, query_string=params)
            self.log.info(f"GET RESPONSE: {res}")
            self.assertEqual(res.status_code, 200)
            self.log.info(f"RESPONSE DATA: {res.data}")
            self.log.info(f"COMPARING RESPONSE: {res.json} VS {[]}")
            self.assertEqual(res.json, [])
        except Exception as e:
            self.log.error(e)
            raise e

    def test_08_get_relation_without_child_id(self):
        self.log.info("\n")
        self.log.info('08' + 'test get_relation_without_child_id'.center(80, '-'))
        params = {
            "label": self.relation_label,
            "start_id": self.start_node_id
        }
        testing_api = "/v1/neo4j/relations"
        self.log.info(f"GET API: {testing_api}")
        self.log.info(f"GET PARAMS: {params}")
        try:
            # Test client can only take 'query_string' as url parameters
            res = self.app.get(testing_api, query_string=params)
            self.log.info(f"GET RESPONSE: {res}")
            self.assertEqual(res.status_code, 200)
            self.log.info(f"RESPONSE DATA: {res.data}")
            res = res.json[0]
            self.log.info(f"RESPONSE JSON: {res}")
            self.log.info(f"CHECK RELATION TYPE: {res['r']['type']} VS {self.relation_label}")
            self.assertEqual(res['r']['type'], self.relation_label)
            path = res['p']
            start_node = path.get('start_node', None)
            self.log.info(f"CHECK RELATION PARENT ID: {start_node['id']} VS {self.start_node_id}")
            self.assertEqual(start_node['id'], self.start_node_id)
            end_node = start_node['children']['end_node']
            self.log.info(f"CHECK RELATION CHILD ID: {end_node['id']} VS {self.end_node_id}")
            self.assertEqual(end_node['id'], self.end_node_id)
        except Exception as e:
            self.log.error(e)
            raise e

    def test_09_get_relation_without_parent_id(self):
        self.log.info("\n")
        self.log.info('09' + 'test get_relation_without_parent_id'.center(80, '-'))
        params = {
            "label": self.relation_label,
            "end_id": self.start_node_id
        }
        testing_api = "/v1/neo4j/relations"
        self.log.info(f"GET API: {testing_api}")
        self.log.info(f"GET PARAMS: {params}")
        try:
            # Test client can only take 'query_string' as url parameters
            res = self.app.get(testing_api, query_string=params)
            self.log.info(f"GET RESPONSE: {res}")
            self.assertEqual(res.status_code, 200)
            self.log.info(f"RESPONSE DATA: {res.data}")
            self.log.info(f"COMPARING RESPONSE: {res.json} VS {[]}")
            self.assertEqual(res.json, [])
        except Exception as e:
            self.log.error(e)
            raise e

    def test_10_get_relation_without_id(self):
        self.log.info("\n")
        self.log.info('10' + 'test get_relation_without_id'.center(80, '-'))
        params = {
            "label": self.relation_label
        }
        testing_api = "/v1/neo4j/relations"
        self.log.info(f"GET API: {testing_api}")
        self.log.info(f"GET PARAMS: {params}")
        try:
            # Test client can only take 'query_string' as url parameters
            res = self.app.get(testing_api, query_string=params)
            self.log.info(f"GET RESPONSE: {res}")
            self.assertEqual(res.status_code, 403)
            self.log.info(f"RESPONSE DATA: {res.data}")
            self.log.info(f"COMPARING RESPONSE: {'start_id and end_id are required'} IN {res.json}")
            self.assertIn("start_id and end_id are required", res.json)
        except Exception as e:
            self.log.error(e)
            raise e

    def test_11_update_relation(self):
        self.log.info("\n")
        self.log.info('11' + 'test update_relation'.center(80, '-'))
        # Check original label
        params = {
            "label": self.relation_label,
            "start_id": self.start_node_id,
            "end_id": self.end_node_id
        }
        try:
            origin_res = self.app.get("/v1/neo4j/relations", query_string=params)
            self.assertEqual(origin_res.status_code, 200)
            origin_res = origin_res.json[0]
            self.log.info(f"ORIGINAL RELATION TYPE: {origin_res['r']['type']}")
            self.assertEqual(origin_res['r']['type'], self.relation_label)

            # Update relation with new label
            payload = {
                "new_label": "new_label",
                "start_id": self.start_node_id,
                "end_id": self.end_node_id,
            }
            testing_api = "/v1/neo4j/relations/%s" % self.relation_label
            self.log.info(f"PUT API: {testing_api}")
            self.log.info(f"PUT PAYLOAD: {payload}")
            res = self.app.put(testing_api, json=payload)
            self.log.info(f"PUT RESPONSE: {res.data}")
            response = res.json[0]
            self.log.info(f"RESPONSE JSON: \n {response}")
            self.log.info(f"COMPARING STATUS: {res.status_code} VS {200}")
            self.assertEqual(res.status_code, 200)
            self.relation_label = "new_label"

            # check if the label updated
            params = {
                "label": "new_label",
                "start_id": self.start_node_id,
                "end_id": self.end_node_id
            }
            check_res = self.app.get("/v1/neo4j/relations", query_string=params)
            self.assertEqual(check_res.status_code, 200)
            check_res = check_res.json[0]
            self.log.info(f"UPDATED RELATION TYPE: {check_res['r']['type']}")
            self.assertEqual(check_res['r']['type'], self.relation_label)
            self.log.info(f"COMPARE ORIGIN LABEL VS NEW LABEL: {origin_res['r']['type']} VS {check_res['r']['type']}")
            self.assertNotEqual(origin_res['r']['type'], check_res['r']['type'])
            self.relation_label ="new_label"
        except Exception as e:
            self.log.error(e)
            raise e

    def test_12_update_relation_with_same_value(self):
        self.log.info("\n")
        self.log.info('12' + 'test update_relation_with_same_value'.center(80, '-'))
        # Check original label
        params = {
            "label": "new_label",
            "start_id": self.start_node_id,
            "end_id": self.end_node_id
        }
        try:
            origin_res = self.app.get("/v1/neo4j/relations", query_string=params)
            self.assertEqual(origin_res.status_code, 200)
            origin_res = origin_res.json[0]
            self.log.info(f"ORIGINAL RELATION TYPE: {origin_res['r']['type']}")
            self.assertEqual(origin_res['r']['type'], "new_label")

            # Update relation with new label
            payload = {
                "new_label": "new_label",
                "start_id": self.start_node_id,
                "end_id": self.end_node_id,
            }
            testing_api = "/v1/neo4j/relations/%s" % self.relation_label
            self.log.info(f"PUT API: {testing_api}")
            self.log.info(f"PUT PAYLOAD: {payload}")
            res = self.app.put(testing_api, json=payload)
            self.log.info(f"PUT RESPONSE: {res.data}")
            response = res.json[0]
            self.log.info(f"RESPONSE JSON: \n {response}")
            self.log.info(f"COMPARING STATUS: {res.status_code} VS {200}")
            self.assertEqual(res.status_code, 200)

            # check if the label updated
            params = {
                "label": "new_label",
                "start_id": self.start_node_id,
                "end_id": self.end_node_id
            }
            check_res = self.app.get("/v1/neo4j/relations", query_string=params)
            self.assertEqual(check_res.status_code, 200)
            check_res = check_res.json[0]
            self.log.info(f"UPDATED RELATION TYPE: {check_res['r']['type']}")
            self.assertEqual(check_res['r']['type'], "new_label")
            self.log.info(f"COMPARE ORIGIN LABEL VS NEW LABEL: {origin_res['r']['type']} VS {check_res['r']['type']}")
            self.assertEqual(origin_res['r']['type'], check_res['r']['type'])
        except Exception as e:
            self.log.error(e)
            raise e

    def test_13_update_relation_without_label(self):
        self.log.info("\n")
        self.log.info('13' + 'test update_relation_without_label'.center(80, '-'))
        # Check original label
        params = {
            "label": "new_label",
            "start_id": self.start_node_id,
            "end_id": self.end_node_id
        }
        try:
            origin_res = self.app.get("/v1/neo4j/relations", query_string=params)
            self.assertEqual(origin_res.status_code, 200)
            origin_res = origin_res.json[0]
            self.log.info(f"ORIGINAL RELATION TYPE: {origin_res['r']['type']}")
            self.assertEqual(origin_res['r']['type'], "new_label")

            # Update relation with new label
            payload = {
                "start_id": self.start_node_id,
                "end_id": self.end_node_id,
            }
            testing_api = "/v1/neo4j/relations/%s" % self.relation_label
            self.log.info(f"PUT API: {testing_api}")
            self.log.info(f"PUT PAYLOAD: {payload}")
            res = self.app.put(testing_api, json=payload)
            self.log.info(f"PUT RESPONSE: {res.data}")
            response = res.json[0]
            self.log.info(f"RESPONSE JSON: \n {response}")
            self.log.info(f"COMPARING STATUS: {res.status_code} VS {403}")
            self.assertEqual(res.status_code, 403)
            self.log.info(f"COMPARING RESPONSE: {'start_id, new_label and end_id are required'} IN {res.json}")
            self.assertIn("start_id, new_label and end_id are required", res.json)
        except Exception as e:
            self.log.error(e)
            raise e

    def test_14_update_relation_without_id(self):
        self.log.info("\n")
        self.log.info('14' + 'test update_relation_without_id'.center(80, '-'))
        # Check original label
        params = {
            "label": "new_label",
            "start_id": self.start_node_id,
            "end_id": self.end_node_id
        }
        try:
            origin_res = self.app.get("/v1/neo4j/relations", query_string=params)
            self.assertEqual(origin_res.status_code, 200)
            origin_res = origin_res.json[0]
            self.log.info(f"ORIGINAL RELATION TYPE: {origin_res['r']['type']}")
            self.assertEqual(origin_res['r']['type'], "new_label")

            # Update relation with new label
            payload = {
                "new_label": self.relation_label,
                "start_id": self.start_node_id
            }
            testing_api = "/v1/neo4j/relations/%s" % self.relation_label
            self.log.info(f"PUT API: {testing_api}")
            self.log.info(f"PUT PAYLOAD: {payload}")
            res = self.app.put(testing_api, json=payload)
            self.log.info(f"PUT RESPONSE: {res.data}")
            response = res.json[0]
            self.log.info(f"RESPONSE JSON: \n {response}")
            self.log.info(f"COMPARING STATUS: {res.status_code} VS {403}")
            self.assertEqual(res.status_code, 403)
            self.log.info(f"COMPARING RESPONSE: {'start_id, new_label and end_id are required'} IN {res.json}")
            self.assertIn("start_id, new_label and end_id are required", res.json)
        except Exception as e:
            self.log.error(e)
            raise e

    def test_15_update_relation_with_non_exist_id(self):
        self.log.info("\n")
        self.log.info('15' + 'test update_relation_with_non_exist_id'.center(80, '-'))
        # Check original label
        params = {
            "label": "new_label",
            "start_id": self.start_node_id,
            "end_id": self.end_node_id
        }
        try:
            origin_res = self.app.get("/v1/neo4j/relations", query_string=params)
            self.assertEqual(origin_res.status_code, 200)
            origin_res = origin_res.json[0]
            self.log.info(f"ORIGINAL RELATION TYPE: {origin_res['r']['type']}")
            self.assertEqual(origin_res['r']['type'], "new_label")

            # Update relation with new label
            payload = {
                "new_label": self.relation_label,
                "start_id": self.start_node_id,
                "end_id": 1
            }
            testing_api = "/v1/neo4j/relations/%s" % self.relation_label
            self.log.info(f"PUT API: {testing_api}")
            self.log.info(f"PUT PAYLOAD: {payload}")
            res = self.app.put(testing_api, json=payload)
            self.log.info(f"PUT RESPONSE: {res.data}")
            response = res.json[0]
            self.log.info(f"RESPONSE JSON: \n {response}")
            self.log.info(f"COMPARING STATUS: {res.status_code} VS {200}")
            self.assertEqual(res.status_code, 200)
            self.log.info(f"COMPARING RESPONSE: {'success'} IN {res.json}")
            self.assertIn("success", res.json)
        except Exception as e:
            self.log.error(e)
            raise e

    def test_16_update_relation_for_non_exist_relation(self):
        self.log.info("\n")
        self.log.info('16' + 'test update_relation_for_non_exist_relation'.center(80, '-'))
        temp_node_id = self.test.create_node(self.node_label, self.start_node_attribute)
        self.log.info(f"TEMP NODE CREATED WITH ID: {temp_node_id}")
        # Update relation with new label
        payload = {
            "new_label": self.relation_label,
            "start_id": self.start_node_id,
            "end_id": temp_node_id
        }
        try:
            testing_api = "/v1/neo4j/relations/%s" % self.relation_label
            self.log.info(f"PUT API: {testing_api}")
            self.log.info(f"PUT PAYLOAD: {payload}")
            res = self.app.put(testing_api, json=payload)
            self.log.info(f"PUT RESPONSE: {res.data}")
            response = res.json
            self.log.info(f"RESPONSE JSON: \n {response}")
            self.log.info(f"COMPARING STATUS: {res.status_code} VS {200}")
            self.assertEqual(res.status_code, 200)
            self.log.info(f"COMPARING RESPONSE JSON: {response} VS {'success'}")
            self.assertEqual(response, 'success')
            self.test.delete_node(temp_node_id, self.node_label)
        except Exception as e:
            self.log.error(e)
            raise e

    def test_17_get_end_node_by_relation(self):
        self.__class__.relation_label = "new_label"
        self.log.info("\n")
        self.log.info('17' + 'test get_end_node_by_relation'.center(80, '-'))
        # check the end node by giving start node ID
        testing_api = "/v1/neo4j/relations/%s/node/" % self.relation_label
        get_start = testing_api + str(self.start_node_id)
        self.log.info(f"GET START NODE API: {get_start}")
        try:
            res = self.app.get(get_start)
            self.log.info(f"RESPONSE: {res}")
            self.log.info(f"COMPARING STATUS: {res.status_code} VS {200}")
            self.assertEqual(res.status_code, 200)
            res = res.json[0]
            self.log.info(f"COMPARING NODE ID: {res['id']} VS {self.end_node_id}")
            self.assertEqual(res['id'], self.end_node_id)
        except Exception as e:
            self.log.error(e)
            raise e

    def test_18_get_start_node_by_relation(self):
        self.log.info("\n")
        self.log.info('18' + 'test get_start_node_by_relation'.center(80, '-'))
        # check the start node by giving end node ID
        params = {"start": False}
        testing_api = "/v1/neo4j/relations/%s/node/" % self.relation_label
        get_end = testing_api + str(self.end_node_id)
        self.log.info(f"GET END NODE API: {get_end}")
        self.log.info(f"GET PARAMS: {params}")
        try:
            res = self.app.get(get_end, query_string=params)
            self.log.info(f"COMPARING STATUS: {res.status_code} VS {200}")
            self.assertEqual(res.status_code, 200)
            res = res.json[0]
            self.log.info(f"COMPARING NODE ID: {res['id']} VS {self.start_node_id}")
            self.assertEqual(res['id'], self.start_node_id)
        except Exception as e:
            self.log.error(e)
            raise e

    def test_19_get_start_node_by_non_exist_relation(self):
        self.log.info("\n")
        self.log.info('19' + 'test get_start_node_by_non_exist_relation'.center(80, '-'))
        # check the start node by giving end node ID
        params = {"start": False}
        testing_api = "/v1/neo4j/relations/%s/node/" % "fake_relation"
        get_end = testing_api + str(self.end_node_id)
        self.log.info(f"GET END NODE API: {get_end}")
        self.log.info(f"GET PARAMS: {params}")
        try:
            res = self.app.get(get_end, query_string=params)
            self.log.info(f"COMPARING STATUS: {res.status_code} VS {200}")
            self.assertEqual(res.status_code, 200)
            self.log.info(f"RESPONSE: {res}, DATA: {res.data}, JSON: {res.json}")
            self.log.info(f"COMPARING RESULT: {res.json} VS {[]}")
            self.assertEqual(res.json, [])
        except Exception as e:
            self.log.error(e)
            raise e

    def test_20_get_non_exist_id_by_relation(self):
        self.log.info("\n")
        self.log.info('20' + 'test get_none_exist_id_by_relation'.center(80, '-'))
        # check the start node by giving end node ID
        params = {"start": False}
        testing_api = "/v1/neo4j/relations/%s/node/" % self.relation_label
        get_end = testing_api + str(1)
        self.log.info(f"GET END NODE API: {get_end}")
        self.log.info(f"GET PARAMS: {params}")
        try:
            res = self.app.get(get_end, query_string=params)
            self.log.info(f"COMPARING STATUS: {res.status_code} VS {200}")
            self.assertEqual(res.status_code, 200)
            self.log.info(f"RESPONSE: {res}, DATA: {res.data}, JSON: {res.json}")
            self.log.info(f"COMPARING RESULT: {res.json} VS {[]}")
            self.assertEqual(res.json, [])
        except Exception as e:
            self.log.error(e)
            raise e

    def test_21_get_relation_by_query(self):
        """
        response = {'end_node': {'id': 204,
                                 'labels': ['test_label'],
                                 'name': 'end_node',
                                 'time_created': '2020-10-09T13:07:57',
                                 'time_lastmodified': '2020-10-09T13:07:57',
                                 'test_original_key': 'test_original_end'},
                    'p': {'start_node': {'id': 203,
                                         'children': {'end_node': {'id': 204,
                                                                   'children': {}
                                                                  }
                                                      }
                                        }
                         },
                    'r': {'type': 'new_label'},
                    'start_node': {'id': 203,
                                   'labels': ['test_label'],
                                   'name': 'start_node',
                                   'time_created': '2020-10-09T13:07:57',
                                   'time_lastmodified': '2020-10-09T13:07:57',
                                   'test_original_key': 'test_original_start'}
         }
        """
        # Get the relationship by the properties of node: ActionOnRelationshipByQuery.post
        self.log.info("\n")
        self.log.info('21' + 'test get_relation_by_query'.center(80, '-'))
        testing_api = '/v1/neo4j/relations/query'
        payload = {'label': self.relation_label,
                   'start_label': self.node_label,
                   'end_label': self.node_label,
                   'start_params': self.start_node_attribute,
                   'end_params': self.end_node_attribute
                  }
        self.log.info(f"POST API: {testing_api}")
        self.log.info(f"POST PAYLOAD: {payload}")
        try:
            response = self.app.post(testing_api, json=payload)
            self.log.info(f"COMPARING STATUS: {response.status_code} VS {200}")
            self.assertEqual(response.status_code, 200)
            response = response.json
            # Find the relation that match this round of test
            res = next(x for x in response if x['end_node']['id'] == self.end_node_id)
            self.log.info(f"MATCHED RECORD: {res}")
            self.log.info(f"COMPARING end_node ID: {res['end_node']['id']} VS {self.end_node_id}")
            self.assertEqual(res['end_node']['id'], self.end_node_id)
            self.log.info(f"COMPARING end_node labels: {res['end_node']['labels']} VS {[self.node_label]}")
            self.assertEqual(res['end_node']['labels'], [self.node_label])
            self.log.info(f"COMPARING end_node attribute: "
                          f"{res['end_node']['name']} VS {self.end_node_attribute['name']}, "
                          f"{res['end_node']['test_original_key']} VS {self.end_node_attribute['test_original_key']}")
            self.assertEqual(res['end_node']['test_original_key'], self.end_node_attribute['test_original_key'])

            p = res['p']
            self.log.info(f"COMPARING p start_node id: {p['start_node']['id']} VS {self.start_node_id}")
            self.assertEqual(p['start_node']['id'], self.start_node_id)
            self.log.info(f"COMPARING p start_node children node id: "
                          f"{p['start_node']['children']['end_node']['id']} VS {self.end_node_id}")
            self.assertEqual(p['start_node']['children']['end_node']['id'], self.end_node_id)

            r = res['r']
            self.log.info(f"COMPARING r type: {r['type']} VS {self.relation_label}")
            self.assertEqual(r['type'], self.relation_label)

            start_node = res['start_node']
            self.log.info(f"COMPARING start_node id: {start_node['id']} VS {self.start_node_id}")
            self.assertEqual(start_node['id'], self.start_node_id)
            self.log.info(f"COMPARING start_node label: {start_node['labels']} VS {[self.node_label]}")
            self.assertEqual(start_node['labels'], [self.node_label])
            self.log.info(f"COMPARING start_node attribute: "
                          f"{start_node['name']} VS {self.start_node_attribute['name']}, "
                          f"{start_node['test_original_key']} VS {self.start_node_attribute['test_original_key']}")
            self.assertEqual(start_node['test_original_key'], self.start_node_attribute['test_original_key'])
        except Exception as e:
            self.log.error(e)
            raise e

    def test_22_get_relation_by_query_with_only_label(self):
        self.log.info("\n")
        self.log.info('22' + 'test get_relation_by_query_with_only_label'.center(80, '-'))
        testing_api = '/v1/neo4j/relations/query'
        payload = {'label': self.relation_label}
        self.log.info(f"POST API: {testing_api}")
        self.log.info(f"POST PAYLOAD: {payload}")
        try:
            response = self.app.post(testing_api, json=payload)
            self.log.info(f"COMPARING STATUS: {response.status_code} VS {200}")
            self.assertEqual(response.status_code, 200)
            response = response.json
            # Find the relation that match this round of test
            res = next(x for x in response if x['end_node']['id'] == self.end_node_id)
            self.log.info(f"MATCHED RECORD: {res}")
            self.log.info(f"COMPARING end_node ID: {res['end_node']['id']} VS {self.end_node_id}")
            self.assertEqual(res['end_node']['id'], self.end_node_id)
            self.log.info(f"COMPARING end_node labels: {res['end_node']['labels']} VS {[self.node_label]}")
            self.assertEqual(res['end_node']['labels'], [self.node_label])
            self.log.info(f"COMPARING end_node attribute: "
                          f"{res['end_node']['name']} VS {self.end_node_attribute['name']}, "
                          f"{res['end_node']['test_original_key']} VS {self.end_node_attribute['test_original_key']}")
            self.assertEqual(res['end_node']['test_original_key'], self.end_node_attribute['test_original_key'])

            p = res['p']
            self.log.info(f"COMPARING p start_node id: {p['start_node']['id']} VS {self.start_node_id}")
            self.assertEqual(p['start_node']['id'], self.start_node_id)
            self.log.info(f"COMPARING p start_node children node id: "
                          f"{p['start_node']['children']['end_node']['id']} VS {self.end_node_id}")
            self.assertEqual(p['start_node']['children']['end_node']['id'], self.end_node_id)

            r = res['r']
            self.log.info(f"COMPARING r type: {r['type']} VS {self.relation_label}")
            self.assertEqual(r['type'], self.relation_label)

            start_node = res['start_node']
            self.log.info(f"COMPARING start_node id: {start_node['id']} VS {self.start_node_id}")
            self.assertEqual(start_node['id'], self.start_node_id)
            self.log.info(f"COMPARING start_node label: {start_node['labels']} VS {[self.node_label]}")
            self.assertEqual(start_node['labels'], [self.node_label])
            self.log.info(f"COMPARING start_node attribute: "
                          f"{start_node['name']} VS {self.start_node_attribute['name']}, "
                          f"{start_node['test_original_key']} VS {self.start_node_attribute['test_original_key']}")
            self.assertEqual(start_node['test_original_key'], self.start_node_attribute['test_original_key'])
        except Exception as e:
            self.log.error(e)
            raise e

    def test_23_get_relation_by_query_with_wrong_end_node_label(self):
        self.log.info("\n")
        self.log.info('23' + 'test get_relation_by_query_wrong_end_node_label'.center(80, '-'))
        testing_api = '/v1/neo4j/relations/query'
        payload = {'label': self.relation_label,
                   'start_label': self.node_label,
                   'end_label': "someother_label",
                   'start_params': self.start_node_attribute,
                   'end_params': self.end_node_attribute
                   }
        self.log.info(f"POST API: {testing_api}")
        self.log.info(f"POST PAYLOAD: {payload}")
        try:
            response = self.app.post(testing_api, json=payload)
            self.log.info(f"COMPARING STATUS: {response.status_code} VS {200}")
            self.assertEqual(response.status_code, 200)
            response = response.json
            self.log.info(f"COMPARING RESPONSE: {response} VS {[]}")
            self.assertEqual(response, [])
        except Exception as e:
            self.log.error(e)
            raise e

    def test_23_get_relation_by_query_with_wrong_label(self):
        self.log.info("\n")
        self.log.info('23' + 'test get_relation_by_query_wrong_label'.center(80, '-'))
        testing_api = '/v1/neo4j/relations/query'
        payload = {'label': "OTHER_RELATION",
                   'start_label': self.node_label,
                   'end_label': self.node_label,
                   'start_params': self.start_node_attribute,
                   'end_params': self.end_node_attribute
                   }
        self.log.info(f"POST API: {testing_api}")
        self.log.info(f"POST PAYLOAD: {payload}")
        try:
            response = self.app.post(testing_api, json=payload)
            self.log.info(f"COMPARING STATUS: {response.status_code} VS {200}")
            self.assertEqual(response.status_code, 200)
            response = response.json
            self.log.info(f"COMPARING RESPONSE: {response} VS {[]}")
            self.assertEqual(response, [])
        except Exception as e:
            self.log.error(e)
            raise e

    def test_24_get_relation_by_query_with_relation_label_none(self):
        self.log.info("\n")
        self.log.info('24' + 'test get_relation_by_query_with_relation_label_none'.center(80, '-'))
        testing_api = '/v1/neo4j/relations/query'
        payload = {'label': None,
                   'start_label': self.node_label,
                   'end_label': self.node_label,
                   'start_params': self.start_node_attribute,
                   'end_params': self.end_node_attribute
                   }
        self.log.info(f"POST API: {testing_api}")
        self.log.info(f"POST PAYLOAD: {payload}")
        try:
            response = self.app.post(testing_api, json=payload)
            self.log.info(f"COMPARING STATUS: {response.status_code} VS {200}")
            self.assertEqual(response.status_code, 200)
            response = response.json
            # Find the relation that match this round of test
            res = next(x for x in response if x['end_node']['id'] == self.end_node_id)
            self.log.info(f"MATCHED RECORD: {res}")
            self.log.info(f"COMPARING end_node ID: {res['end_node']['id']} VS {self.end_node_id}")
            self.assertEqual(res['end_node']['id'], self.end_node_id)
            self.log.info(f"COMPARING end_node labels: {res['end_node']['labels']} VS {[self.node_label]}")
            self.assertEqual(res['end_node']['labels'], [self.node_label])
            self.log.info(f"COMPARING end_node attribute: "
                          f"{res['end_node']['name']} VS {self.end_node_attribute['name']}, "
                          f"{res['end_node']['test_original_key']} VS {self.end_node_attribute['test_original_key']}")
            self.assertEqual(res['end_node']['test_original_key'], self.end_node_attribute['test_original_key'])

            p = res['p']
            self.log.info(f"COMPARING p start_node id: {p['start_node']['id']} VS {self.start_node_id}")
            self.assertEqual(p['start_node']['id'], self.start_node_id)
            self.log.info(f"COMPARING p start_node children node id: "
                          f"{p['start_node']['children']['end_node']['id']} VS {self.end_node_id}")
            self.assertEqual(p['start_node']['children']['end_node']['id'], self.end_node_id)

            r = res['r']
            self.log.info(f"COMPARING r type: {r['type']} VS {self.relation_label}")
            self.assertEqual(r['type'], self.relation_label)

            start_node = res['start_node']
            self.log.info(f"COMPARING start_node id: {start_node['id']} VS {self.start_node_id}")
            self.assertEqual(start_node['id'], self.start_node_id)
            self.log.info(f"COMPARING start_node label: {start_node['labels']} VS {[self.node_label]}")
            self.assertEqual(start_node['labels'], [self.node_label])
            self.log.info(f"COMPARING start_node attribute: "
                          f"{start_node['name']} VS {self.start_node_attribute['name']}, "
                          f"{start_node['test_original_key']} VS {self.start_node_attribute['test_original_key']}")
            self.assertEqual(start_node['test_original_key'], self.start_node_attribute['test_original_key'])
        except Exception as e:
            self.log.error(e)
            raise e

    def test_24_1_get_relation_by_query_with_id(self):
        self.log.info("\n")
        self.log.info('24.1' + 'test get_relation_by_query_with_relation_label_none'.center(80, '-'))
        testing_api = '/v1/neo4j/relations/query'
        start_param = self.start_node_attribute
        end_param = self.end_node_attribute
        start_param['id'] = self.start_node_id
        end_param['id'] = self.end_node_id
        payload = {'label': self.relation_label,
                   'start_label': self.node_label,
                   'end_label': self.node_label,
                   'start_params': start_param,
                   'end_params': end_param
                  }
        self.log.info(f"POST API: {testing_api}")
        self.log.info(f"POST PAYLOAD: {payload}")
        try:
            response = self.app.post(testing_api, json=payload)
            self.log.info(f"COMPARING STATUS: {response.status_code} VS {200}")
            self.assertEqual(response.status_code, 200)
            response = response.json
            # Find the relation that match this round of test
            res = next(x for x in response if x['end_node']['id'] == self.end_node_id)
            self.log.info(f"MATCHED RECORD: {res}")
            self.log.info(f"COMPARING end_node ID: {res['end_node']['id']} VS {self.end_node_id}")
            self.assertEqual(res['end_node']['id'], self.end_node_id)
            self.log.info(f"COMPARING end_node labels: {res['end_node']['labels']} VS {[self.node_label]}")
            self.assertEqual(res['end_node']['labels'], [self.node_label])
            self.log.info(f"COMPARING end_node attribute: "
                          f"{res['end_node']['name']} VS {self.end_node_attribute['name']}, "
                          f"{res['end_node']['test_original_key']} VS {self.end_node_attribute['test_original_key']}")
            self.assertEqual(res['end_node']['test_original_key'], self.end_node_attribute['test_original_key'])

            p = res['p']
            self.log.info(f"COMPARING p start_node id: {p['start_node']['id']} VS {self.start_node_id}")
            self.assertEqual(p['start_node']['id'], self.start_node_id)
            self.log.info(f"COMPARING p start_node children node id: "
                          f"{p['start_node']['children']['end_node']['id']} VS {self.end_node_id}")
            self.assertEqual(p['start_node']['children']['end_node']['id'], self.end_node_id)

            r = res['r']
            self.log.info(f"COMPARING r type: {r['type']} VS {self.relation_label}")
            self.assertEqual(r['type'], self.relation_label)

            start_node = res['start_node']
            self.log.info(f"COMPARING start_node id: {start_node['id']} VS {self.start_node_id}")
            self.assertEqual(start_node['id'], self.start_node_id)
            self.log.info(f"COMPARING start_node label: {start_node['labels']} VS {[self.node_label]}")
            self.assertEqual(start_node['labels'], [self.node_label])
            self.log.info(f"COMPARING start_node attribute: "
                          f"{start_node['name']} VS {self.start_node_attribute['name']}, "
                          f"{start_node['test_original_key']} VS {self.start_node_attribute['test_original_key']}")
            self.assertEqual(start_node['test_original_key'], self.start_node_attribute['test_original_key'])
        except Exception as e:
            self.log.error(e)
            raise e

    def test_25_get_relation_by_query_without_relation_label(self):
        """
        * IMPORTANT:
        By posting this API with empty payload {}, it will retrieve all result
        """
        self.log.info("\n")
        self.log.info('25' + 'test get_relation_by_query_without_relation_label'.center(80, '-'))
        testing_api = '/v1/neo4j/relations/query'
        payload = {}
        self.log.info(f"POST API: {testing_api}")
        self.log.info(f"POST PAYLOAD: {payload}")
        try:
            response = self.app.post(testing_api, json=payload)
            self.log.info(f"COMPARING STATUS: {response.status_code} VS {200}")
            self.assertEqual(response.status_code, 200)
            response = response.json
            # Find the relation that match this round of test
            res = next(x for x in response if x['end_node']['id'] == self.end_node_id)
            self.log.info(f"MATCHED RECORD: {res}")
            self.log.info(f"COMPARING end_node ID: {res['end_node']['id']} VS {self.end_node_id}")
            self.assertEqual(res['end_node']['id'], self.end_node_id)
            self.log.info(f"COMPARING end_node labels: {res['end_node']['labels']} VS {[self.node_label]}")
            self.assertEqual(res['end_node']['labels'], [self.node_label])
            self.log.info(f"COMPARING end_node attribute: "
                          f"{res['end_node']['name']} VS {self.end_node_attribute['name']}, "
                          f"{res['end_node']['test_original_key']} VS {self.end_node_attribute['test_original_key']}")
            self.assertEqual(res['end_node']['test_original_key'], self.end_node_attribute['test_original_key'])

            p = res['p']
            self.log.info(f"COMPARING p start_node id: {p['start_node']['id']} VS {self.start_node_id}")
            self.assertEqual(p['start_node']['id'], self.start_node_id)
            self.log.info(f"COMPARING p start_node children node id: "
                          f"{p['start_node']['children']['end_node']['id']} VS {self.end_node_id}")
            self.assertEqual(p['start_node']['children']['end_node']['id'], self.end_node_id)

            r = res['r']
            self.log.info(f"COMPARING r type: {r['type']} VS {self.relation_label}")
            self.assertEqual(r['type'], self.relation_label)

            start_node = res['start_node']
            self.log.info(f"COMPARING start_node id: {start_node['id']} VS {self.start_node_id}")
            self.assertEqual(start_node['id'], self.start_node_id)
            self.log.info(f"COMPARING start_node label: {start_node['labels']} VS {[self.node_label]}")
            self.assertEqual(start_node['labels'], [self.node_label])
            self.log.info(f"COMPARING start_node attribute: "
                          f"{start_node['name']} VS {self.start_node_attribute['name']}, "
                          f"{start_node['test_original_key']} VS {self.start_node_attribute['test_original_key']}")
            self.assertEqual(start_node['test_original_key'], self.start_node_attribute['test_original_key'])
            self.log.info(response)
        except Exception as e:
            self.log.error(e)
            raise e

    def test_26_test_delete_empty_relation(self):
        self.log.info("\n")
        self.log.info('26' + 'test delete_empty_relation'.center(80, '-'))
        testing_api = '/v1/neo4j/relations'
        self.log.info(f"DELETE API: {testing_api}")
        params = {
            "start_id": '',
            "end_id": self.end_node_id
        }
        self.log.info(f"DELETE PARAMS: {params}")
        try:
            # Test client can only take 'query_string' as url parameters
            res = self.app.delete(testing_api, query_string=params)
            self.assertEqual(res.status_code, 403)
            self.log.info(f"DELETE RESPONSE: {res}")
            res = res.json
            self.log.info(f"RESPONSE JSON: {res}")
            retrieve_api = '/v1/neo4j/relations'
            self.log.info(f"CHECK RELATION API: {retrieve_api}")
            check_res = self.app.get(retrieve_api, query_string=params)
            self.assertEqual(check_res.status_code, 200)
            check_res = check_res.json
            self.log.info(f'CHECK RELATION: {check_res}')
            self.log.info(f"CHECK RELATION EXISTS: {check_res != []}")
            self.assertIsNotNone(check_res)
        except Exception as e:
            self.log.error(e)
            raise e

    def test_27_test_delete_relation_without_id(self):
        self.log.info("\n")
        self.log.info('27' + 'test delete_relation_without_id'.center(80, '-'))
        testing_api = '/v1/neo4j/relations'
        self.log.info(f"DELETE API: {testing_api}")
        try:
            res = self.app.delete(testing_api)
            self.log.info(f"DELETE RESPONSE: {res}")
            self.assertEqual(res.status_code, 403)
            self.log.info(f"RESPONSE DATA: {res.data}")
            self.log.info(f"COMPARING: {b'start_id and end_id are required'} IN {res.data}")
            self.assertIn(b'start_id and end_id are required', res.data)
        except Exception as e:
            self.log.error(e)
            raise e

    def test_28_test_delete_relation_with_one_id(self):
        self.log.info("\n")
        self.log.info('28' + 'test delete_relation_with_one_id'.center(80, '-'))
        testing_api = '/v1/neo4j/relations'
        self.log.info(f"DELETE API: {testing_api}")
        params = {
            "end_id": self.end_node_id
        }
        self.log.info(f"DELETE PARAMS: {params}")
        try:
            res = self.app.delete(testing_api, query_string=params)
            self.assertEqual(res.status_code, 403)
            self.log.info(f"DELETE RESPONSE: {res}")
            res = res.json
            self.log.info(f"RESPONSE JSON: {res}")
            retrieve_api = '/v1/neo4j/relations'
            self.log.info(f"CHECK RELATION API: {retrieve_api}")
            check_res = self.app.get(retrieve_api, query_string=params)
            self.assertEqual(check_res.status_code, 200)
            check_res = check_res.json
            self.log.info(f'DOMPARING RELATION: {check_res} VS {[]}')
            self.log.info(f"CHECK RELATION EXISTS: {check_res != []}")
            self.assertIsNotNone(check_res)
        except Exception as e:
            self.log.error(e)
            raise e

    def test_29_test_delete_relation_without_relation(self):
        self.log.info("\n")
        self.log.info('29' + 'test delete_relation_with_one_id'.center(80, '-'))
        testing_api = '/v1/neo4j/relations'
        self.log.info(f"DELETE API: {testing_api}")
        end_node_id = self.test.create_node(self.node_label, self.end_node_attribute)
        params = {
            "start_id": self.start_node_id,
            "end_id": end_node_id
        }
        self.log.info(f"CHECK RELATION OF START NODE AND NEW NODE: {self.start_node_id} VS {end_node_id}")
        retrieve_api = '/v1/neo4j/relations'
        self.log.info(f"CHECK RELATION API: {retrieve_api}")
        origin_res = self.app.get(retrieve_api, query_string=params)
        self.assertEqual(origin_res.status_code, 200)
        origin_res = origin_res.json
        self.log.info(f'DOMPARING RELATION: {origin_res} VS {[]}')
        self.log.info(f"CHECK RELATION EXISTS: {origin_res != []}")
        self.log.info(f"DELETE PARAMS: {params}")
        try:
            res = self.app.delete(testing_api, query_string=params)
            self.assertEqual(res.status_code, 200)
            self.log.info(f"DELETE RESPONSE: {res}")
            res = res.json
            self.log.info(f"RESPONSE JSON: {res}")
            retrieve_api = '/v1/neo4j/relations'
            self.log.info(f"CHECK RELATION API: {retrieve_api}")
            check_res = self.app.get(retrieve_api, query_string=params)
            self.assertEqual(check_res.status_code, 200)
            check_res = check_res.json
            self.log.info(f'DOMPARING RELATION: {check_res} VS {[]}')
            self.log.info(f"CHECK RELATION EXISTS: {check_res != []}")
            self.test.delete_node(end_node_id, self.node_label)
        except Exception as e:
            self.log.error(e)
            raise e

    def test_30_test_delete_relation(self):
        self.log.info("\n")
        self.log.info('30' + 'test delete_relation'.center(80, '-'))
        testing_api = '/v1/neo4j/relations'
        self.log.info(f"DELETE API: {testing_api}")
        params = {
            "start_id": self.start_node_id,
            "end_id": self.end_node_id
        }
        self.log.info(f"DELETE PARAMS: {params}")
        try:
            res = self.app.delete(testing_api, query_string=params)
            self.log.info(f"GET RESPONSE: {res}")
            res = res.json
            self.log.info(f"RESPONSE JSON: {res}")
            retrieve_api = '/v1/neo4j/relations'
            self.log.info(f"CHECK RELATION API: {retrieve_api}")
            check_res = self.app.get(retrieve_api, query_string=params)
            self.assertEqual(check_res.status_code, 200)
            check_res = check_res.json
            self.log.info(f'DOMPARING RELATION: {check_res} VS {[]}')
            self.assertEqual(check_res, [])
        except Exception as e:
            self.log.error(e)
            raise e

# DEPRECATED: get node beyond relation '/v1/neo4j/relations/<label>/node/<id>/none'
