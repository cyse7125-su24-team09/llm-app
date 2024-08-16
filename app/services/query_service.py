from app.services.elasticsearch_service import vector_search

def combined_query(query: str) -> str:
    # Retrieve relevant documents using vector search
    search_results = vector_search(query)

    # Combine the results into a single context that can be passed to the language model
    source_information = ""
    for result in search_results:
        source_information += f"CVE ID: {result.get('cve_id', 'N/A')}, CVE DATA: {result.get('cve_data', 'N/A')}\n"

    # Construct the final prompt for the language model
    combined_query_prompt = (
        f"Query: {query}\n"
        f"Continue to answer the query by using these Search Results:\n"
        f"{source_information}"
    )

    return combined_query_prompt
