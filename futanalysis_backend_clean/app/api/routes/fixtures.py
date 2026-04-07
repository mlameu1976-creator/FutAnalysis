from fastapi import APIRouter
from app.services.fixtures_service import FixturesService

router = APIRouter(prefix="/fixtures", tags=["Fixtures"])

fixtures_service = FixturesService()

@router.get("/{fixture_id}")
def get_fixture_detail(fixture_id: int):
    return fixtures_service.get_fixture_detail(fixture_id)
