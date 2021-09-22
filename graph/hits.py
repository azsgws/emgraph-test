import os
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


def rank_nodes_with_authority(node2authority):
    authorities = list(set(node2authority.values()))
    authorities_sorted = sorted(authorities, reverse=True)
    authority2ranking = dict()
    ranking = 0
    for v in authorities_sorted:
        authority2ranking[v] = ranking
        ranking += 1

    node2ranking = dict()
    for k,v in node2authority.items():
        node2ranking[k] = {"ranking": authority2ranking[v]}
    
    return node2ranking


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
sfdp_G = nx.cytoscape_graph(sfdp_graph)
dot_G = nx.cytoscape_graph(dot_graph)

# 作成したグラフをもとに，hits.authoritiesを計算
sfdp_hubs, sfdp_authorities = nx.hits(sfdp_G, max_iter = 10000, normalized = True)
dot_hubs, dot_authorities = nx.hits(dot_G, max_iter = 10000, normalized = True)

# authorityを順位付け
sfdp_node2ranking = rank_nodes_with_authority(sfdp_authorities)
dot_node2ranking = rank_nodes_with_authority(dot_authorities)

# authoritiesをノードのサイズに適用する
sfdp_node2authority = dict()
dot_node2authority = dict()

# min_max_normalization(authorities, 1.0, 0.1)
sfdp_node2authority = decide_node_size_from_authority_log(sfdp_authorities)
dot_node2authority = decide_node_size_from_authority_log(dot_authorities)

sfdp_node_authorities = dict()
for k,v in sfdp_node2authority.items():
    sfdp_node_authorities[k] = {'authority': v}

dot_node_authorities = dict()
for k,v in dot_node2authority.items():
    dot_node_authorities[k] = {'authority': v}

# node_sizeをグラフの属性値として定義する
nx.set_node_attributes(sfdp_G, sfdp_node_authorities)
nx.set_node_attributes(dot_G, dot_node_authorities)
nx.set_node_attributes(sfdp_G, sfdp_node2ranking)
nx.set_node_attributes(dot_G, dot_node2ranking)

# グラフの描画
nx.draw_networkx(sfdp_G)
nx.draw_networkx(dot_G)
#fig = plt.savefig("test.png")

sfdp_graph_json = nx.cytoscape_data(sfdp_G, attrs=None)
dot_graph_json = nx.cytoscape_data(dot_G, attrs=None)

try:
    os.chdir("graph_attrs")
    with open("sfdp_graph_hits.json", "w") as f:
        f.write(json.dumps(sfdp_graph_json, indent=4))

    with open("dot_graph_hits.json", "w") as f:
        f.write(json.dumps(dot_graph_json, indent=4))

finally:
    os.chdir(cwd)