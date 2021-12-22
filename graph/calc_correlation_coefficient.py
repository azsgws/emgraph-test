import os
import pandas as pd
import json
import re
from create_table import make_article2number_of_referenced
from create_referenced_article_ranking import make_article2authority_minus_pagerank, \
    make_article2pagerank_from_graph_attrs, make_article2authority_from_graph_attrs

def calc_correlation_coefficient_number_of_referenced_and_authority_minus_pagerank():
    article2number_of_referenced = make_article2number_of_referenced()
    article2authority_minus_pagerank = make_article2authority_minus_pagerank("2020-06-18")
    
    number_of_referenced = list()
    authority_minus_pagerank = list()
    for k, v in article2number_of_referenced.items():
        number_of_referenced.append(float(v))
        authority_minus_pagerank.append(float(article2authority_minus_pagerank[k]))
        
    s1 = pd.Series(number_of_referenced)
    s2 = pd.Series(authority_minus_pagerank)

    res = s1.corr(s2)

    return res


def calc_correlation_coefficient_number_of_referenced_and_pagerank():
    article2number_of_referenced = make_article2number_of_referenced()
    article2pagerank = make_article2pagerank_from_graph_attrs("2020-06-18")
    
    number_of_referenced = list()
    pagerank = list()
    for k, v in article2number_of_referenced.items():
        number_of_referenced.append(float(v))
        pagerank.append(float(article2pagerank[k]))
        
    s1 = pd.Series(number_of_referenced)
    s2 = pd.Series(pagerank)

    res = s1.corr(s2)

    return res


def calc_correlation_coefficient_number_of_referenced_and_authority():
    article2number_of_referenced = make_article2number_of_referenced()
    article2authority = make_article2authority_from_graph_attrs("2020-06-18")
    
    number_of_referenced = list()
    authority = list()
    for k, v in article2number_of_referenced.items():
        number_of_referenced.append(float(v))
        authority.append(float(article2authority[k]))
        
    s1 = pd.Series(number_of_referenced)
    s2 = pd.Series(authority)

    res = s1.corr(s2)

    return res

def calc_correlation_coefficient_number_of_labels_and_authority_minus_pagerank():
    with open("article2number_of_labels.json", "r") as f:
        article2number_of_theorems_or_definitons = json.load(f)
    article2authority_minus_pagerank = make_article2authority_minus_pagerank("2020-06-18")
    number_of_labels = list()
    authority_minus_pagerank = list()
    for k, v in article2number_of_theorems_or_definitons.items():
        key = re.sub(r"\.miz", "", k).upper()
        number_of_labels.append(float(v))
        authority_minus_pagerank.append(float(article2authority_minus_pagerank[key]))
        
    s1 = pd.Series(number_of_labels)
    s2 = pd.Series(authority_minus_pagerank)

    res = s1.corr(s2)

    return res

def calc_correlation_coefficient_number_of_labels_and_pagerank():
    with open("article2number_of_labels.json", "r") as f:
        article2number_of_theorems_or_definitons = json.load(f)
    article2authority_minus_pagerank = make_article2pagerank_from_graph_attrs("2020-06-18")
    number_of_labels = list()
    pagerank = list()
    for k, v in article2number_of_theorems_or_definitons.items():
        key = re.sub(r"\.miz", "", k).upper()
        number_of_labels.append(float(v))
        pagerank.append(float(article2authority_minus_pagerank[key]))
        
    s1 = pd.Series(number_of_labels)
    s2 = pd.Series(pagerank)

    res = s1.corr(s2)

    return res

def calc_correlation_coefficient_number_of_labels_and_authority():
    with open("article2number_of_labels.json", "r") as f:
        article2number_of_theorems_or_definitons = json.load(f)
    article2authority = make_article2authority_from_graph_attrs("2020-06-18")
    number_of_labels = list()
    authority = list()
    for k, v in article2number_of_theorems_or_definitons.items():
        key = re.sub(r"\.miz", "", k).upper()
        number_of_labels.append(float(v))
        authority.append(float(article2authority[key]))
        
    s1 = pd.Series(number_of_labels)
    s2 = pd.Series(authority)

    res = s1.corr(s2)

    return res

