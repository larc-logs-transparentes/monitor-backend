from fastapi import FastAPI
from .routers import roots

# create app
app = FastAPI()
app.include_router(roots.router)


@app.get("/")
async def root():
    return {"message": "Hello World"}
