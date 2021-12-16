import os
import sys
import json
import networkx as nx
import math
import pprint
from retrieve_dependency import make_miz_dependency
from create_graph import create_nodes, remove_cycle, remove_redundant_dependency, restore_removed_cycles

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


def calc_hits(mml_version, auth=True, nx_hits=True):
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
    if nx_hits:
        dot_node2hub, dot_node2authority = nx.hits(dot_G, max_iter = 10000, normalized = True)
    else:
        dot_node2hub, dot_node2authority = hits(mml_version)

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


def hits(mml_version):
    article2ref_articles = make_miz_dependency(mml_version)
    nodes = create_nodes(article2ref_articles)
    cycles = remove_cycle(nodes)
    remove_redundant_dependency(nodes)
    if cycles:
        restore_removed_cycles(nodes, cycles)

    old_node2authority = dict()
    old_node2hub = dict()
    new_node2authority = dict()
    new_node2hub = dict()

    for n in nodes:
        old_node2authority[n] = float(1)
        old_node2hub[n] = float(1)
        new_node2authority[n] = float(0)
        new_node2hub[n] = float(0)

    for _ in range(1000):
        for n in nodes:
            for s in n.sources:
                new_node2authority[n] += old_node2hub[s]
            for t in n.targets:
                new_node2hub[n] += old_node2authority[t]
        total_authority = float(sum(new_node2authority.values()))
        total_hub = float(sum(new_node2hub.values()))
        for n in nodes:
            old_node2authority[n] = new_node2authority[n]/total_authority
            old_node2hub[n] = new_node2hub[n]/total_hub
            new_node2authority[n] = float(0)
            new_node2hub[n] = float(0)
    
    for n in nodes:
        old_node2authority[n.name] = old_node2authority[n]
        old_node2hub[n.name] = old_node2hub[n]
        del old_node2authority[n]
        del old_node2hub[n]
        
    return old_node2hub, old_node2authority


def create_node2authority(mml_version, is_nx=True, create_file=False):
    cwd = os.getcwd()
    try:
        os.chdir("graph_attrs")
        with open("dot_graph_" + mml_version + ".json", "r") as f:
            dot_graph = json.load(f)
    finally:
        os.chdir(cwd)

    # networkxのグラフを作成
    G = nx.cytoscape_graph(dot_graph)
    # 作成したグラフをもとに，hits.authoritiesを計算
    if is_nx:
        _, node2authority = nx.hits(G)
        title_tail = "nx_hits"
    else:
        _, node2authority = hits(mml_version)
        title_tail = "my_hits"

    if create_file:
        with open("node2authority(" + mml_version + ")_" + title_tail + ".txt", "w") as f:
            f.write(pprint.pformat(sorted(node2authority.items(), key=lambda x:x[1], reverse=True)))

    return node2authority

if __name__ == "__main__":
    create_node2authority("2020-06-18", is_nx=False, create_file=True)