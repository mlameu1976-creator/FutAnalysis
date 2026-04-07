import os
from fastapi import APIRouter

router = APIRouter(prefix="/debug")

@router.get("/env")
def debug_env():
    return {
        "API_FOOTBALL_KEY_loaded": bool(os.getenv("API_FOOTBALL_KEY"))
    }
