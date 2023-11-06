from fastapi import FastAPI
from app.routers.recipes import recipes_router
from .database import database


app = FastAPI(
    summary="API de exemplo",
    title="API de exemplo2",
    description="Descrição da API de exemplo",
)

@app.get("/")
async def read_main():
    return {"msg": "Hello World"}


app.include_router(recipes_router, prefix="/api/v1", tags=["recipes"])

# Estabelece conexão com o banco de dados
@app.on_event("startup")
async def startup_event():
   await database.connect()

@app.on_event("shutdown")
async def shutdown_event():
    await database.disconnect()
