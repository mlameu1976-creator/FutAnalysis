from fastapi import APIRouter, UploadFile, File, HTTPException
from sqlmodel import Session, select
from .db import engine
from .crud import create_match, list_matches, delete_match
import csv, io
router = APIRouter(prefix='/admin')
@router.post('/import-csv')
async def import_csv(file: UploadFile = File(...)):
    if not file.filename.endswith('.csv'):
        raise HTTPException(400, 'CSV required')
    text = (await file.read()).decode('utf-8')
    reader = csv.DictReader(io.StringIO(text))
    imported = 0
    with Session(engine) as session:
        for row in reader:
            create_match(session, title=row.get('title') or f"{row.get('home')} vs {row.get('away')}", competition=row.get('competition'), date=row.get('date'), home=row.get('home'), away=row.get('away'), score=row.get('score'))
            imported += 1
    return {'imported': imported}
@router.get('/matches')
def admin_matches():
    with Session(engine) as session:
        return list_matches(session)
@router.delete('/matches/{match_id}')
def admin_delete(match_id: int):
    with Session(engine) as session:
        ok = delete_match(session, match_id)
        if not ok:
            raise HTTPException(404)
        return {'deleted': match_id}
