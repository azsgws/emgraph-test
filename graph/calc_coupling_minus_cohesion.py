import os
import json
from calc_cohesion_minus_coupling import get_article2cohesion_from_json, get_article2coupling_from_json

def make_article2coupling_minus_cohesion_from_json():
    article2coupling_minus_cohesion = dict()
    article2coupling = get_article2coupling_from_json()
    article2cohesion = get_article2cohesion_from_json()
    for k in article2cohesion.keys():
        article2coupling_minus_cohesion[k] = \
            article2coupling[k] - article2cohesion[k]
    return article2coupling_minus_cohesion

def create_coupling_minus_cohesion_json():
    article2coupling_minus_cohesion = make_article2coupling_minus_cohesion_from_json()
    cwd = os.getcwd()
    try:
        os.chdir("research_data/article2values")
        with open("article2coupling_minus_cohesion.json", "w") as f:
            f.write(json.dumps(article2coupling_minus_cohesion, indent=4))
    finally:
        os.chdir(cwd)

def calc_average_coupling_minus_cohesion():
    article2coupling_minus_cohesion = make_article2coupling_minus_cohesion_from_json()
    total = 0.0
    for v in article2coupling_minus_cohesion.values():
        total += v
    return total / len(article2coupling_minus_cohesion.keys())

if __name__ == "__main__":
    create_coupling_minus_cohesion_json()
    print(calc_average_coupling_minus_cohesion())