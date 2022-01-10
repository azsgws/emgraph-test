import matplotlib.pyplot as plt
import statistics
import os
import json
import re
from create_referenced_article_ranking import make_article2authority_from_graph_attrs, make_article2authority_minus_pagerank, make_article2pagerank_from_graph_attrs
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
        os.chdir("result_pagerank_auth")
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
    
def create_pagerank_and_auth_coloring_table(mml_version):
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

    node2coordinate = dict()
    pagerank = list()
    authority = list()

    for i in dot_graph_pagerank['elements']['nodes']:
        node2coordinate[i['data']['id']] = dict()
        node2coordinate[i['data']['id']]["x"] = i['data']['pagerank']
        pagerank.append(i['data']['pagerank'])

    for i in dot_graph_authority['elements']['nodes']:
        node2coordinate[i['data']['id']]["y"] = i['data']['authority']
        authority.append(i['data']['authority'])

    pagerank_median = statistics.median(pagerank)
    authority_median = statistics.median(authority)

    g1, g2, g3, g4 = list(), list(), list(), list()

    for k, v in node2coordinate.items():
        if v["x"]>pagerank_median and v["y"]>authority_median:
            g1.append(k)
        elif v["x"]<=pagerank_median and v["y"]>authority_median:
            g2.append(k)
        elif v["x"]<=pagerank_median and v["y"]<=authority_median:
            g3.append(k)
        else:  # v["x"]>pagerank_median and v["y"]<=authority_median:
            g4.append(k)

    x1, x2, x3, x4 = list(), list(), list(), list()
    y1, y2, y3, y4 = list(), list(), list(), list()

    for i in g1:
        x1.append(node2coordinate[i]["x"])
        y1.append(node2coordinate[i]["y"])
    for i in g2:
        x2.append(node2coordinate[i]["x"])
        y2.append(node2coordinate[i]["y"])
    for i in g3:
        x3.append(node2coordinate[i]["x"])
        y3.append(node2coordinate[i]["y"])
    for i in g4:
        x4.append(node2coordinate[i]["x"])
        y4.append(node2coordinate[i]["y"])
        
    plt.title("MML(" + mml_version + ") PageRank-HITS(Authority) Coloring by median")
    plt.xlabel("PageRank")
    plt.ylabel("Authority")
    plt.grid(True)

    plt.scatter(x1,y1,vmin=0.0, vmax=1.0, s=10, c='red')
    plt.scatter(x2,y2,vmin=0.0, vmax=1.0, s=10, c='blue')
    plt.scatter(x3,y3,vmin=0.0, vmax=1.0, s=10, c='yellow')
    plt.scatter(x4,y4,vmin=0.0, vmax=1.0, s=10, c='green')

    try:
        os.chdir("result_pagerank_auth")
        fig.savefig("MML(" + mml_version + ")_hub-authority-coloring-table(median).png")

    finally:
        os.chdir(cwd)

def make_article2number_of_referenced():
    cwd = os.getcwd()
    try:
        os.chdir("research_data/article2values/")
        with open("article2number_of_referenced(2020-06-18).json", "r") as f:
            article2number_of_referenced = json.load(f)
    finally:
        os.chdir(cwd)
    
    return article2number_of_referenced

def create_scattter_plot_of_number_of_referenced_and_pagerank():
    article2number_of_referenced = make_article2number_of_referenced()
    article2pagerank = make_article2pagerank_from_graph_attrs("2020-06-18")
    fig = plt.figure()

    x = list()
    y = list()
    for k, v in article2number_of_referenced.items():
        x.append(float(v))
        y.append(float(article2pagerank[k]))
        # x: number of referenced, y: PageRank
    
    plt.scatter(x, y, s=10,vmin=0.00, vmax=1.00, c='red')

    plt.title("MML(2020-06-18): number of referenced - PageRank")
    plt.xlabel("number of referenced")
    plt.ylabel("PageRank")
    plt.grid(True)

    cwd = os.getcwd()
    try:
        os.chdir("research_data/scatter_plots")
        fig.savefig("MML(2020-06-18)_number_of_referenced-PageRank.png")

    finally:
        os.chdir(cwd)

