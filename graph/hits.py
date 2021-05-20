import os
import json
import networkx as nx


cwd = os.getcwd()

try:
    os.chdir("graph_attrs")
    with open("dot_graph_ver2.json", "r") as f:
        graph = json.load(f)

finally:
    os.chdir(cwd)

# networkxのグラフを作成
G = nx.cytoscape_graph(graph)

# 作成したグラフをもとに，hits.authoritiesを計算
hubs, authorities = nx.hits(G, max_iter = 5000, normalized = True)

# authoritiesをノードのサイズに適用する
node_size = dict()
for k, v in authorities.items():
    node_size[k] = {'node_size': v*100.0 + 150.0}
print(node_size)

# node_sizeをグラフの属性値として定義する
nx.set_node_attributes(G, node_size)

# グラフの描画
nx.draw_networkx(G)

graph_json = nx.cytoscape_data(G, attrs=None)

with open("dot_graph_ver3.json", "w") as f:
    f.write(json.dumps(graph_json))