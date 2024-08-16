from fastapi import APIRouter
from app.core.config import config
from app.services.query_service import combined_query
from app.services.llm_service import generate_response_from_documents

router = APIRouter()

@router.get("/search/")
def vector_search(query: str):
    results = combined_query(query)
    # generated_response = generate_response_from_documents(results)
    return {results}