def create_scattter_plot_of_number_of_referenced_and_authority():
    article2number_of_referenced = make_article2number_of_referenced()
    article2authority = make_article2authority_from_graph_attrs("2020-06-18")
    fig = plt.figure()

    x = list()
    y = list()
    for k, v in article2number_of_referenced.items():
        x.append(float(v))
        y.append(float(article2authority[k]))
        # x: number of referenced, y: authority
    
    plt.scatter(x, y, s=10,vmin=0.00, vmax=1.00, c='red')

    plt.title("MML(2020-06-18): number of referenced - Authority")
    plt.xlabel("number of referenced")
    plt.ylabel("PageRank")
    plt.grid(True)

    cwd = os.getcwd()
    try:
        os.chdir("research_data/scatter_plots")
        fig.savefig("MML(2020-06-18)_number_of_referenced-authority.png")

    finally:
        os.chdir(cwd)

def create_scattter_plot_of_number_of_referenced_and_authority_minus_pagerank():
    article2number_of_referenced = make_article2number_of_referenced()
    article2authortiy_minus_pagerank = make_article2authority_minus_pagerank("2020-06-18")
    fig = plt.figure()

    x = list()
    y = list()
    for k, v in article2number_of_referenced.items():
        x.append(float(v))
        y.append(float(article2authortiy_minus_pagerank[k]))
        # x: number of referenced, y:  HITS-Authority minus PageRank-Authority
    
    plt.scatter(x, y, s=10,vmin=0.00, vmax=1.00, c='red')

    plt.title("MML(2020-06-18): number of referenced & HITS-Authority minus PageRank-Authority")
    plt.xlabel("number of referenced")
    plt.ylabel("HITS-Authority minus HITS-PageRank")
    plt.grid(True)

    cwd = os.getcwd()
    try:
        os.chdir("research_data/scatter_plots")
        fig.savefig("MML(2020-06-18)_number_of_referenced-authority_minus_PageRank.png")

    finally:
        os.chdir(cwd)

def create_scatter_plot_number_of_labels_and_authority_minus_pagerank():
    with open("research_data/article2values/article2number_of_inner_theorems_and_definitions.json", "r") as f:
        article2number_of_inner_theorems_and_definitions = json.load(f)
    article2authority_minus_pagerank = make_article2authority_minus_pagerank("2020-06-18")
    fig = plt.figure()

    x = list()
    y = list()
    for k, v in article2number_of_inner_theorems_and_definitions.items():
        key = re.sub(r"\.miz", "", k).upper()
        x.append(float(v))
        y.append(float(article2authority_minus_pagerank[key]))
        # x: number of label y:  HITS-Authority minus PageRank-Authority
    
    plt.scatter(x, y, s=10,vmin=0.00, vmax=1.00, c='red')

    plt.title("MML(2020-06-18): number of labels &  HITS-Authority minus PageRank-Authority")
    plt.xlabel("number of labels")
    plt.ylabel(" HITS-Authority minus PageRank-Authority")
    plt.grid(True)

    cwd = os.getcwd()
    try:
        os.chdir("research_data/scatter_plots")
        fig.savefig("MML(2020-06-18)_number_of_labels-authority_minus_PageRank.png")

    finally:
        os.chdir(cwd)

def create_scatter_plot_number_of_labels_and_pagerank():
    with open("research_data/article2values/article2number_of_inner_theorems_and_definitions.json", "r") as f:
        article2number_of_inner_theorems_and_definitions = json.load(f)
    article2pagerank = make_article2pagerank_from_graph_attrs("2020-06-18")
    fig = plt.figure()

    x = list()
    y = list()
    for k, v in article2number_of_inner_theorems_and_definitions.items():
        key = re.sub(r"\.miz", "", k).upper()
        x.append(float(v))
        y.append(float(article2pagerank[key]))
        # x: number of label y: PageRank
    
    plt.scatter(x, y, s=10,vmin=0.00, vmax=1.00, c='red')

    plt.title("MML(2020-06-18): number of labels & PageRank")
    plt.xlabel("number of labels")
    plt.ylabel("PageRank")
    plt.grid(True)

    cwd = os.getcwd()
    try:
        os.chdir("research_data/scatter_plots")
        fig.savefig("MML(2020-06-18)_number_of_labels-PageRank.png")

    finally:
        os.chdir(cwd)

