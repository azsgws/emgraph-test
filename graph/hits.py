import os
import json
import networkx as nx
import pprint
import math

def min_max_normalization(data_dict, max_val, min_val):
    node_size = dict()
    data_dict_max = max(data_dict.values())
    data_dict_min = min(data_dict.values())

    for k, v in data_dict.items():
        node_size[k] = {'size': 
            ((v - data_dict_min) / (data_dict_max - data_dict_min)) * (max_val - min_val) + min_val}
        node_size[k]['size'] *= 1500

    return node_size


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
hubs, authorities = nx.hits(G, max_iter = 10000, normalized = True)

# authoritiesをノードのサイズに適用する
node2size = dict()

#pprint.pprint(node_size)
print(min(authorities.values()))
# max authority 0.04532309683747147
# min authority 0.0000000000

# min_max_normalization(authorities, 1.0, 0.1)
log_val_list = list()

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
print(node2size_min)

for k,v in node2size.items():
    node2size[k] = v - node2size_min + float(1)

with open("node_size.txt", "w") as f:
    f.write(str(node2size))

node_size = dict()
for k,v in node2size.items():
    node_size[k] = {'size': v}

# node_sizeをグラフの属性値として定義する
nx.set_node_attributes(G, node_size)

# グラフの描画
nx.draw_networkx(G)
#fig = plt.savefig("test.png")

graph_json = nx.cytoscape_data(G, attrs=None)

with open("dot_graph_ver3_pre.json", "w") as f:
    f.write(json.dumps(graph_json))