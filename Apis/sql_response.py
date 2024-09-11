from fastapi import APIRouter, HTTPException, Depends
from .jwt_helper import get_current_user
from Generate_response import generate_response
from pydantic import BaseModel

router = APIRouter()


# Define a Pydantic model for the query
class Query(BaseModel):
    query: str


@router.post("/generate_response")
async def sql_response(query: Query, current_user: dict = Depends(get_current_user)):
    """
    Handle SQL query and generate a response. Requires JWT authentication.

    Args:
        query (Query): The query to be executed.
        current_user (dict): The authenticated user from JWT token.

    Returns:
        dict: The result of the query response.
    """
    result = await generate_response(query.query)
    if result:
        return result
    else:
        raise HTTPException(status_code=404, detail="No results found")
