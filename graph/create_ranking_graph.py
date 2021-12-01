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

def create_pagerank_minus_authority_graph(mml_version):
    cwd = os.getcwd()
    try:
        os.chdir("graph_attrs")
        with open("dot_graph_" + mml_version + ".json", "r") as f:
            dot_graph = json.load(f)
    finally:
        os.chdir(cwd)

    cwd = os.getcwd()
    try:
        os.chdir("result_pagerank_hits")
        with open("MML(" + mml_version + ")_pagerank_minus_hits.txt", "r") as f:
            result_pagerank_minus_auth = f.readlines()
    finally:
        os.chdir(cwd)

    node2calc_value = dict()
    for i in result_pagerank_minus_auth:
        s = re.split(r'\s', i)
        node2calc_value[s[0]] = s[1]

    node2ranking = rank_nodes_with_value(node2calc_value)
    node2group = grouping_for_ranking(node2ranking)

    # networkxのグラフを作成
    dot_G = nx.cytoscape_graph(dot_graph)
    nx.set_node_attributes(dot_G, node2group)
    # グラフの描画
    nx.draw_networkx(dot_G)
    dot_graph_json = nx.cytoscape_data(dot_G, attrs=None)
    try:
        os.chdir("graph_attrs")
        with open("dot_graph_" + mml_version + "_pagerank_minus_authority.json", "w") as f:
            f.write(json.dumps(dot_graph_json, indent=4))
    finally:
        os.chdir(cwd)
