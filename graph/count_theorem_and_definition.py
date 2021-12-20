import os
import glob
import pprint
import json
from invest_diff_ver_article import extract_theorem_definition_and_label

def make_mizar_file_path(mml_version):
    cwd = os.getcwd()
    try:
        os.chdir("mml/" + mml_version + "/")
        miz_files = glob.glob("*.miz")  # mmlディレクトリの.mizファイルを取り出す

    finally:
        os.chdir(cwd)
    
    return miz_files

def remove_label(theorem_definition_and_labels):
    label = list()
    not_label = list()
    for word in theorem_definition_and_labels:
        if ":" in word:
            not_label.append(word)
        else:
            label.append(word)
    return label, not_label

def make_labels_and_non_labels(theorems_definitions_and_labels):
    labels = list()
    non_labels = list()
    for word in theorems_definitions_and_labels:
        if ":" in word:
            non_labels.append(word)
        else:
            labels.append(word)
    return labels, non_labels
    
def count_theorem_and_definition(miz_file_context):
    thoerem_or_definition2number = dict()
    theorems_definitions_and_labels = extract_theorem_definition_and_label(miz_file_context)
    _, non_labels = make_labels_and_non_labels(theorems_definitions_and_labels)
    for i in non_labels:
        if not i in thoerem_or_definition2number.keys():
            thoerem_or_definition2number[i] = 1
        else:
            thoerem_or_definition2number[i] += 1
    return thoerem_or_definition2number

def make_total_or_definition2number(miz_file2theorem_or_definition2number):
    total_theorem_or_definition2number = dict()
    for k1 in miz_file2theorem_or_definition2number.keys():
        for k2, v2 in miz_file2theorem_or_definition2number[k1].items():
            if not k2 in total_theorem_or_definition2number.keys():
                total_theorem_or_definition2number[k2] = v2
            else:
                total_theorem_or_definition2number[k2] += v2
    return total_theorem_or_definition2number

def calc_average_of_theorems_and_definitions(miz_file2theorems_and_definitions):
    total_theorem_or_definition2number = make_total_or_definition2number(miz_file2theorems_and_definitions)
    total_miz_file = len(miz_file2theorems_and_definitions.keys())
    total = 0
    for num in total_theorem_or_definition2number.values():
        total += num
    return total / total_miz_file

def main(mml_version):
    miz_file2theorem_or_definition2number = dict()
    mizar_file_path = make_mizar_file_path(mml_version)
    for mizar_file in mizar_file_path:
        with open(os.path.join("mml/" + mml_version + "/", mizar_file), 'rt',
                  encoding='utf-8', errors="ignore") as f:
            context = f.read()
        miz_file2theorem_or_definition2number[mizar_file] = dict()
        miz_file2theorem_or_definition2number[mizar_file] = count_theorem_and_definition(context)
    with open("article_referenced_theorems_and_definitions.json", "w") as f:
        f.write(json.dumps(miz_file2theorem_or_definition2number, indent=4))
    total_theorem_or_definition2number = make_total_or_definition2number(miz_file2theorem_or_definition2number)
    with open("th_or_def2num.txt", "w") as f:
        f.write(pprint.pformat(sorted(total_theorem_or_definition2number.items(),
                key=lambda x:x[1], reverse=True)))
        f.write("\n average: " + str(calc_average_of_theorems_and_definitions(miz_file2theorem_or_definition2number)))
    with open("th_or_def2num.json", "w") as f:
        f.write(json.dumps(total_theorem_or_definition2number, indent=4))


if __name__ == "__main__":
    main("2020-06-18")
