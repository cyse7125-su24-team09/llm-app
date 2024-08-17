from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services.query_service import query_llm

router = APIRouter()

# Define a Pydantic model for the request body
class QueryRequest(BaseModel):
    query: str

@router.post("/search/")
def vector_search(request: QueryRequest):
    try:
        # Extract the query from the request body
        query = request.query
        
        # Call the query_llm function with the query
        results = query_llm(query)
        
        # If results are not None, return them
        if results:
            return results
        else:
            raise HTTPException(status_code=500, detail="Error generating response")
    except Exception as e:
        # Handle unexpected errors
        raise HTTPException(status_code=500, detail=str(e))
