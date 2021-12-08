from collections import defaultdict
import os
import glob
import re
import pprint

def get_mml_version():
    cwd = os.getcwd()
    try:
        os.chdir("mml")
        mml_version = glob.glob("**/", recursive=True)
    finally:
        os.chdir(cwd)
    mml_version = [re.sub("/", "", version) for version in mml_version ]
    mml_version.remove("2003-12-24")
    mml_version.remove("2005-05-31")

    return sorted(mml_version)


def get_ranking_pagerank_minus_auth_txt():
    cwd = os.getcwd()
    try:
        os.chdir("result_pagerank_auth")
        ranking_pagerank_minus_auth_txt = glob.glob('*.txt')
    finally:
        os.chdir(cwd)

    ranking_pagerank_minus_auth_txt.remove('MML(2003-12-24)_pagerank_minus_auth.txt')
    ranking_pagerank_minus_auth_txt.remove('MML(2005-05-31)_pagerank_minus_auth.txt')

    return sorted(ranking_pagerank_minus_auth_txt)


def find_article_required_refactoring():
    node2ranking_each_mml_version = dict()
    ranking_pagerank_minus_auth_txt = get_ranking_pagerank_minus_auth_txt()
    for txt in ranking_pagerank_minus_auth_txt:
        with open(os.path.join("result_pagerank_auth/", txt), 'rt',
                  encoding='utf-8', errors="ignore") as f:
            node_and_value = f.readlines()
            node2ranking = dict()
            ranking = 1
            for v in node_and_value:
                n = v.split()
                node2ranking[n[0]] = ranking
                ranking += 1
            version = txt[4:14]
        node2ranking_each_mml_version[version] = node2ranking

    node2displacement_between_two_version = calc_displacement_between_two_version(node2ranking_each_mml_version)
    with open("displacement_between_two_version.txt", "w") as f:
        f.write(pprint.pformat(sorted(node2displacement_between_two_version.items(), key=lambda x:x[1], reverse=False)))

    node2displacement_in_all_version = calc_displacement_in_all_version(node2ranking_each_mml_version)
    with open("displacement_in_all_version.txt", "w") as f:
        f.write(pprint.pformat(sorted(node2displacement_in_all_version.items(), key=lambda x:x[1], reverse=False)))


def calc_displacement_between_two_version(node2ranking_each_mml_version):
    mml_version = get_mml_version()
    node2score = dict()
    for i in range(len(mml_version)-1):
        current_version = mml_version[i]
        next_version = mml_version[i+1]
        for k,v in node2ranking_each_mml_version[current_version].items():
            if not k in node2score.keys():
                node2score[k] = 0
            if k in node2ranking_each_mml_version[next_version].keys():
                node2score[k] = min(node2score[k], v - node2ranking_each_mml_version[next_version][k])

    return node2score


def calc_displacement_in_all_version(node2ranking_each_mml_version):
    mml_version = get_mml_version()
    node2ranking = dict()
    node2score = dict()

    for i in range(len(mml_version)-1):
        current_version = mml_version[i]
        for k,v in node2ranking_each_mml_version[current_version].items():
            if not k in node2ranking.keys():
                node2ranking[k] = dict()
                node2ranking[k][0] = dict()
                node2ranking[k][0]["min"] = v
                node2ranking[k][0]["max"] = v
            else:
                key_max = max(node2ranking[k].keys())
                if v < node2ranking[k][key_max]["min"]:
                    node2ranking[k][key_max + 1] = dict()
                    node2ranking[k][key_max + 1]["min"] = v
                    node2ranking[k][key_max + 1]["max"] = v
                else:
                    node2ranking[k][key_max]["max"] = max(v, node2ranking[k][key_max]["max"])
    
    for k in node2ranking.keys():
        for i in node2ranking[k].keys():
            for j in range(i, len(node2ranking[k].keys())):
                if not k in node2score.keys():
                    node2score[k] = node2ranking[k][i]["min"] - node2ranking[k][j]["max"]
                else:
                    node2score[k] = min(node2score[k], node2ranking[k][i]["min"] - node2ranking[k][j]["max"])
    return node2score


if __name__ == '__main__':
    node2score = find_article_required_refactoring()
    