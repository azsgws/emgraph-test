import matplotlib.pyplot as plt
import os
import json

def create_pagerank_and_auth_table(mml_version):
    cwd = os.getcwd()

    try:
        os.chdir("graph_attrs")
        with open("dot_graph_" + mml_version + "_pagerank.json", "r") as f:
            dot_graph_pagerank = json.load(f)
        with open("dot_graph_" + mml_version + "_hits_authority.json", "r") as f:
            dot_graph_authority = json.load(f)

    finally:
        os.chdir(cwd)

    fig = plt.figure()

    node2pagerank = dict()
    node2hits_authority = dict()

    for i in dot_graph_pagerank['elements']['nodes']:
        node2pagerank[i['data']['id']] = i['data']['pagerank']

    for i in dot_graph_authority['elements']['nodes']:
        node2hits_authority[i['data']['id']] = i['data']['authority']

    x = node2hits_authority.values()
    y = node2pagerank.values()

    plt.title("MML(" + mml_version + ") PageRank-HITS(Authority)")
    plt.xlabel("authority")
    plt.ylabel("PageRank")
    plt.grid(True)

    plt.scatter(x,y,vmin=0.0, vmax=1.0, s=10)

    try:
        os.chdir("result_pagerank_hits")
        fig.savefig("MML(" + mml_version + ")_pagerank-authority-table.png")

    finally:
        os.chdir(cwd)


def create_hub_auth_table(mml_version):
    cwd = os.getcwd()

    try:
        os.chdir("graph_attrs")
        with open("dot_graph_" + mml_version + "_hits_hub.json", "r") as f:
            dot_graph_hub = json.load(f)
        with open("dot_graph_" + mml_version + "_hits_authority.json", "r") as f:
            dot_graph_authority = json.load(f)

    finally:
        os.chdir(cwd)

    fig = plt.figure()

    node2hits_hub = dict()
    node2hits_authority = dict()

    for i in dot_graph_hub['elements']['nodes']:
        node2hits_hub[i['data']['id']] = i['data']['hub']

    for i in dot_graph_authority['elements']['nodes']:
        node2hits_authority[i['data']['id']] = i['data']['authority']

    x = node2hits_authority.values()
    y = node2hits_hub.values()

    plt.title("MML(" + mml_version + ") HITS(Hub)-HITS(Authority)")
    plt.xlabel("Authority")
    plt.ylabel("Hub")
    plt.grid(True)

    plt.scatter(x,y,vmin=0.0, vmax=1.0, s=10)

    try:
        os.chdir("result_hub_authority")
        fig.savefig("MML(" + mml_version + ")_hub-authority-table.png")

    finally:
        os.chdir(cwd)
    

def create_tables(mml_version):
    create_pagerank_and_auth_table(mml_version)
    create_hub_auth_table(mml_version)