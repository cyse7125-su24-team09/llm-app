from elasticsearch import Elasticsearch, helpers
from app.core.config import config
from app.services.embedding_service import get_embedding

print(f"Connecting to Elasticsearch at {config.ES_HOST_URL} with basic auth username {config.ES_USERNAME} password {config.ES_PASSWORD}") 
client = Elasticsearch(
    [config.ES_HOST_URL],
    basic_auth=(config.ES_USERNAME, config.ES_PASSWORD),
    verify_certs=False,
    ssl_show_warn=False
)
client.info()

def create_index(index_name, index_mapping):
    if client.indices.exists(index=index_name):
        client.indices.delete(index=index_name)
    client.indices.create(index=index_name, mappings=index_mapping)

def vector_search(cve_query: str):
    question_embedding = get_embedding(cve_query)
    knn = {
        "field": "embedding",
        "query_vector": question_embedding,
        "k": 10,
        "num_candidates": 150,
    }
    response = client.search(index=config.ELASTICSEARCH_INDEX, knn=knn, size=5)
    results = []
    for hit in response["hits"]["hits"]:
        id = hit["_id"]
        score = hit["_score"]
        cve_id = hit["_source"]["cve_id"]
        cve_data = hit["_source"]["cve_data"]
        result = {
            "id": id,
            "_score": score,
            "cve_id": cve_id,
            "cve_data": cve_data,
        }
        results.append(result)
    return results
