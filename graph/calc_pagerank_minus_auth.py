import os
import json

def calc_pagerank_minus_auth(mml_version):
    cwd = os.getcwd()

    try:
        os.chdir("graph_attrs")
        with open("dot_graph_"+ mml_version +"_pagerank.json", "r") as f:
            dot_graph_pagerank = json.load(f)
        with open("dot_graph_"+ mml_version +"_hits_authority.json", "r") as f:
            dot_graph_authority = json.load(f)

    finally:
        os.chdir(cwd)

    node2pagerank = dict()
    node2hits_authority = dict()

    for i in dot_graph_pagerank['elements']['nodes']:
        node2pagerank[i['data']['id']] = i['data']['pagerank']

    for i in dot_graph_authority['elements']['nodes']:
        node2hits_authority[i['data']['id']] = i['data']['authority']

    node2pagerank_minus_auth = dict()
    for k in node2pagerank.keys():
        node2pagerank_minus_auth[k] = \
            node2pagerank[k] - node2hits_authority[k]

    try:
        os.chdir("result_pagerank_auth")
        with open("MML("+ mml_version +")_pagerank_minus_auth.txt", 'w') as fout:
            for k,v in sorted(node2pagerank_minus_auth.items(), key=lambda x:x[1]):
                fout.write(f'{k} {v} \n')

    finally:
        os.chdir(cwd)