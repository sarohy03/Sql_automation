from fastapi import FastAPI
from Apis import sql_response,Signin,Login,getUser

app = FastAPI()


app.include_router(sql_response.router)
app.include_router(Signin.router)
app.include_router(Login.router)
app.include_router(getUser.router)
