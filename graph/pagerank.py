import os
import json
import networkx as nx
import pprint

def min_max_normalization(node2value, max_val, min_val):
    node_size = dict()
    node2value_max = max(node2value.values())
    node2value_min = min(node2value.values())

    for k, v in node2value.items():
        node_size[k] = {'pagerank': 
            ((v - node2value_min) / (node2value_max - node2value_min)) * (max_val - min_val) + min_val}

    return node_size


def rank_nodes_with_pagerank(node2pagerank):
    pagerank = list(set(node2pagerank.values()))
    pagerank_sorted = sorted(pagerank, reverse=True)
    pagerank2ranking = dict()
    ranking = 0
    for v in pagerank_sorted:
        pagerank2ranking[v] = ranking
        ranking += 1

    node2ranking = dict()
    for k,v in node2pagerank.items():
        node2ranking[k] = {"ranking": pagerank2ranking[v]}

    return node2ranking


def update_pagerank_for_set_node_attribute(node2pagerank):
    a = dict()
    for k,v in node2pagerank.items():
        a[k] = {'pagerank': v}
    return a


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

def make_pagerank_graph(mml_version):
    cwd = os.getcwd()

    try:
        os.chdir("graph_attrs")
        with open("dot_graph_" + mml_version + ".json", "r") as f:
            dot_graph = json.load(f)

    finally:
        os.chdir(cwd)

    # networkxのグラフを作成
    dot_G = nx.cytoscape_graph(dot_graph)
    # 作成したグラフをもとに，pagerankを計算
    dot_node2pagerank = nx.pagerank_numpy(dot_G)
    # pagerankに順位付け
    dot_node2ranking = rank_nodes_with_pagerank(dot_node2pagerank)
    # pagerankの順位をもとにグループ分け
    dot_node2group = grouping_for_ranking(dot_node2ranking)
    # pagerankの値を正規化して，属性値'pagerank'に登録
    dot_node2pagerank = update_pagerank_for_set_node_attribute(dot_node2pagerank)
    # pagerankの値，順位をグラフの属性値として定義する
    nx.set_node_attributes(dot_G, dot_node2ranking)

    nx.set_node_attributes(dot_G, dot_node2pagerank)
    nx.set_node_attributes(dot_G, dot_node2group)

    # グラフの描画
    nx.draw_networkx(dot_G)

    dot_graph_json = nx.cytoscape_data(dot_G, attrs=None)

    try:
        os.chdir("graph_attrs")
        with open("dot_graph_" + mml_version + "_pagerank.json", "w") as f:
            f.write(json.dumps(dot_graph_json, indent=4))
        
    finally:
        os.chdir(cwd)
        

def create_node2pagerank(mml_version, create_file=False):
    cwd = os.getcwd()

    try:
        os.chdir("graph_attrs")
        with open("dot_graph_" + mml_version + ".json", "r") as f:
            dot_graph = json.load(f)

    finally:
        os.chdir(cwd)

    # networkxのグラフを作成
    G = nx.cytoscape_graph(dot_graph)
    # 作成したグラフをもとに，pagerankを計算
    node2pagerank = nx.pagerank_numpy(G)

    if create_file:
        with open("node2pagerank(" + mml_version +").txt", "w") as f:
            f.write(pprint.pformat(sorted(node2pagerank.items(), key=lambda x:x[1], reverse=True)))
    
    return node2pagerank


if __name__ == "__main__":
    create_node2pagerank("2020-06-18", True)