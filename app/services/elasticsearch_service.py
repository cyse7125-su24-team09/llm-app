from elasticsearch import Elasticsearch, helpers
from app.core.config import config
from app.services.embedding_service import get_embedding

print(f"Connecting to Elasticsearch at {config.ES_HOST_URL} with basic auth username {config.ES_USERNAME} password {config.ES_PASSWORD}") 
try:
    client = Elasticsearch(
        [config.ES_HOST_URL],
        basic_auth=(config.ES_USERNAME, config.ES_PASSWORD),
        verify_certs=False,
        ssl_show_warn=False
    )
except Exception as e:
    print(f"Error connecting to Elasticsearch: {str(e)}")
    # Handle the error gracefully, e.g. log the error or show a user-friendly message
    # You can also raise the exception again if you want the app to crash in case of connection failure
client.info()

def vector_search(cve_query):
    question_embedding = get_embedding(cve_query)
    knn = {
        "field": "embedding",
        "query_vector": question_embedding,
        "k": 10,
        "num_candidates": 150,
    }

    response = client.search(index="cves", knn=knn, size=5)
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

    search_result = ""
    for i, result in enumerate(results, 1):
        search_result += (
            f"{i}. **CVE ID**: {result.get('cve_id', 'N/A')}\n"
            f"   **Description**: {result.get('cve_data', 'N/A')}\n\n"
        )

    return search_result