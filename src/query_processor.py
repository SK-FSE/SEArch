from model import model_service
from db import db_methods
import typing as tp


# backend entrypoint
# backend logic should start here
def str_to_list(s):
    if len(s) > 2:
        return s[1: -1].replace('\'', '').split(',')
    return s

def get_search_result(query: str, is_deep: bool):
    ml_model = model_service.Model()
    if is_deep:
        datasets = ml_model.get_datasets_by_query(query)
        res = {'query': query,
               'is_filter': 0,
               'total': len(datasets)}
        if len(datasets) != 0:
            hits = []
            for dataset in datasets:
                hits.append({'id': dataset[0],
                             'title': dataset[4],
                             'year': dataset[2],
                             'author': str_to_list(dataset[3]),
                             'article_piece': 'dataset_piece',
                             'dataset': dataset[1]})
            res['hits'] = hits

    else:
        articles = ml_model.get_articles_by_query(query)
        res = {'query': query,
               'is_filter': 0,
               'total': len(articles)}
        if len(articles) != 0:
            hits = []
            for article in articles:
                hits.append({'id': article[0],
                             'title': article[1],
                             'year': article[2],
                             'author': str_to_list(article[3]),
                             'article_piece': '...'.join(article[4])})
            res['hits'] = hits
    return res
