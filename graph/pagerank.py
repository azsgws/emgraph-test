import os
import json
import networkx as nx
import math

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

# 作成したグラフをもとに，hits.authoritiesを計算
dot_node2pagerank = nx.pagerank(dot_G)
print(max(dot_node2pagerank.values()))
print(min(dot_node2pagerank.values()))

# authoritiesをノードのサイズに適用する
dot_node_size = dict()
for k,v in dot_node2pagerank.items():
    dot_node_size[k] = {'size': v*20000}

# node_sizeをグラフの属性値として定義する
nx.set_node_attributes(dot_G, dot_node_size)

# グラフの描画
nx.draw_networkx(dot_G)

dot_graph_json = nx.cytoscape_data(dot_G, attrs=None)

with open("dot_graph_pagerank.json", "w") as f:
    f.write(json.dumps(dot_graph_json))