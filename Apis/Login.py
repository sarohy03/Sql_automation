from fastapi import APIRouter,  HTTPException
from datetime import  timedelta
from .jwt_helper import client_collection,LoginClient,Token,verify_password,ACCESS_TOKEN_EXPIRE_MINUTES,create_access_token


router = APIRouter()

@router.post("/login", response_model=Token)
async def login(client: LoginClient):
    db_client = await client_collection.find_one({"email": client.email})
    if db_client is None or not verify_password(client.password, db_client["password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"email": db_client["email"]}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}


