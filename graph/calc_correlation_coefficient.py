import os
import pandas as pd
from create_table import make_article2number_of_referenced
from create_referenced_article_ranking import make_article2authority_minus_pagerank, \
    make_article2pagerank_from_graph_attrs, make_article2authority_from_graph_attrs

def calc_correlation_coefficient_number_of_referenced_and_authortiy_minus_pagerank():
    article2number_of_referenced = make_article2number_of_referenced()
    article2authortiy_minus_pagerank = make_article2authority_minus_pagerank("2020-06-18")
    
    number_of_referenced = list()
    authority_minus_pagerank = list()
    for k, v in article2number_of_referenced.items():
        number_of_referenced.append(float(v))
        authority_minus_pagerank.append(float(article2authortiy_minus_pagerank[k]))
        
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

if __name__ == '__main__':
    res1 = calc_correlation_coefficient_number_of_referenced_and_authortiy_minus_pagerank()
    res2 = calc_correlation_coefficient_number_of_referenced_and_pagerank()
    res3 = calc_correlation_coefficient_number_of_referenced_and_authority()

    cwd = os.getcwd()
    try:
        os.chdir("research_data/scatter_plots")
        with open("correlation_coefficient.txt", "w") as f:
            f.write("<number_of_referenced> - <authority_minus_pagerank>: " + str(res1) + "\n"
                    + "<number_of_referenced> - <pagerank>: " + str(res2) + "\n"
                    + "<number_of_referenced> - <authority>: " + str(res3) + "\n")
    finally:
        os.chdir(cwd)