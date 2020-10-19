from model import model_service
from db import db_methods
import typing as tp


# backend entrypoint
# backend logic should start here

def get_search_result(query: str):
    ml_model = model_service.Model()
    articles = ml_model.get_articles_by_query(query)
    res = {'query': query,
               'is_filter': 0,
               'total': len(articles),
           }
    if len(articles) != 0:
        ids = [x[0] for x in articles]
        article_dates = db_methods.get_article_date_by_ids(ids)
        hits = []
        for article in articles:
            hits.append({'id': article[0], 'title': article[1], 'year': article[2], 'author': ', '.join(article[3]), 'article_piece': '...'.join(article[4])})
        res['hits'] = hits
    return res
