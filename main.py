from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from account.handlers import account_router
from finances.handlers import finance_router
import uvicorn


app = FastAPI()

# CORS — чтобы браузер мог делать запросы к API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(account_router)
app.include_router(finance_router)

# Раздаём статические файлы
app.mount("/static", StaticFiles(directory="templates"), name="static")

@app.get("/")
async def root():
    return FileResponse("templates/login.html")

@app.get("/{page}.html")
async def serve_page(page: str):
    return FileResponse(f"templates/{page}.html")


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)