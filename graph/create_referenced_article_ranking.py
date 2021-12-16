import pprint
from retrieve_dependency import make_miz_dependency

def create_article2number_of_referenced(mizar_ver, create_file=False):
    article2dependency_article = make_miz_dependency(mizar_ver)
    article2number_of_referenced = dict()
    for dependncy_articles in article2dependency_article.values():
        for v in dependncy_articles:
            if not v in article2number_of_referenced.keys():
                article2number_of_referenced[v] = 1
            else:
                article2number_of_referenced[v] += 1

    if create_file:
        with open("article2number_of_referenced("+ mizar_ver +").txt", "w") as f:
            f.write(pprint.pformat(sorted(article2number_of_referenced.items(), key=lambda x:x[1], reverse=True)))

    return article2number_of_referenced

if __name__ == '__main__':
    create_article2number_of_referenced("2020-06-18", create_file=True)