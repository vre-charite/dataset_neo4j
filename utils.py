# Copyright 2022 Indoc Research
# 
# Licensed under the EUPL, Version 1.2 or – as soon they
# will be approved by the European Commission - subsequent
# versions of the EUPL (the "Licence");
# You may not use this work except in compliance with the
# Licence.
# You may obtain a copy of the Licence at:
# 
# https://joinup.ec.europa.eu/collection/eupl/eupl-text-eupl-12
# 
# Unless required by applicable law or agreed to in
# writing, software distributed under the Licence is
# distributed on an "AS IS" basis,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either
# express or implied.
# See the Licence for the specific language governing
# permissions and limitations under the Licence.
# 

import json
from neo4j.graph import Node, Relationship, Path
import py2neo
from datetime import datetime
import neotime

#from . import neo4j_connection

def node_2_json(obj):
    # print(obj)
    if hasattr(obj, "id"):
        temp = {
            'id': obj.id,
            'labels': list(obj.labels)
        }
    else:
        temp = {
            'id': obj.identity,
            'labels': list(obj.labels)
        }
    # add the all the attribute all together
    temp.update(dict(zip(obj.keys(), obj.values())))

    # update the timestamp
    try:
        temp['time_lastmodified'] = str(temp['time_lastmodified'])[:19]
        temp['time_created'] = str(temp['time_created'])[:19]
    except Exception as e:
        print(e)

    return temp

def path_2_json(obj):
    result = {}
    # loop over the query result
    # print(obj.relationships)
    # for x in obj:
    #     # print("\n\n")

    # print(previous)

    current_node_tree = result
    #     print(len(x))

    #     # loop over the relationship to make into json
    for r in obj.relationships:

        start_node = node_2_json(r.start_node)
        if not start_node.get("name"):
            continue
        temp = current_node_tree.get(start_node["name"], None)
        # print(temp)
        # if we are not at the end
        if not temp:
            # print("##########################")
            current_node_tree.update({
                start_node["name"]: {
                    "id": start_node["id"],
                    "children": {}
                }
            })
        current_node_tree = current_node_tree.get(
            start_node["name"])["children"]

        end_node = node_2_json(r.end_node)
        if not end_node.get("name"):
            continue
        temp = current_node_tree.get(end_node["name"], None)
        if not temp:
            # print("##########################")
            current_node_tree.update({
                end_node["name"]: {
                    "id": end_node["id"],
                    "children": {}
                }
            })
    return result

# function will turn the neo4j query result of dataset
# and transform into dataset json object
# the input should be <Noe4j.Record> output will be flattend data in record
# please note here all the node should name as node in return
# all the path should name as p in return
def neo4j_obj_2_json(query_record):

    def make_json_by_type(obj):
        if type(obj) == Node:
            return node_2_json(obj)
        elif type(obj) == Path:
            return path_2_json(obj)
        else:
            # note here relationship is more genetic
            # if the relation give ()-[PARENT]->() the return
            # will be <abc.PARENT> so I use else with try to catch it
            try:
                relation = {"type": obj.type}
                if hasattr(obj, "_properties"):
                    for key, value in obj._properties.items():
                        relation[key] = value
                return relation
            except Exception as e:
                return None

    result = {}
    # print(query_record)
    for key, value in query_record.items():
        result.update({key: make_json_by_type(value)})

    # print(result)

    return result


# this function will cleanup the all the testing data named contains
# "test% so this is the testing naming convension
#def cleanup():
#    neo4j_session = neo4j_connection.session()
#
#    query = "match (n) where n.name contains 'test' delete n"
#
#    res = neo4j_session.run(query)
