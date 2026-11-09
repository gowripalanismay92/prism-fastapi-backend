import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.api.router import api_router
from app.core.config import get_settings
from app.repositories.bob_csv_repository import BOBCSVRepository
from app.services import BOBService

settings = get_settings()
logging.basicConfig(level=settings.log_level.upper())
logger = logging.getLogger("prism_bob_api")


@asynccontextmanager
async def lifespan(app: FastAPI):
    repository = BOBCSVRepository(settings.data_file)
    repository.load()
    app.state.bob_repository = repository
    app.state.bob_service = BOBService(repository)
    logger.info("BOB dataset loaded: %s records", repository.record_count)
    yield


app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="Advisor-scoped Book of Business API for the Prism frontend.",
    lifespan=lifespan,
)


@app.get("/health/live", tags=["Health"])
def live():
    return {"status": "alive"}


@app.get("/health/ready", tags=["Health"])
def ready(request: Request):
    repository = getattr(request.app.state, "bob_repository", None)
    if repository is None:
        return JSONResponse(status_code=503, content={"status": "not_ready"})
    return {"status": "ready", "records_loaded": repository.record_count}


app.include_router(api_router)
