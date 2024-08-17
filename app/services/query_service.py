from app.services.elasticsearch_service import vector_search
from app.core.config import config
import requests
import json

def generate_payload(query):
    source_information = vector_search(query)
    prompt = (
        f"### Query: {query}\n\n"
        f"### Search Results:\n{source_information}\n"
        f"### Instructions: Based on the query and the provided search results, "
        f"generate a detailed and informative answer."
    )

    return {"model": "gemma2:9b", "prompt": prompt, "stream": False}


def query_llm(query):
    url = config.LLM_SERVER_URL
    headers = {
        "Content-Type": "application/json",
    }

    payload = generate_payload(query)
    json_payload = json.dumps(payload)

    response = requests.post(url, headers=headers, data=json_payload)
    print(response)
    if response.status_code == 200:
        response_data= response.json()
        filtered_response = {
           "created_at": response_data.get("created_at"),
           "response": response_data.get("response"),
        }
        return filtered_response
    else:
        print(f"Request failed with status code {response.status_code}")
        print(f"Response: {response.text}")
        return None
    

# test_query = "What was the vulnerability in Campcodes Online Examination System?"
# test_results = generate_payload(test_query)

# print(test_results)
