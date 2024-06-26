import threading
import uvicorn

from contextlib import asynccontextmanager
from fastapi import FastAPI

from .global_roots_periodic_fetcher.LogServerDataManager import LogServerDataManager
from .routers import routes


# Create data fetcher object to start it with API, but on other thread
data_fetcher = LogServerDataManager()


# Define actions to take on API server startup and shutdown
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Run at startup: second thread with database fetcher from LogServer to Monitor
    thread = threading.Thread(target=LogServerDataManager.start_get_data_from_log_server)
    thread.start()
    yield

    # Run on shutdown: turn off second thread
    LogServerDataManager.set_turn_fetcher_on(False)
    print('Shutting down...')


# Create API app and include routers
app = FastAPI(lifespan=lifespan)
app.include_router(routes.router)


# Start server
@app.get("/")
def root():
    return {"message": "Hello World"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)
