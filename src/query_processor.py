from model import model_service

# backend entrypoint
# backend logic should start here
def get_search_result(query):
    ml_model = model_service.Model()
    datasets = ml_model.get_datasets_by_query(query)
    if len(datasets) == 0:
        response = ['404']
    else:
        response = [str(x) for x in datasets[0]]
    print(response)

    return response
