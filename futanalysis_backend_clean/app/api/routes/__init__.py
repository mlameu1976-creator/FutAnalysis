from fastapi import APIRouter

from app.api.routes.internal_sync import router as internal_sync_router
from app.api.routes.internal_generate_pipeline import router as internal_pipeline_router

api_router = APIRouter()

api_router.include_router(internal_sync_router)
api_router.include_router(internal_pipeline_router)