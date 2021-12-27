import re
import pprint
import json
from retrieve_dependency import get_miz_files

def make_schemes(article_contents):
    file_words = re.findall(r"[\n\s]*from[\n\s]*|\w+:*|\([\w+\s*\,*\s*]+\)|\(|\)|\n|::|;|\.=|", article_contents)
    is_comment = False
    is_scheme = False
    schemes = str()

    # mizファイルからbyで引用するtheorem,labelを取得する
    for word in file_words:
        # コメント行の場合
        if word == "::" and not is_comment:
            is_comment = True
            continue
        # コメント行の終了
        if re.search(r"\n", word) and is_comment:
            is_comment = False
            continue
        # fromの検索
        if re.fullmatch(r"[\n\s]+from[\n\s]+", word) and not is_comment:
            is_scheme = True
            continue
        # fromで引用している箇所を取得
        if is_scheme and word != "\n" and word != "":
            if schemes:
                schemes += word
                # 終端記号が来たら終わる
                if (re.search(r";", word) or re.search(r"\.=", word)) and is_scheme:
                    is_scheme = False
                continue
            schemes = word
        
    return separate_shemes(schemes)


def separate_shemes(schemes_str):
    schemes_list = re.split(r";|\.=", schemes_str)
    schemes_list = [s for s in schemes_list if s != "" or not re.match(r"\s*\n\s*", s)]
    return schemes_list


def separate_label(schemes):
    new_schemes = list()
    for scheme in schemes:
        if "(" in scheme:
            separated_scheme = scheme.split('(')
            scheme_title = separated_scheme.pop(0)
            separated_schemes = separated_scheme.pop(0)
            separated_schemes = separated_schemes.split(',')
            for new_scheme in separated_schemes:
                new_scheme = new_scheme.strip()
                new_scheme = new_scheme.strip(')')
                new_scheme = new_scheme.strip()
                new_schemes.append(scheme_title + "(" + new_scheme + ")")
        elif scheme == "":
            pass
        else:
            new_schemes.append(scheme)
    return new_schemes

def make_article2scheme2number(article2schemes):
    article2scheme2number = dict()
    for k,schemes in article2schemes.items():
        article2scheme2number[k] = dict()
        for scheme in schemes:
            if not scheme in article2scheme2number[k].keys():
                article2scheme2number[k][scheme] = 1
            else:
                article2scheme2number[k][scheme] += 1
    return article2scheme2number

def extract_schemes(article_contents):
    schemes = make_schemes(article_contents)
    schemes = separate_label(schemes)
    return schemes

if __name__ == "__main__":
    article2schemes = dict()
    articles = get_miz_files("2020-06-18")
    for article in articles:
        with open("mml/2020-06-18/" + article, "r", encoding="utf-8", errors="ignore") as f:
            contents = f.read()
        article2schemes[article] = extract_schemes(contents)
    # with open("mml/2020-06-18/fscirc_2.miz", "r", encoding="utf-8", errors="ignore") as f:
    #     contents = f.read()
    # article2schemes["fscirc_2"] = extract_schemes(contents)
    with open("research_data/article2values/article2schemes.json", "w") as f:
        f.write(json.dumps(article2schemes, indent=4))
    with open("research_data/article2values/article2schemes.txt", "w") as f:
        f.write(pprint.pformat(article2schemes))
    article2scheme2number = make_article2scheme2number(article2schemes=article2schemes)
    with open("research_data/article2values/article2scheme2number.json", "w") as f:
        f.write(json.dumps(article2scheme2number, indent=4))
    with open("research_data/article2values/article2scheme2number.txt", "w") as f:
        f.write(pprint.pformat(article2scheme2number))
    