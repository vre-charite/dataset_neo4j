#
# this file is the basic operation on the neo4j includes
# add the node and relationship to fullfill the basic
# requirement on the neo4j
#

from datetime import datetime

from . import neo4j_connection
from config import ConfigClass
from utils import neo4j_obj_2_json, path_2_json, node_2_json
from services.logger_services.logger_factory_service import SrvLoggerFactory
from py2neo import Graph, Node, Relationship
from py2neo.matching import RelationshipMatcher, NodeMatcher, CONTAINS 
import neotime

class Neo4jClient(object):
     
    def __init__(self):
        self._logger = SrvLoggerFactory('api_invitation').get_logger()
        try:
            self.graph = Graph(
                ConfigClass.NEO4J_URL, 
                username=ConfigClass.NEO4J_USER, 
                password=ConfigClass.NEO4J_PASS,
                max_connections=200,
            )
            self.nodes = NodeMatcher(self.graph)
            self.relationships = RelationshipMatcher(self.graph)
        except Exception as e:
            self._logger.error("Error in __init__ connecting to Neo4j:" + str(e))

    def add_node(self, label, name, param={}):
        if label[0].isnumeric():
            raise Exception("Invalid input")
        node = Node(
            label, 
            name=name,
            time_created=neotime.DateTime.utc_now(),
            time_lastmodified=neotime.DateTime.utc_now(),
            **param,
        )
        parent_id = param.pop("parent_id", None)
        parent_relation = param.pop("parent_relation", None)
        # if we have parent then add relationship
        if parent_id and parent_relation:
            end_node = self.nodes.get(parent_id)
            relationship = Relationship(node, parent_relation, end_node) 
            self.graph.create(relationship)
        self.graph.create(node)
        return node

    def get_node(self, label, id):
        return self.graph.nodes.match(label).where("id(_) = %d" % id).first()
        #return self.graph.nodes.get(id)

    # in order to facilitate the query in the frontend
    # we provide all the possible key with value with it
    def get_property_by_label(self, label):
        #neo4j_session = neo4j_connection.session()
        #query = 'MATCH (n:%s) UNWIND keys(n) as key \
        #    return key, collect(distinct n[key]) as options' % (label)
        #res = neo4j_session.run(query)
        #return res
        return self.nodes.match(label).all()

    def update_node(self, label, id, params={}, update_modified_time=True):
        node = self.get_node(label, id)
        if update_modified_time:
            node.update(**params, time_lastmodified=neotime.DateTime.utc_now())
        else:
            node.update(**params)
        self.graph.push(node)
        return node

    def query_node(self, label, params=None, limit=None, skip=None, count=False, partial=False, order_by=None, order_type=None):
        if partial:
            for key, value in params.items():
                if isinstance(value, str):
                    params[key] = CONTAINS(value)
                else:
                    params[key] = value
        if params:
            query = self.nodes.match(label, **params)
        else:
            query = self.nodes.match(label)

        if count:
            return query.count()
        if order_by: 
            if order_type and order_type.lower() == "desc":
                order_by = f"_.{order_by} DESC"
            else:
                order_by = f"_.{order_by}"
            query = query.order_by(order_by)
        if limit:
            query = query.limit(limit)
        if skip:
            query = query.skip(skip)
        return query.all() 

    # method allow to query the relationship
    # also the parameter allow the none so that we can query the 1-to-1
    def get_relation(self, relation_label, start_id=None, end_id=None):
        start_node = None
        end_node = None
        if start_id:
            start_node = self.nodes.get(start_id)
        if end_id:
            end_node = self.nodes.get(end_id)

        if not start_node and not end_node:
            return []
        if relation_label:
            return self.relationships.match((start_node, end_node), r_type=relation_label).all()
        else:
            return self.relationships.match((start_node, end_node)).all()

    def add_relation_between_nodes(self, relation_label, start_id, end_id):
        if type(start_id) == list and type(end_id) == list:
            raise Exception('Both start_id and end_id can be the list')
        if start_id == end_id:
            raise Exception("Error cannot add yourself as parent/child")
        start_node = self.nodes.get(start_id)
        end_node = self.nodes.get(end_id)
        relationship = self.relationships.match((start_node, end_node)).first()
        if hasattr(relationship, "start_node") and hasattr(relationship, "end_node"):
            raise Exception("dataset(s) already be the parent(s).")

        relationship = Relationship(start_node, relation_label, end_node)
        self.graph.create(relationship)
        return relationship

    def update_relation(self, label, new_label, start_id, end_id, properties={}):
        start_node = self.nodes.get(start_id)
        end_node = self.nodes.get(end_id)
        relationship = self.relationships.match((start_node, end_node)).first()
        self.graph.separate(relationship)
        relationship = Relationship(start_node, new_label, end_node)
        for key, value in properties.items():
            relationship[key] = value
        self.graph.create(relationship)
        return relationship

    def delete_relation(self, start_id, end_id):
        start_node = self.nodes.get(start_id)
        end_node = self.nodes.get(end_id)
        if start_node and end_node:
            relationship = self.relationships.match((start_node, end_node)).first()
            self.graph.separate(relationship)
            return relationship
        else:
            raise Exception

    def delete_node(self, label, id):
        node = self.graph.nodes.match(label).where("id(_) = %d" % id).first()
        if node:
            self.graph.separate(node)
            self.graph.delete(node)
        else:
            raise Exception


