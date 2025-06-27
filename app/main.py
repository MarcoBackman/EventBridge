import uvicorn
from fastapi import FastAPI
from contextlib import asynccontextmanager

#from app.api.v1.controller.email_controller import email
from app.api.v1.controller.slack_controller import slack_router
from app.api.v1.controller.license_controller import license_router
from app.utils.logger import setup_logging
from app.core.database import init_db
from app.core.config import settings
import logging

#logger initilization
setup_logging()
app_logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    app_logger.info("Applcation starting up...")
    #db initialization
    await init_db()
    app_logger.info("Database initialized successfully.")

    #app.include_router(email.router, prefix="/v1")
    app.include_router(slack_router, prefix="/v1")
    app.include_router(license_router, prefix="/v1")

    yield

app = FastAPI(lifespan=lifespan)

@app.get("/health")
async def read_root():
    app_logger.info("Root endpoint accessed.")
    return {"message":"Service Healthy"}

if __name__ == "__main__":
    app_logger.info("Starting Uvicorn server...")
    uvicorn.run(app, host=settings.APP_URL, port=settings.APP_PORT)
