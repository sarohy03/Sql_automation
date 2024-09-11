from fastapi import  HTTPException, routing

# from jwt_helper import ClientCreate,ClientResponse,client_collection,get_password_hash
from .jwt_helper import ClientCreate,ClientResponse,client_collection,get_password_hash
router = routing.APIRouter()

# Routes
@router.post("/signup", response_model=ClientResponse)
async def signup(client: ClientCreate):
    db_client = await client_collection.find_one({"email": client.email})
    if db_client:
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed_password = get_password_hash(client.password)
    new_client = {
        "name": client.name,
        "email": client.email,
        "password": hashed_password
    }
    result = await client_collection.insert_one(new_client)
    return {**new_client, "id": str(result.inserted_id)}