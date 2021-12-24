import re
import pprint
import json
from retrieve_dependency import get_miz_files

def make_schemes(article_contents):
    file_words = re.findall(r"\w+:*|\([\w+\s*\,*\s*]+\)|\(|\)|\n|::|;|\.=|", article_contents)
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
        if re.fullmatch(r"from", word) and not is_comment:
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
        if re.search(r"\([\s\n]*.+[\s\n]*,[[\s\n]*.+[\s\n]*]+\)", scheme):
        # if re.search(r",", scheme):
            # print(scheme)
            label = re.findall(r"\([\s\n]*.+[\s\n]*,[[\s\n]*.+[\s\n]*]+\)", scheme)
            labels = label[0].split(',')
            scheme_title = re.sub(r"\([\s\n]*.+[\s\n]*,[[\s\n]*.+[\s\n]*]+\)", "", scheme)
            for i in labels:
                new_i = i.strip()
                new_i = new_i.strip('(')
                new_i = new_i.strip(')')
                new_i = new_i.strip(',')
                new_i = new_i.strip()
                new_schemes.append(scheme_title + "(" + new_i + ")")
        elif re.search(r"\([\s\n]+\w+[\s\n]*\)", scheme):
            label = re.findall(r"\([\s\n]+\w+[\s\n]*\)", scheme)
            new_label = label[0].strip()
            new_label = new_label.strip('(')
            new_label = new_label.strip(')')
            new_label = new_label.strip()
            scheme_title = re.sub(r"\([\s\n]+\w+[\s\n]*\)", "", scheme)
            new_schemes.append(scheme_title + "(" + new_label + ")")
        elif re.search(r"\([\s\n]*\w+[\s\n]+\)", scheme):
            label = re.findall(r"\([\s\n]*\w+[\s\n]+\)", scheme)
            new_label = label[0].strip()
            new_label = new_label.strip('(')
            new_label = new_label.strip(')')
            new_label = new_label.strip()
            scheme_title = re.sub(r"\([\s\n]*\w+[\s\n]+\)", "", scheme)
            new_schemes.append(scheme_title + "(" + new_label + ")")

        else:
            new_schemes.append(scheme)
    return new_schemes

def extract_schemes(article_contents):
    schemes = make_schemes(article_contents)
    schemes = separate_label(schemes)
    return schemes

if __name__ == "__main__":
    article2schemes = dict()
    articles = get_miz_files("2020-06-18")
    # for article in articles:
    #     with open("mml/2020-06-18/" + article, "r", encoding="utf-8", errors="ignore") as f:
    #         contents = f.read()
    #     article2schemes[article] = extract_schemes(contents)
    with open("mml/2020-06-18/fscirc_2.miz", "r", encoding="utf-8", errors="ignore") as f:
        contents = f.read()
    article2schemes["aofa_a01"] = extract_schemes(contents)
    
    with open("fscirc_2.json", "w") as f:
        f.write(json.dumps(article2schemes, indent=4))
    with open("fscirc_2.txt", "w") as f:
        f.write(pprint.pformat(article2schemes))