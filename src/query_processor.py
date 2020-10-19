from model import model_service
from db_methods import get_article_date_by_ids
import typing as tp


# backend entrypoint
# backend logic should start here

def get_search_result(query: str) -> tp.List[str]:
    ml_model = model_service.Model()
    datasets = ml_model.get_datasets_by_query(query)
    if len(datasets) == 0:
        response = ['404']
    else:
        ids = [x[0] for x in datasets]
        response = []
        print(ids)
        article_dates = get_article_date_by_ids(ids)
        print(article_dates)
        for i in range(len(ids)):
            article_string = str(datasets[i][0]) + ';' + str(datasets[i][1]) + ';' + str(datasets[i][2]) \
                             + ';' + str(article_dates[i])
            response.append(article_string)
        # response = [x for x in datasets]
    return response
