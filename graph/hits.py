import os
import json
import networkx as nx
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


cwd = os.getcwd()

try:
    os.chdir("graph_attrs")
    with open("sfdp_graph.json", "r") as f:
        sfdp_graph = json.load(f)
    with open("dot_graph_ver2.json", "r") as f:
        dot_graph = json.load(f)

finally:
    os.chdir(cwd)

# networkxのグラフを作成
sfdp_G = nx.cytoscape_graph(sfdp_graph)
dot_G = nx.cytoscape_graph(dot_graph)

# 作成したグラフをもとに，hits.authoritiesを計算
sfdp_hubs, sfdp_authorities = nx.hits(sfdp_G, max_iter = 10000, normalized = True)
dot_hubs, dot_authorities = nx.hits(dot_G, max_iter = 10000, normalized = True)

# authoritiesをノードのサイズに適用する
sfdp_node2size = dict()
dot_node2size = dict()

# min_max_normalization(authorities, 1.0, 0.1)
sfdp_node2size = decide_node_size_from_authority_log(sfdp_authorities)
dot_node2size = decide_node_size_from_authority_log(dot_authorities)

sfdp_node_size = dict()
for k,v in sfdp_node2size.items():
    sfdp_node_size[k] = {'size': v}

dot_node_size = dict()
for k,v in dot_node2size.items():
    dot_node_size[k] = {'size': v}

# node_sizeをグラフの属性値として定義する
nx.set_node_attributes(sfdp_G, sfdp_node_size)
nx.set_node_attributes(dot_G, dot_node_size)

# グラフの描画
nx.draw_networkx(sfdp_G)
nx.draw_networkx(dot_G)
#fig = plt.savefig("test.png")

sfdp_graph_json = nx.cytoscape_data(sfdp_G, attrs=None)
dot_graph_json = nx.cytoscape_data(dot_G, attrs=None)

with open("sfdp_graph_ver2_hits.json", "w") as f:
    f.write(json.dumps(sfdp_graph_json))

with open("dot_graph_ver3_hits.json", "w") as f:
    f.write(json.dumps(dot_graph_json))