def create_scatter_plot_number_of_labels_and_authority():
    with open("research_data/article2values/article2number_of_inner_theorems_and_definitions.json", "r") as f:
        article2number_of_inner_theorems_and_definitions = json.load(f)
    article2authority = make_article2authority_from_graph_attrs("2020-06-18")
    fig = plt.figure()

    x = list()
    y = list()
    for k, v in article2number_of_inner_theorems_and_definitions.items():
        key = re.sub(r"\.miz", "", k).upper()
        x.append(float(v))
        y.append(float(article2authority[key]))
        # x: number of label y: Authority
    
    plt.scatter(x, y, s=10,vmin=0.00, vmax=1.00, c='red')

    plt.title("MML(2020-06-18): number of labels & Authority")
    plt.xlabel("number of labels")
    plt.ylabel("Authority")
    plt.grid(True)

    cwd = os.getcwd()
    try:
        os.chdir("research_data/scatter_plots")
        fig.savefig("MML(2020-06-18)_number_of_labels-Authority.png")

    finally:
        os.chdir(cwd)

def create_scatter_plot_number_of_theorems_definitions_and_authority_minus_pagerank():
    with open("research_data/article2values/article2number_of_outer_theorems_and_definitions.json", "r") as f:
        article2number_of_theorems_or_definitons = json.load(f)
    article2authority_minus_pagerank = make_article2authority_minus_pagerank("2020-06-18")
    fig = plt.figure()

    x = list()
    y = list()
    for k, v in article2number_of_theorems_or_definitons.items():
        key = re.sub(r"\.miz", "", k).upper()
        x.append(float(v))
        y.append(float(article2authority_minus_pagerank[key]))
        # x: number of theorems and defintions y:  HITS-Authority minus PageRank-Authority
    
    plt.scatter(x, y, s=10,vmin=0.00, vmax=1.00, c='red')

    plt.title("MML(2020-06-18): \nnumber of theorems and definitions &  HITS-Authority minus PageRank-Authority")
    plt.xlabel("number of theorems and definitions")
    plt.ylabel(" HITS-Authority minus PageRank-Authority")
    plt.grid(True)

    cwd = os.getcwd()
    try:
        os.chdir("research_data/scatter_plots")
        fig.savefig("MML(2020-06-18)_number_of_theorems_and_definitions-authority_minus_PageRank.png")

    finally:
        os.chdir(cwd)

def create_scatter_plot_number_of_theorems_definitions_and_pagerank():
    with open("research_data/article2values/article2number_of_outer_theorems_and_definitions.json", "r") as f:
        article2number_of_theorems_or_definitons = json.load(f)
    article2pagerank = make_article2pagerank_from_graph_attrs("2020-06-18")
    fig = plt.figure()

    x = list()
    y = list()
    for k, v in article2number_of_theorems_or_definitons.items():
        key = re.sub(r"\.miz", "", k).upper()
        x.append(float(v))
        y.append(float(article2pagerank[key]))
        # x: number of theorems and defintions y: PageRank
    
    plt.scatter(x, y, s=10,vmin=0.00, vmax=1.00, c='red')

    plt.title("MML(2020-06-18): \nnumber of theorems and definitions & PageRank")
    plt.xlabel("number of theorems and definitions")
    plt.ylabel("PageRank")
    plt.grid(True)

    cwd = os.getcwd()
    try:
        os.chdir("research_data/scatter_plots")
        fig.savefig("MML(2020-06-18)_number_of_theorems_and_definitions-PageRank.png")

    finally:
        os.chdir(cwd)

