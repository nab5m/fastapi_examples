import uvicorn

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from routers import official_docs, api

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
app.include_router(official_docs.router, prefix="/offical/docs", tags=["offical_docs"])
app.include_router(api.v1.router, prefix="/api/v1", tags=["api_v1"])

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
