from count_theorem_definition_label import make_mizar_file_path
import os
import re
import json

def make_article2num_of_theorem_definition_scheme(mml_version):
    article2num_of_theorem_definition_scheme = dict()
    mizar_files = make_mizar_file_path(mml_version)
    for mizar_file in mizar_files:
        with open(os.path.join("mml/" + mml_version + "/", mizar_file), 'rt',
                  encoding='utf-8', errors="ignore") as f:
            contents = f.read()
            article2num_of_theorem_definition_scheme[mizar_file] = \
                count_theorem_definition_scheme(contents)

    return article2num_of_theorem_definition_scheme

def count_theorem_definition_scheme(article):
    # 単語、改行、::、;で区切ってファイルの内容を取得
    file_words = re.findall(r"\w+|\n|::", article)
    is_comment = False
    key_word_counter = 0
    key_words = ["theorem", "definition", "scheme"]

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
        if not is_comment and word in key_words:
            key_word_counter += 1

    return key_word_counter

if __name__ == "__main__":
    article2num_of_theorem_definition_scheme = \
        make_article2num_of_theorem_definition_scheme("2020-06-18")
    cwd = os.getcwd()
    try:
        os.chdir("research_data/article2values/")
        with open("article2number_of_theorem_definition_scheme.json", "w") as f:
            f.write(json.dumps(article2num_of_theorem_definition_scheme, indent=4))
    finally:
        os.chdir(cwd)
