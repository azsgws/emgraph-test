import os
import json
import networkx as nx
import re

def min_max_normalization(node2value, max_val, min_val):
    node_size = dict()
    node2value_max = max(node2value.values())
    node2value_min = min(node2value.values())

    for k, v in node2value.items():
        node_size[k] = {'pagerank': 
            ((v - node2value_min) / (node2value_max - node2value_min)) * (max_val - min_val) + min_val}

    return node_size


def make_node_to_value4nx_set_node_attributes(node2value, attribute_name):
    node2value4nx_set_node_attributes = dict()
    for k, v in node2value.items():
        node2value4nx_set_node_attributes[k] = {attribute_name: v}
    return node2value4nx_set_node_attributes


def rank_nodes_with_value(node2value):
    values = list(set(node2value.values()))
    values_sorted = sorted(values, reverse=True)
    value2ranking = dict()
    ranking = 0
    for v in values_sorted:
        value2ranking[v] = ranking
        ranking += 1

    node2ranking = dict()
    for k,v in node2value.items():
        node2ranking[k] = {"ranking": value2ranking[v]}

    return node2ranking


def grouping_for_ranking(node2ranking):
    max_ranking = 0
    for v in node2ranking.values():
        if v["ranking"] > max_ranking:
            max_ranking = v["ranking"]
    
    node2group = dict()
    for k,v in node2ranking.items():
        if v["ranking"] < max_ranking/10:
            node2group[k] = {"group": 0}
        elif v["ranking"] < max_ranking/10 * 2:
            node2group[k] = {"group": 1}
        elif v["ranking"] < max_ranking/10 * 3:
            node2group[k] = {"group": 2}
        elif v["ranking"] < max_ranking/10 * 4:
            node2group[k] = {"group": 3}
        elif v["ranking"] < max_ranking/10 * 5:
            node2group[k] = {"group": 4}
        elif v["ranking"] < max_ranking/10 * 6:
            node2group[k] = {"group": 5}
        elif v["ranking"] < max_ranking/10 * 7:
            node2group[k] = {"group": 6}
        elif v["ranking"] < max_ranking/10 * 8:
            node2group[k] = {"group": 7}
        elif v["ranking"] < max_ranking/10 * 9:
            node2group[k] = {"group": 8}
        else:
            node2group[k] = {"group": 9}
    return node2group

def create_authority_minus_pagerank_graph(mml_version):
    cwd = os.getcwd()
    try:
        os.chdir("graph_attrs")
        with open("dot_graph_" + mml_version + ".json", "r") as f:
            dot_graph = json.load(f)
    finally:
        os.chdir(cwd)

    cwd = os.getcwd()
    try:
        os.chdir("result_pagerank_auth")
        with open("MML(" + mml_version + ")_auth_minus_pagerank.txt", "r") as f:
            result_auth_minus_pagerank = f.readlines()
    finally:
        os.chdir(cwd)

    # networkxのグラフを作成
    dot_G = nx.cytoscape_graph(dot_graph)

    node2auth_minus_pagerank = dict()
    for i in result_auth_minus_pagerank:
        s = re.split(r'\s', i)
        node2auth_minus_pagerank[s[0]] = s[1]

    # ノードにauth - pagerankの値を割り当て
    node2auth_minus_pagerank4nx_set_node_attributes = \
        make_node_to_value4nx_set_node_attributes(node2auth_minus_pagerank, 'auth_minus_pagerank')
    nx.set_node_attributes(dot_G, node2auth_minus_pagerank4nx_set_node_attributes)
    # ノードにauth - pagerankのランキングを割り当て
    node2ranking = rank_nodes_with_value(node2auth_minus_pagerank)
    node2group = grouping_for_ranking(node2ranking)
    nx.set_node_attributes(dot_G, node2group)
    
    dot_graph_json = nx.cytoscape_data(dot_G, attrs=None)

    try:
        os.chdir("graph_attrs")
        with open("dot_graph_" + mml_version + "_authority_minus_pagerank.json", "w") as f:
            f.write(json.dumps(dot_graph_json, indent=4))
    finally:
        os.chdir(cwd)

if __name__=="__main__":
    import sys
    mml_version = sys.argv[1]
    create_authority_minus_pagerank_graph(mml_version)