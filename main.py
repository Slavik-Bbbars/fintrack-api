from fastapi import FastAPI, HTTPException, APIRouter
from account.handlers import account_router
from finances.handlers import finance_router
import uvicorn



app = FastAPI()

app.include_router(account_router)
app.include_router(finance_router)



@app.get('/')
async def root():
    return {'message': 'sup!'}


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)