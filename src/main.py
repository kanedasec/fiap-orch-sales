import logging
from fastapi import FastAPI
from src.api.api import router as api_router
from src.core.config import settings

log = logging.getLogger(__name__)

def create_app() -> FastAPI:
    app = FastAPI(title="FIAP Orchestrator - Sales")

    @app.on_event("startup")
    async def startup_event():
        log.info("Starting fiap-orch-sales")

    app.include_router(api_router)
    return app

app = create_app()
