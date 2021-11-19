import os
import json

def calc_hub_plus_auth(mml_version):
    cwd = os.getcwd()

    try:
        os.chdir("graph_attrs")
        with open("dot_graph_"+ mml_version +"_hits_hub.json", "r") as f:
            dot_graph_hub = json.load(f)
        with open("dot_graph_"+ mml_version +"_hits_authority.json", "r") as f:
            dot_graph_authority = json.load(f)

    finally:
        os.chdir(cwd)

    node2hub = dict()
    node2authority = dict()

    for i in dot_graph_hub['elements']['nodes']:
        node2hub[i['data']['id']] = i['data']['hub']

    for i in dot_graph_authority['elements']['nodes']:
        node2authority[i['data']['id']] = i['data']['authority']

    node2hub_plus_auth = dict()
    for k in node2hub.keys():
        node2hub_plus_auth[k] = \
            node2hub[k] + node2authority[k]

    try:
        os.chdir("result_hub_plus_authority")
        with open("MML("+ mml_version +")_hub_plus_authority.txt", 'w') as fout:
            for k,v in sorted(node2hub_plus_auth.items(), key=lambda x:x[1], reverse=True):
                fout.write(f'{k} {v} \n')

    finally:
        os.chdir(cwd)