class Neo4jNode(object):
    # todo move the neo4j_connection here?

    # in order to facilitate the query in the frontend
    # we provide all the possible key with value with it
    def get_property_by_label(self, label):
        neo4j_session = neo4j_connection.session()

        query = 'MATCH (n:%s) UNWIND keys(n) as key \
            return key, collect(distinct n[key]) as options' % (label)

        res = neo4j_session.run(query)

        return res

    # delete node recursively, this function does not have API, test only
    def delete_node(self, node_id):
        neo4j_session = neo4j_connection.session()
        query = "MATCH (n:test_label) \
                 where id(n)=%s \
                 DETACH DELETE n" % node_id
        res = neo4j_session.run(query)

        return res


class Neo4jRelationship(object):

    # note here it is not necessary to have label and parameter
    def get_relation_with_params(self, relation_label=None,
                                 start_label=None, end_label=None,
                                 start_params=None, end_params=None, 
                                 count=False, partial=False, page_kwargs={}):
        def format_label(label):
            if(label):
                return ':'+label
            return ''

        relation_label = format_label(relation_label)
        start_label = format_label(start_label)
        end_label = format_label(end_label)

        query = 'match p=(start_node%s)-[r%s]->(end_node%s) ' % (
                start_label, relation_label,  end_label)
 
        if(isinstance(start_params, dict)):
            query += 'where'
            for key, value in start_params.items():
                if type(value) == str:
                    value = "'%s'" % value

                # id have special function
                if key == 'id':
                    query += ' Id(start_node) = {value} and'.format(value=value)
                else:
                    if partial:
                        query += ' start_node.{key} contains {value} and'.format(
                            key=key, value=value)
                    else:
                        query += ' start_node.{key} = {value} and'.format(
                            key=key, value=value)
            query = query[:-3]

        if(isinstance(end_params, dict)):
            query += 'with * where'
            for key, value in end_params.items():
                if type(value) == str:
                    value = "'%s'" % value
                # id have special function
                if key == 'id':
                    query += ' Id(end_node) = {value} and'.format(value=value)
                else:
                    if partial and value:
                        if key in ["container_id"]:
                            query += ' end_node.{key} CONTAINS {value} and'.format(
                                key=key, value=value)
                        else:
                            query += ' TOLOWER(end_node.{key}) CONTAINS TOLOWER({value}) and'.format(
                                key=key, value=value)
                    else:
                        if key in ["container_id"]:
                            query += ' end_node.{key} = {value} and'.format(
                                key=key, value=value)
                        else:
                            query += ' TOLOWER(end_node.{key}) = TOLOWER({value}) and'.format(
                                key=key, value=value)
            query = query[:-3]
        if count:
            query += 'return count(*)'
        else:
            query += 'return *'
            if page_kwargs.get("order_by"):
                order = page_kwargs['order_by']
                query += f' ORDER BY start_node.{order}'
            if page_kwargs.get("order_type"):
                order_type = page_kwargs['order_type']
                query += f' {order_type}'
            if page_kwargs.get("skip"):
                skip = page_kwargs["skip"]
                query += f' skip {skip}'
            if page_kwargs.get("limit"):
                limit = page_kwargs["limit"]
                query += f' limit {limit}'
        neo4j_session = neo4j_connection.session()
        res = neo4j_session.run(query)

        return res

    # method allow to query the nodes on other side of relation
    # also the parameter allow the none so that we can query the
    # 1-to-n, n-to-1 if start == True -> node_id-to-others
    def get_node_along_relation(self, relation_label, node_id, start=True):
        query = 'match r=(start_node)-[:%s]->(end_node) ' % relation_label

        # now start add the start node and end node condition
        if start:
            query += 'where ID(start_node)=$node_id return end_node as node'
        else:
            query += 'where ID(end_node)=$node_id return start_node as node'

        neo4j_session = neo4j_connection.session()
        res = neo4j_session.run(query, node_id=node_id)

        return res
