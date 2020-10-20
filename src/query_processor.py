from model import model_service
from db import db_methods
import typing as tp


# backend entrypoint
# backend logic should start here

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
                             'title': 'tmp',
                             'year': 'tmp3',
                             'author': dataset[2],
                             'article_piece': dataset[3],
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
                             'author': article[3],
                             'article_piece': '...'.join(article[4])})
            res['hits'] = hits
    return res