def create_scatter_plot_number_of_theorems_definitions_and_authority():
    with open("research_data/article2values/article2number_of_outer_theorems_and_definitions.json", "r") as f:
        article2number_of_theorems_or_definitons = json.load(f)
    article2authority = make_article2authority_from_graph_attrs("2020-06-18")
    fig = plt.figure()

    x = list()
    y = list()
    for k, v in article2number_of_theorems_or_definitons.items():
        key = re.sub(r"\.miz", "", k).upper()
        x.append(float(v))
        y.append(float(article2authority[key]))
        # x: number of theorems and defintions y: Authority
    
    plt.scatter(x, y, s=10,vmin=0.00, vmax=1.00, c='red')

    plt.title("MML(2020-06-18): \nnumber of theorems and definitions & Authority")
    plt.xlabel("number of theorems and definitions")
    plt.ylabel("Authority")
    plt.grid(True)

    cwd = os.getcwd()
    try:
        os.chdir("research_data/scatter_plots")
        fig.savefig("MML(2020-06-18)_number_of_theorems_and_definitions-Authority.png")

    finally:
        os.chdir(cwd)

def create_scatter_plot_coupling_and_authority_minus_pagerank():
    with open("research_data/article2values/article2coupling.json", "r") as f:
        article2coupling = json.load(f)
    article2authority_minus_pagerank = make_article2authority_minus_pagerank("2020-06-18")
    fig = plt.figure()

    x = list()
    y = list()
    for k, v in article2coupling.items():
        key = re.sub(r"\.miz", "", k).upper()
        x.append(float(v))
        y.append(float(article2authority_minus_pagerank[key]))
        # x: coupoing y:  HITS-Authority minus PageRank-Authority
    
    plt.scatter(x, y, s=10,vmin=0.00, vmax=1.00, c='red')

    plt.title("MML(2020-06-18): \nCoupling &  HITS-Authority minus PageRank-Authority")
    plt.xlabel("Coupling")
    plt.ylabel(" HITS-Authority minus PageRank-Authority")
    plt.grid(True)

    cwd = os.getcwd()
    try:
        os.chdir("research_data/scatter_plots")
        fig.savefig("MML(2020-06-18)_coupling-Authority_minus_PageRank.png")

    finally:
        os.chdir(cwd)

def create_scatter_plot_coupling_and_pagerank():
    with open("research_data/article2values/article2coupling.json", "r") as f:
        article2coupling = json.load(f)
    article2pagerank = make_article2pagerank_from_graph_attrs("2020-06-18")
    fig = plt.figure()

    x = list()
    y = list()
    for k, v in article2coupling.items():
        key = re.sub(r"\.miz", "", k).upper()
        x.append(float(v))
        y.append(float(article2pagerank[key]))
        # x: coupoing y: PageRank
    
    plt.scatter(x, y, s=10,vmin=0.00, vmax=1.00, c='red')

    plt.title("MML(2020-06-18): \nCoupling & PageRank-Authority")
    plt.xlabel("Coupling")
    plt.ylabel("PageRank-Authority")
    plt.grid(True)

    cwd = os.getcwd()
    try:
        os.chdir("research_data/scatter_plots")
        fig.savefig("MML(2020-06-18)_coupling-PageRank.png")

    finally:
        os.chdir(cwd)

def create_scatter_plot_coupling_and_authority():
    with open("research_data/article2values/article2coupling.json", "r") as f:
        article2coupling = json.load(f)
    article2authority = make_article2authority_from_graph_attrs("2020-06-18")
    fig = plt.figure()

    x = list()
    y = list()
    for k, v in article2coupling.items():
        key = re.sub(r"\.miz", "", k).upper()
        x.append(float(v))
        y.append(float(article2authority[key]))
        # x: coupoing y: Authority
    
    plt.scatter(x, y, s=10,vmin=0.00, vmax=1.00, c='red')

    plt.title("MML(2020-06-18): \nCoupling & HITS-Authority")
    plt.xlabel("Coupling")
    plt.ylabel("HITS-Authority")
    plt.grid(True)

    cwd = os.getcwd()
    try:
        os.chdir("research_data/scatter_plots")
        fig.savefig("MML(2020-06-18)_coupling_and_HITS-Authority.png")

    finally:
        os.chdir(cwd)

