from fastapi import FastAPI

from .db_manager.db_connection import get_db_client
from .routers import roots

# create app and include routers
app = FastAPI()
app.include_router(roots.router)


# Start server
@app.get("/")
async def root():
    return {"message": "Hello World"}


# When ending FastAPI, close db connection
@app.on_event("shutdown")
async def shutdown_event():
    client = get_db_client()
    client.close()
