from .utils import *

def retrain_model():
    papers, f = load_data('data/')
    papers = papers.sample(200)
    train_models(papers)
    train_search_model(papers, f)


class Model:
    model = None
    __instance = None

    def __init__(self):
        if self.model is None:
            self._load_model()

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = object.__new__(cls)
        return cls.__instance

    def _load_model(self, use_mock=False):
        if use_mock:
            self.model = MockModel()
        else:
            self.model = BM25Okapi_custom(path='papers_search/')

    def get_datasets_by_query(self, query):
        return self.model.dataset_search(query)

    def get_articles_by_query(self, query):
        return self.model.paper_search(query)


class MockModel:
    def predict(self, query, datasets=False):
        if datasets:
            # dataset_id, dataset, context to show on SERP
            return [(1, 'dataset1', ['author1'], 'preview message1'),
                    (2, 'dataset2', ['author2', 'author3'],
                     'preview message2'),
                    (3, 'dataset3', [], 'preview message3'),
                    (4, 'dataset4', ['1234'], 'preview message4')]

        # article_id, article, preview_message
        return [(1, 'article1', 1992, ['author1', 'author2'], ['preview1', 'preview2']),
                (2, 'article2', 1986, [], []),
                (3, 'article3', 1112, ['author3'], ['preview3']),
                (4, 'article4', 4343, ['123'], ['12345'])]
