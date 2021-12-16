import json
from os import write
import pprint
import invest_diff_ver_article



if __name__ == '__main__':
    with open("research_data/displacement_in_all_version_ranking_up.json") as f:
        node2displacement_in_all_version_ranking_up = json.load(f)
    with open("research_data/displacement_in_all_version_ranking_down.json") as f:
        node2displacement_in_all_version_ranking_down = json.load(f)

    # ranking up
    sorted_node2displacement_in_all_version_ranking_up = sorted(node2displacement_in_all_version_ranking_up.items(),
                                      key=lambda x:x[1]["score"], reverse=True)
    counter = 0
    number_of_rank_in_article = 100
    total_environ_displacement = 0
    total_theorem_and_label_displacement = 0
    total_number_of_proof = 0
    with open("ranking-up.md", "w") as f:
        f.write("|         | 比較したバージョン        | 環境部のアーティクルの種類の数 | byで引用するtheorem, label | proofの数 | \n")
        f.write("|---------|-------------------------|------------------------------|---------------------------|-----------| \n")
        for t in sorted_node2displacement_in_all_version_ranking_up:
            row = invest_diff_ver_article.main(t[0].lower(), t[1]["old_ver"], t[1]["new_ver"], create_output=False)
            f.write("| " + row[0] + 
                    " | " + t[1]["old_ver"] + " and " + t[1]["new_ver"] + 
                    " | +" + str(row[1]) + ", -"+ str(row[3]) + 
                    " | +" + str(row[5]) + ", -" + str(row[7]) + 
                    " | " + str(row[10] - row[9]) + " | \n")
            total_environ_displacement += row[1]
            total_environ_displacement -= row[3]
            total_theorem_and_label_displacement += row[5]
            total_theorem_and_label_displacement += row[7]
            total_number_of_proof += (row[10] - row[9])
            if number_of_rank_in_article < counter:
                break
            else:
                counter += 1
        f.write("| AVERAGE | ***** | " + str(total_environ_displacement / number_of_rank_in_article) + 
                " | " + str(total_theorem_and_label_displacement / number_of_rank_in_article) + 
                " | " + str(total_number_of_proof / number_of_rank_in_article))
    
    # ranking down
    sorted_node2displacement_in_all_version_ranking_down = sorted(node2displacement_in_all_version_ranking_down.items(),
                                      key=lambda x:x[1]["score"], reverse=False)
    counter = 0
    number_of_rank_in_article = 100
    total_environ_displacement = 0
    total_theorem_and_label_displacement = 0
    total_number_of_proof = 0
    with open("ranking-down.md", "w") as f:
        f.write("|         | 比較したバージョン        | 環境部のアーティクルの種類の数 | byで引用するtheorem, label | proofの数 | \n")
        f.write("|---------|-------------------------|------------------------------|---------------------------|-----------| \n")
        for t in sorted_node2displacement_in_all_version_ranking_down:
            row = invest_diff_ver_article.main(t[0].lower(), t[1]["old_ver"], t[1]["new_ver"], create_output=False)
            f.write("| " + row[0] + 
                    " | " + t[1]["old_ver"] + " and " + t[1]["new_ver"] + 
                    " | +" + str(row[1]) + ", -"+ str(row[3]) + 
                    " | +" + str(row[5]) + ", -" + str(row[7]) + 
                    " | " + str(row[10] - row[9]) + " | \n")
            total_environ_displacement += row[1]
            total_environ_displacement -= row[3]
            total_theorem_and_label_displacement += row[5]
            total_theorem_and_label_displacement += row[7]
            total_number_of_proof += (row[10] - row[9])
            if number_of_rank_in_article < counter:
                break
            else:
                counter += 1
        f.write("| AVERAGE | ***** | " + str(total_environ_displacement / number_of_rank_in_article) + 
                " | " + str(total_theorem_and_label_displacement / number_of_rank_in_article) + 
                " | " + str(total_number_of_proof / number_of_rank_in_article))