def create_scatter_plot_cohesion_and_authority_minus_pagerank():
    with open("research_data/article2values/article2cohesion.json", "r") as f:
        article2cohesion = json.load(f)
    article2authority_minus_pagerank = make_article2authority_minus_pagerank("2020-06-18")
    fig = plt.figure()

    x = list()
    y = list()
    for k, v in article2cohesion.items():
        key = re.sub(r"\.miz", "", k).upper()
        x.append(float(v))
        y.append(float(article2authority_minus_pagerank[key]))
        # x: coupoing y:  HITS-Authority minus PageRank-Authority
    
    plt.scatter(x, y, s=10,vmin=0.00, vmax=1.00, c='red')

    plt.title("MML(2020-06-18): \nCohesion &  HITS-Authority minus PageRank-Authority")
    plt.xlabel("Cohesion")
    plt.ylabel("HITS-Authority minus PageRank-Authority")
    plt.grid(True)

    cwd = os.getcwd()
    try:
        os.chdir("research_data/scatter_plots")
        fig.savefig("MML(2020-06-18)_cohesion-Authority_minus_PageRank.png")

    finally:
        os.chdir(cwd)

def create_scatter_plot_cohesion_and_pagerank():
    with open("research_data/article2values/article2cohesion.json", "r") as f:
        article2cohesion = json.load(f)
    article2pagerank = make_article2pagerank_from_graph_attrs("2020-06-18")
    fig = plt.figure()

    x = list()
    y = list()
    for k, v in article2cohesion.items():
        key = re.sub(r"\.miz", "", k).upper()
        x.append(float(v))
        y.append(float(article2pagerank[key]))
        # x: coupoing y: PageRank
    
    plt.scatter(x, y, s=10,vmin=0.00, vmax=1.00, c='red')

    plt.title("MML(2020-06-18): \nCohesion & PageRank-Authority")
    plt.xlabel("Cohesion")
    plt.ylabel("PageRank-Authorituy")
    plt.grid(True)

    cwd = os.getcwd()
    try:
        os.chdir("research_data/scatter_plots")
        fig.savefig("MML(2020-06-18)_cohesion-PageRank.png")

    finally:
        os.chdir(cwd)

def create_scatter_plot_cohesion_and_authority():
    with open("research_data/article2values/article2cohesion.json", "r") as f:
        article2cohesion = json.load(f)
    article2authority = make_article2authority_from_graph_attrs("2020-06-18")
    fig = plt.figure()

    x = list()
    y = list()
    for k, v in article2cohesion.items():
        key = re.sub(r"\.miz", "", k).upper()
        x.append(float(v))
        y.append(float(article2authority[key]))
        # x: coupoing y: Authority
    
    plt.scatter(x, y, s=10,vmin=0.00, vmax=1.00, c='red')

    plt.title("MML(2020-06-18): \nCohesion & HITS-Authority")
    plt.xlabel("Cohesion")
    plt.ylabel("HITS-Authority")
    plt.grid(True)

    cwd = os.getcwd()
    try:
        os.chdir("research_data/scatter_plots")
        fig.savefig("MML(2020-06-18)_cohesion_and_HITS-Authority.png")

    finally:
        os.chdir(cwd)

def create_tables(mml_version):
    create_pagerank_and_auth_table(mml_version)
    create_hub_auth_table(mml_version)
    create_pagerank_and_auth_coloring_table(mml_version=mml_version)

if __name__=="__main__":
    create_scatter_plot_coupling_and_authority_minus_pagerank()
    create_scatter_plot_coupling_and_pagerank()
    create_scatter_plot_coupling_and_authority()
    create_scatter_plot_cohesion_and_authority_minus_pagerank()
    create_scatter_plot_cohesion_and_pagerank()
    create_scatter_plot_cohesion_and_authority()
