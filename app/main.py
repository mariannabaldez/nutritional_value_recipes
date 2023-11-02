from fastapi import FastAPI

app = FastAPI(
    summary="API de exemplo",
    title="API de exemplo2",
    description="Descrição da API de exemplo",
)

@app.get("/")
async def read_main():
    return {"msg": "Hello World"}