import os
import json

def get_article2cohesion_from_json():
    cwd = os.getcwd()
    try:
        os.chdir("research_data/article2values")
        with open("article2cohesion.json", "r") as f:
            article2cohesion = json.load(f)
    finally:
        os.chdir(cwd)
    return article2cohesion

def get_article2coupling_from_json():
    cwd = os.getcwd()
    try:
        os.chdir("research_data/article2values")
        with open("article2coupling.json", "r") as f:
            article2coupling = json.load(f)
    finally:
        os.chdir(cwd)
    return article2coupling

def make_article2cohesion_minus_coupling_from_json():
    article2cohesion_minus_coupling = dict()
    article2cohesion = get_article2cohesion_from_json()
    article2coupling = get_article2coupling_from_json()
    for k in article2cohesion.keys():
        article2cohesion_minus_coupling[k] = \
            article2cohesion[k] - article2coupling[k]
    return article2cohesion_minus_coupling

def create_cohesion_minus_coupling_json():
    article2cohesion_minus_coupling = make_article2cohesion_minus_coupling_from_json()
    cwd = os.getcwd()
    try:
        os.chdir("research_data/article2values")
        with open("article2cohesion_minus_coupling.json", "w") as f:
            f.write(json.dumps(article2cohesion_minus_coupling, indent=4))
    finally:
        os.chdir(cwd)

def calc_average_cohesion_minus_coupling():
    article2cohesion_minus_coupling = make_article2cohesion_minus_coupling_from_json()
    total = 0.0
    for v in article2cohesion_minus_coupling.values():
        total += v
    return total / len(article2cohesion_minus_coupling.keys())

if __name__ == "__main__":
    create_cohesion_minus_coupling_json()
    print(calc_average_cohesion_minus_coupling())