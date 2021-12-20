# 0. 比較するaritlce名，version(2つ)を取得
# 1. importするaritlce数を比較
# 2. importしたarticleの種類を比較
# 3. byで引用した定理の数を比較
# 4. byで引用した定理の種類を比較
# 5. proofの数
import sys
import os
import re
from retrieve_dependency import extract_articles, merge_values

def get_diff_ver_article(article, old_ver, new_ver):
    """Get aticle's text in 2-versions.

    Args:
        article ([str]): want to get article
        old_ver ([str]): old version in 2-version
        new_ver ([str]): new version in 2-version

    Returns:
        [tuple]: artilce contents in 2-version.
    """
    with open(os.path.join("mml/" + old_ver + "/", article + ".miz"), 'rt',
              encoding='utf-8', errors="ignore") as f:
        article_old_ver = f.read()
    with open(os.path.join("mml/" + new_ver + "/", article + ".miz"), 'rt',
              encoding='utf-8', errors="ignore") as f:
        article_new_ver = f.read()
    return article_old_ver, article_new_ver


def extract_environ_articles(article):
    """Extract artilce's environ part.

    Args:
        article ([str]): article content

    Returns:
        [set]: environ articles which article has articles in environ part
    """
    directive2articles = extract_articles(article)
    dependency_articles = merge_values(directive2articles, remove_keys=["vocabularies", "vocabulary"])  # vocabulary
    return dependency_articles

def count_environ_articles(article_old_ver, article_new_ver):
    """count articles in environ part

    Args:
        article_old_ver ([type]): [description]
        article_new_ver ([type]): [description]

    Returns:
        [type]: [description]
    """
    intersection, only_article_old_ver, only_article_new_ver = compare_environ_articles(article_old_ver, article_new_ver)
    return len(intersection), len(only_article_old_ver), len(only_article_new_ver)

def compare_environ_articles(article_old_ver, article_new_ver):
    """[summary]

    Args:
        article_old_ver ([type]): [description]
        article_new_ver ([type]): [description]

    Returns:
        [type]: [description]
    """
    old_article_environ = extract_environ_articles(article_old_ver)
    new_article_environ = extract_environ_articles(article_new_ver)
    intersection = old_article_environ & new_article_environ
    only_old_article = old_article_environ - new_article_environ
    only_new_article = new_article_environ - old_article_environ
    return intersection, only_old_article, only_new_article
    
def count_importing_theorems(old_article, new_article):
    old_article_theoerem_and_label = extract_theorem_definition_and_label(old_article)
    new_article_theoerem_and_label = extract_theorem_definition_and_label(new_article)
    return len(old_article_theoerem_and_label), len(new_article_theoerem_and_label)

def compare_importing_theorems_and_labels(old_article, new_article):
    old_article_theoerem_and_label = set(extract_theorem_definition_and_label(old_article))
    new_article_theoerem_and_label = set(extract_theorem_definition_and_label(new_article))
    intersection = old_article_theoerem_and_label & new_article_theoerem_and_label
    only_old_article_theorem_and_label = old_article_theoerem_and_label - new_article_theoerem_and_label
    only_new_article_theorem_and_label = new_article_theoerem_and_label - old_article_theoerem_and_label
    return intersection, only_old_article_theorem_and_label, only_new_article_theorem_and_label

def extract_theorem_definition_and_label(article):
    # 単語、改行、::、;で区切ってファイルの内容を取得
    file_words = re.findall(r"\w+:*|\n|::|;|\.=", article)
    is_comment = False
    is_theorem_or_label = False
    theorem_and_label = list()

    # mizファイルからbyで引用するtheorem,labelを取得する
    for word in file_words:
        # コメント行の場合
        if word == "::" and not is_comment:
            is_comment = True
            continue
        # コメント行の終了
        if re.search(r"\n", word) and is_comment:
            is_comment = False
        # byの検索
        if word == "by" and not is_comment:
            is_theorem_or_label = True
            continue
        # byで引用する構文の終了
        if (re.search(r";", word) or re.search(r"\.=", word)) and is_theorem_or_label:
            is_theorem_or_label = False
        # byで引用するtheorem, labelを取得
        if is_theorem_or_label and word != "\n":
            if theorem_and_label:
                if re.search(r":$|def$", theorem_and_label[-1]):
                    theorem_and_label[-1] = theorem_and_label[-1] + word
                    continue
                elif re.match(r"\d+", word):
                    theorem_and_label.append(theorem_and_label[-1] + word)
                    continue
            theorem_and_label.append(word)
        
    return theorem_and_label

def get_numnber_of_proof(old_article, new_article):
    return count_proof(old_article), count_proof(new_article)

def count_proof(article):
    # 単語、改行、::、;で区切ってファイルの内容を取得
    file_words = re.findall(r"\w+|\n|::", article)
    is_comment = False
    proof_counter = 0

    # mizファイルからbyで引用するtheorem,labelを取得する
    for word in file_words:
        # コメント行の場合
        if word == "::" and not is_comment:
            is_comment = True
            continue
        # コメント行の終了
        if re.search(r"\n", word) and is_comment:
            is_comment = False
        # コメント外でproofが出現
        if not is_comment and word == "proof":
            proof_counter += 1

    return proof_counter


def main(article, old_ver, new_ver, create_output=False):
    old_article, new_article = get_diff_ver_article(article, old_ver, new_ver)
    _, environ_only_old_article, environ_only_new_article = \
        compare_environ_articles(old_article, new_article)
    _, theorems_and_labels_only_old_article, theorems_and_labels_only_new_article = \
        compare_importing_theorems_and_labels(old_article, new_article)
    number_of_proof_in_old_article, number_of_proof_in_new_article = get_numnber_of_proof(old_article, new_article)

    if create_output:
        with open("result_comparing-" + article + ".txt", "w") as f:
            f.write(article + "\n")
            f.write(old_ver + "\t" + new_ver + "\n")
            f.write("ENVIRON \n")
            f.write("only old article \t only new article \n")
            f.write(str(len(environ_only_old_article)) + "\t" + str(len(environ_only_new_article)) + "\n")
            f.write(str(environ_only_old_article) + "\t" + str(environ_only_new_article) + "\n\n")
            f.write("THEOREM & LABEL \n")
            f.write("only old article \t only new article \n")
            f.write(str(len(theorems_and_labels_only_old_article)) + "\t" + str(len(theorems_and_labels_only_new_article)) + "\n")
            f.write(str(theorems_and_labels_only_old_article) + "\t" + str(theorems_and_labels_only_new_article) + "\n\n")
            f.write("NUMBER OF PROOF\n")
            f.write("only old article \t only new article \n")
            f.write(str(number_of_proof_in_old_article) + "\t" + str(number_of_proof_in_new_article) + "\n")
    
    return (article, len(environ_only_new_article), environ_only_new_article, len(environ_only_old_article), environ_only_old_article, 
            len(theorems_and_labels_only_new_article), theorems_and_labels_only_new_article, len(theorems_and_labels_only_old_article), theorems_and_labels_only_old_article,
            number_of_proof_in_old_article, number_of_proof_in_new_article)

if __name__ == '__main__':
    article = sys.argv[1]
    old_ver = sys.argv[2]
    new_ver = sys.argv[3]
    main(article, old_ver, new_ver, create_output=True)