def calc_correlation_coefficient_number_of_theorem_and_definiton_between_authoritiy_minus_pagerank():
    with open("article2number_of_theorems_or_defintions.json", "r") as f:
        article2number_of_theorems_or_definitons = json.load(f)
    article2authority_minus_pagerank = make_article2authority_minus_pagerank("2020-06-18")
    number_of_theorems_and_definitions = list()
    authority_minus_pagerank = list()
    for k, v in article2number_of_theorems_or_definitons.items():
        key = re.sub(r"\.miz", "", k).upper()
        number_of_theorems_and_definitions.append(float(v))
        authority_minus_pagerank.append(float(article2authority_minus_pagerank[key]))
        
    s1 = pd.Series(number_of_theorems_and_definitions)
    s2 = pd.Series(authority_minus_pagerank)

    res = s1.corr(s2)

    return res

def calc_correlation_coefficient_number_of_theorem_and_definiton_between_pagerank():
    with open("article2number_of_theorems_or_defintions.json", "r") as f:
        article2number_of_theorems_or_definitons = json.load(f)
    article2pagerank = make_article2pagerank_from_graph_attrs("2020-06-18")
    number_of_theorems_and_definitions = list()
    pagerank = list()
    for k, v in article2number_of_theorems_or_definitons.items():
        key = re.sub(r"\.miz", "", k).upper()
        number_of_theorems_and_definitions.append(float(v))
        pagerank.append(float(article2pagerank[key]))
        
    s1 = pd.Series(number_of_theorems_and_definitions)
    s2 = pd.Series(pagerank)

    res = s1.corr(s2)

    return res

def calc_correlation_coefficient_number_of_theorem_and_definiton_between_authoritiy():
    with open("article2number_of_theorems_or_defintions.json", "r") as f:
        article2number_of_theorems_or_definitons = json.load(f)
    article2authority = make_article2authority_from_graph_attrs("2020-06-18")
    number_of_theorems_and_definitions = list()
    authority = list()
    for k, v in article2number_of_theorems_or_definitons.items():
        key = re.sub(r"\.miz", "", k).upper()
        number_of_theorems_and_definitions.append(float(v))
        authority.append(float(article2authority[key]))
        
    s1 = pd.Series(number_of_theorems_and_definitions)
    s2 = pd.Series(authority)

    res = s1.corr(s2)

    return res

if __name__ == '__main__':
    res1 = calc_correlation_coefficient_number_of_referenced_and_authority_minus_pagerank()
    res2 = calc_correlation_coefficient_number_of_referenced_and_pagerank()
    res3 = calc_correlation_coefficient_number_of_referenced_and_authority()

    res4 = calc_correlation_coefficient_number_of_labels_and_authority_minus_pagerank()
    res5 = calc_correlation_coefficient_number_of_labels_and_pagerank()
    res6 = calc_correlation_coefficient_number_of_labels_and_authority()

    res7 = calc_correlation_coefficient_number_of_theorem_and_definiton_between_authoritiy_minus_pagerank()
    res8 = calc_correlation_coefficient_number_of_theorem_and_definiton_between_pagerank()
    res9 = calc_correlation_coefficient_number_of_theorem_and_definiton_between_authoritiy()

    cwd = os.getcwd()
    try:
        os.chdir("research_data/scatter_plots")
        with open("correlation_coefficient.txt", "w") as f:
            f.write("<number_of_referenced> - <authority_minus_pagerank>: " + str(res1) + "\n"
                    + "<number_of_referenced> - <pagerank>: " + str(res2) + "\n"
                    + "<number_of_referenced> - <authority>: " + str(res3) + "\n"
                    + "<number_of_labels> - <authority_minus_pagerank>: " + str(res4) + "\n"
                    + "<number_of_labels> - <pagerank>: " + str(res5) + "\n"
                    + "<number_of_labels> - <authority>: " + str(res6) + "\n"
                    + "<number_of_theorems_and_definitions> - <authority_minus_pagerank>: " + str(res7) + "\n"
                    + "<number_of_theorems_and_definitions> - <pagerank>: " + str(res8) + "\n"
                    + "<number_of_theorems_and_definitions> - <authority>: " + str(res9) + "\n")
    finally:
        os.chdir(cwd)