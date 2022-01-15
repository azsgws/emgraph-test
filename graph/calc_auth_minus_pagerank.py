import os
import json

def calc_auth_minus_pagerank(mml_version, style="dot"):
    cwd = os.getcwd()

    try:
        os.chdir("graph_attrs")
        with open(style + "_graph_" + mml_version +"_pagerank.json", "r") as f:
            graph_pagerank = json.load(f)
        with open(style + "_graph_" + mml_version +"_hits_authority.json", "r") as f:
            graph_authority = json.load(f)

    finally:
        os.chdir(cwd)

    node2pagerank = dict()
    node2hits_authority = dict()

    for i in graph_pagerank['elements']['nodes']:
        node2pagerank[i['data']['id']] = i['data']['pagerank']

    for i in graph_authority['elements']['nodes']:
        node2hits_authority[i['data']['id']] = i['data']['authority']

    node2auth_minus_pagerank = dict()
    for k in node2pagerank.keys():
        node2auth_minus_pagerank[k] = \
            node2hits_authority[k] - node2pagerank[k]

    try:
        os.chdir("result_pagerank_auth")
        with open("MML("+ mml_version +")_auth_minus_pagerank.txt", 'w') as fout:
            for k,v in sorted(node2auth_minus_pagerank.items(), key=lambda x:x[1], reverse=True):
                fout.write(f'{k} {v} \n')

    finally:
        os.chdir(cwd)