from model import model_service
from db import db_methods
import typing as tp


# backend entrypoint
# backend logic should start here

def get_search_result(query: str):
    res = {'query': query,
               'is_filter': 0,
               'total': 3,
               'hits': [
                   {'title': 'Title1', 'year': '1998', 'id': 1, 'abstract': 'text1',
                    'article_piece': 'Hello world, You\'re rock sucker.', 'author': 'author12'},
                   {'title': 'Title2', 'year': '2005', 'id': 2, 'abstract': 'text1', 'article_piece': 'Hello world, You\'re sock sucker.', 'author': 'author2'},
                   {'title': 'Title3', 'year': '2005', 'id': 3, 'abstract': 'text1', 'article_piece': 'Hello world, You\'re wok sucker.', 'author': 'author3'}]}
    return res
#     ml_model = model_service.Model()
#     datasets = ml_model.get_datasets_by_query(query)
#     if len(datasets) == 0:
#         response = ['404']
#     else:
#         ids = [x[0] for x in datasets]
#         response = []
#         [1]
#         article_dates = db_methods.get_article_date_by_ids(ids)
#         for i in range(len(ids)):
#             article_string = str(datasets[i][0]) + ';' \
#                     + str(datasets[i][1]) + ';' + str(datasets[i][2]) \
#                     + ';' + str(article_dates[i])
#             response.append(article_string)
#     return response
