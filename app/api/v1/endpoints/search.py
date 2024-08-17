from fastapi import APIRouter
from app.core.config import config
from app.services.query_service import query_llm

router = APIRouter()

@router.get("/search/")
def vector_search(query: str):
    results = query_llm(query)
    # generated_response = generate_response_from_documents(results)
    return results
