# 凝集度を計算する
# 結合度は内部で参照しているtheorem,definition,schemeの数である．
import json

def make_article2number_of_inner_theorems_and_difinitions_from_json():
    with open("research_data/article2values/article2number_of_inner_theorems_and_definitions.json",
              "r", encoding='utf-8', errors='ignore') as f:
        article2number_of_inner_theorems_and_difinitions = json.load(f)
    return article2number_of_inner_theorems_and_difinitions

def make_article2number_of_inner_schemes_from_json():
    article2number_of_inner_schemes = dict()
    with open("research_data/article2values/article2number_of_schemes.json",
              "r", encoding='utf-8', errors='ignore') as f:
        article2number_of_schemes = json.load(f)
    for k in article2number_of_schemes.keys():
        article2number_of_inner_schemes[k] = article2number_of_schemes[k]["inner_reference"]
    return article2number_of_inner_schemes

def make_article2cohesion():
    article2cohesion = dict()
    article2number_of_inner_theorems_and_difinitions = \
        make_article2number_of_inner_theorems_and_difinitions_from_json()
    article2number_of_inner_schemes = make_article2number_of_inner_schemes_from_json()
    for article in article2number_of_inner_theorems_and_difinitions.keys():
        article2cohesion[article] = \
            article2number_of_inner_theorems_and_difinitions[article] + article2number_of_inner_schemes[article]
    return article2cohesion

if __name__ == "__main__":
    with open("research_data/article2values/article2cohesion.json", "w") as f:
        f.write(json.dumps(make_article2cohesion(), indent=4))
