import joblib


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

    def _load_model(self, use_mock=True):
        if use_mock:
            self.model = MockModel()

        else:
            self.model = joblib.load('model_name')

    def get_datasets_by_query(self, query):
        return self.model.predict(query, datasets=True)

    def get_articles_by_query(self, query):
        return self.model.predict(query, datasets=False)


class MockModel:
    def predict(self, query, datasets=False):
        if datasets:
            # dataset_id, dataset, context to show on SERP
            return [(1, 1985, ['author1'], 'preview message1'),
                    (2, 1342, ['author2', 'author3'], 'preview message2'),
                    (3, 1998, [], 'preview message3'),
                    (4, 1753, ['1234'], 'preview message4')]

        # article_id, article, preview_message
        return [(1, 'article1', 1992, ['author1', 'author2'], ['preview1', 'preview2']),
                (2, 'article2', 1986, [], []),
                (3, 'article3', 1112, ['author3'], ['preview3']),
                (4, 'article4', 4343, ['123'], ['12345'])]
