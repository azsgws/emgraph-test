import os
import json
import networkx as nx


def min_max_normalization(node2size, max_val, min_val):
    node_size = dict()
    node2size_max = max(node2size.values())
    node2size_min = min(node2size.values())

    for k, v in node2size.items():
        node_size[k] = {'size': 
            ((v - node2size_min) / (node2size_max - node2size_min)) * (max_val - min_val) + min_val}

    return node_size


cwd = os.getcwd()

try:
    os.chdir("graph_attrs")
    with open("sfdp_graph.json", "r") as f:
        sfdp_graph = json.load(f)
    with open("dot_graph.json", "r") as f:
        dot_graph = json.load(f)

finally:
    os.chdir(cwd)

# networkxのグラフを作成
dot_G = nx.cytoscape_graph(dot_graph)
sfdp_G = nx.cytoscape_graph(sfdp_graph)

# 作成したグラフをもとに，hits.authoritiesを計算
dot_node2pagerank = nx.pagerank(dot_G, max_iter=1000)
sfdp_node2pagerank = nx.pagerank(sfdp_G, max_iter=1000)

# authoritiesをノードのサイズに適用する
dot_node_size = min_max_normalization(dot_node2pagerank, 1.0, 210.0)
sfdp_node_size = min_max_normalization(sfdp_node2pagerank, 1.0, 210.0)

# node_sizeをグラフの属性値として定義する
nx.set_node_attributes(dot_G, dot_node_size)
nx.set_node_attributes(sfdp_G, dot_node_size)

# グラフの描画
nx.draw_networkx(dot_G)
nx.draw_networkx(sfdp_G)

dot_graph_json = nx.cytoscape_data(dot_G, attrs=None)
sfdp_graph_json = nx.cytoscape_data(sfdp_G, attrs=None)

try:
    os.chdir("graph_attrs")
    with open("dot_graph_pagerank.json", "w") as f:
        f.write(json.dumps(dot_graph_json))
    with open("sfdp_graph_pagerank.json", "w") as f:
        f.write(json.dumps(sfdp_graph_json))

finally:
    os.chdir(cwd)

