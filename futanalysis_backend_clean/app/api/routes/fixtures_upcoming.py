from fastapi import APIRouter, Query, HTTPException
from app.services.fixtures_service import FixturesService

router = APIRouter(prefix="/fixtures", tags=["Fixtures"])
service = FixturesService()

@router.get("/upcoming")
def get_upcoming_fixtures(
    league_code: str = Query(...),
    limit: int = Query(10)
):
    try:
        return service.get_upcoming_fixtures(league_code, limit)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

