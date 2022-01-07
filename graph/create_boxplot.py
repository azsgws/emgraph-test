import matplotlib.pyplot as plt
import networkx as nx
import os
import json
import random
from networkx.algorithms.cluster import generalized_degree
import math

from networkx.classes import graph

def make_generation2ancestors_from_networkx_graph(Graph_nx, node, generation=1):
    """子孫ノードを取得する．generationまでの世代の子孫ノードを取得する．

    Args:
        node: 子孫ノードを取得したいnetworkx.DiGraph.nodeオブジェクト
        generation (int, optional): [description]. Defaults to 1.
    """
    generation2ancestors = {0: [node]}
    for g in range(generation):
        ancestors = generation2ancestors[g]
        generation2ancestors[g+1] = list()
        for ancestor in ancestors:
            generation2ancestors[g+1] += list(Graph_nx.predecessors(ancestor))
    return generation2ancestors
    
def make_generation2descendants_from_networkx_graph(Graph_nx, node, generation=1):
    """祖先ノードを取得する．generationの祖先ノードのみを取得する

    Args:
        node: 祖先ノードを取得したいnetworkx.DiGraph.nodeオブジェクト
        generation (int, optional): [description]. Defaults to 1.
    """    
    generation2descendants = {0: [node]}
    for g in range(generation):
        descendants = generation2descendants[g]
        generation2descendants[g+1] = list()
        for descendant in descendants:
            generation2descendants[g+1] += list(Graph_nx.successors(descendant))
    return generation2descendants

def calc_distance_for_node_to_node(start_node_x, start_node_y, end_node_x, end_node_y):
    d = pow(start_node_x-end_node_x, 2) + pow(start_node_y-end_node_y, 2)
    return math.sqrt(d)

def get_node_x_and_y_from_graph_attrs(graph_json, node_name):
    for v in graph_json["elements"]["nodes"]:
        for w in v.values():
            if w["name"] == node_name:
                return (w["x"], w["y"])
    
def get_node_random_from_sfdp_graph(mml_version, sample_num=10):
    cwd = os.getcwd()
    try:
        os.chdir("graph_attrs")
        with open("sfdp_graph_" + mml_version + ".json", "r") as f:
            sfdp_graph = json.load(f)
    finally:
        os.chdir(cwd)
    
    Graph = nx.cytoscape_graph(sfdp_graph) # networkxのグラフを作成
    random.seed(0)
    return random.sample(Graph.nodes(), sample_num)

    
def make_generation2distance_node_to_ancestors(mml_version, node_name):
    """ノードと子孫ノードとの距離を測定する．nodeとnodeの子孫ノード(1~5世代)を取得し，
    世代別に距離を取得する．

    Args:
        node ([type]): 子孫ノードとの距離を測定したいノード
    """
    generation2distance_node_to_ancestors = dict()
    
    cwd = os.getcwd()

    try:
        os.chdir("graph_attrs")
        with open("sfdp_graph_" + mml_version + ".json", "r") as f:
            sfdp_graph = json.load(f)

    finally:
        os.chdir(cwd)

    Graph = nx.cytoscape_graph(sfdp_graph) # networkxのグラフを作成
    generation2ancestors = make_generation2ancestors_from_networkx_graph(Graph, node_name, generation=5)
    
    start_node_x, start_node_y = get_node_x_and_y_from_graph_attrs(sfdp_graph, node_name)
    for k,v in generation2ancestors.items():
        generation2distance_node_to_ancestors[k] = list()
        for n in v:
            end_node_x, end_node_y = get_node_x_and_y_from_graph_attrs(sfdp_graph, n)
            generation2distance_node_to_ancestors[k].append(
                calc_distance_for_node_to_node(start_node_x, start_node_y, end_node_x, end_node_y)
            )
    del generation2distance_node_to_ancestors[0]

    return generation2distance_node_to_ancestors

def make_generation2distance_node_to_descendants(mml_version, node_name):
    """ノードと祖先ノードとの距離を測定する．nodeとnodeの祖先ノード(1~5世代)を取得し，
    世代別に距離を取得する．

    Args:
        node ([type]): 祖先ノードとの距離を測定したいノード
    """
    generation2distance_node_to_descendants = dict()
    
    cwd = os.getcwd()

    try:
        os.chdir("graph_attrs")
        with open("sfdp_graph_" + mml_version + ".json", "r") as f:
            sfdp_graph = json.load(f)

    finally:
        os.chdir(cwd)

    Graph = nx.cytoscape_graph(sfdp_graph) # networkxのグラフを作成
    generation2descendants = make_generation2descendants_from_networkx_graph(Graph, node_name, generation=5)
    
    start_node_x, start_node_y = get_node_x_and_y_from_graph_attrs(sfdp_graph, node_name)
    for k,v in generation2descendants.items():
        generation2distance_node_to_descendants[k] = list()
        for n in v:
            end_node_x, end_node_y = get_node_x_and_y_from_graph_attrs(sfdp_graph, n)
            generation2distance_node_to_descendants[k].append(
                calc_distance_for_node_to_node(start_node_x, start_node_y, end_node_x, end_node_y)
            )
    del generation2distance_node_to_descendants[0]

    return generation2distance_node_to_descendants

def create_distance_boxplot(generation2distance, file_name="generation_and_distance"):
    plt.figure(figsize=(10,6))
    plt.boxplot(generation2distance.values(), labels=generation2distance.keys(), sym="+", showmeans=True)
    plt.savefig("research_data/box_plot/" + file_name + ".png")


if __name__ == "__main__":
    node_names = get_node_random_from_sfdp_graph("2020-06-18", sample_num=135)
    # 子孫との距離を測定
    generation2distance = dict()
    for n in node_names:
        d = make_generation2distance_node_to_ancestors("2020-06-18", n)
        for k,v in d.items():
            if not k in generation2distance.keys():
                generation2distance[k] = v
            else:
                generation2distance[k] += v
    create_distance_boxplot(generation2distance, file_name="generation_and_distance_from_node_to_ancestors")
    # 祖先との距離を測定
    generation2distance = dict()
    for n in node_names:
        d = make_generation2distance_node_to_descendants("2020-06-18", n)
        for k,v in d.items():
            if not k in generation2distance.keys():
                generation2distance[k] = v
            else:
                generation2distance[k] += v
    create_distance_boxplot(generation2distance, file_name="generation_and_distance_from_node_to_descendants")
    
    with open("research_data/box_plot/sampling_articles.json", "w") as f:
        f.write(json.dumps(node_names, indent=4))
    