from fastapi import APIRouter, Depends, HTTPException
from .jwt_helper import ClientResponse,client_collection,get_current_user
router = APIRouter()

@router.get("/display-name", response_model=ClientResponse)
async def get_display_name(current_user: dict = Depends(get_current_user)):
    db_client = await client_collection.find_one({"email": current_user["email"]})
    if db_client is None:
        raise HTTPException(status_code=404, detail="User not found")
    return {
        "id": str(db_client["_id"]),
        "name": db_client["name"],
        "email": db_client["email"]
    }