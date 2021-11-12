import os
import sys
import json
import networkx as nx
import math

def decide_node_size_from_authority_log(authorities):
    log_val_list = list()
    node2size = dict()

    for k,v in authorities.items():
        if v:
            node2size[k] = math.log10(v)
            log_val_list.append(math.log10(v))
        # v = 0.0の処理
        else:
            node2size[k] = False

    # v = 0.0の処理
    for k,v in node2size.items():
        if not v:
            node2size[k] = min(log_val_list) - float(1)

    node2size_min = min(node2size.values())

    for k,v in node2size.items():
        node2size[k] = v - node2size_min + float(1)

    return node2size


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


def calc_hits(mml_version, auth=True):
    cwd = os.getcwd()

    try:
        os.chdir("graph_attrs")
        with open("dot_graph_" + mml_version + ".json", "r") as f:
            dot_graph = json.load(f)

    finally:
        os.chdir(cwd)

    # networkxのグラフを作成
    dot_G = nx.cytoscape_graph(dot_graph)

    # 作成したグラフをもとに，hits.authoritiesを計算
    dot_node2hub, dot_node2authority = nx.hits(dot_G, max_iter = 10000, normalized = True)

    dot_node_authority2value = dict()
    for k,v in dot_node2authority.items():
        dot_node_authority2value[k] = {'authority': v}

    # authorityを順位付け
    dot_node2ranking_authority = rank_nodes_with_value(dot_node2authority)

    dot_node_hub2value = dict()
    for k,v in dot_node2hub.items():
        dot_node_hub2value[k] = {'hub': v}

    # hubを順位付け
    dot_node2ranking_hub = rank_nodes_with_value(dot_node2hub)

    # authority,hubの順位をもとにグループ分け
    args = sys.argv

    if auth:
        print("Rank for authority")
        dot_node2group = grouping_for_ranking(dot_node2ranking_authority)
    else:
        print("Rank for hub")
        dot_node2group = grouping_for_ranking(dot_node2ranking_hub)


    # node_sizeをグラフの属性値として定義する
    if auth:
        nx.set_node_attributes(dot_G, dot_node_authority2value)
        nx.set_node_attributes(dot_G, dot_node2ranking_authority)

    else: 
        nx.set_node_attributes(dot_G, dot_node_hub2value)
        nx.set_node_attributes(dot_G, dot_node2ranking_hub)

    nx.set_node_attributes(dot_G, dot_node2group)

    # グラフの描画
    nx.draw_networkx(dot_G)

    dot_graph_json = nx.cytoscape_data(dot_G, attrs=None)

    try:
        os.chdir("graph_attrs")
        if auth:
            with open("dot_graph_" + mml_version + "_hits_authority.json", "w") as f:
                f.write(json.dumps(dot_graph_json, indent=4))
        else:
            with open("dot_graph_" + mml_version + "_hits_hub.json", "w") as f:
                f.write(json.dumps(dot_graph_json, indent=4))

    finally:
        os.chdir(cwd)