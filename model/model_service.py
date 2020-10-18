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
            return [(1, 'dataset1', 'preview message1'),
                    (2, 'dataset2', 'preview message2'),
                    (3, 'dataset3', 'preview message3'),
                    (4, 'dataset4', 'preview message4')]

        # article_id, article, preview_message
        return [(1, 'article1', 'preview message1'),
                (2, 'article2', 'preview message2'),
                (3, 'article3', 'preview message3'),
                (4, 'article4', 'preview message4')]
