from fastapi import FastAPI, Depends, HTTPException, status, Request, Form
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import SQLModel, Session, select
from .db import engine
from . import models, crud, auth
from .admin_routes import router as admin_router
from .api_football import fetch_fixtures
import os
app = FastAPI(title='FutAnalysis API')
app.include_router(admin_router)
@app.on_event('startup')
def on_startup():
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        admin = session.exec(select(models.User).where(models.User.is_admin==True)).first()
        if not admin:
            crud.create_user(session, 'admin', 'adminpass', is_admin=True)
            print('Created admin/adminpass (change in production)')
@app.post('/register')
def register(username: str = Form(...), password: str = Form(...)):
    with Session(engine) as session:
        user = session.exec(select(models.User).where(models.User.username == username)).first()
        if user:
            raise HTTPException(status_code=400, detail='User exists')
        u = crud.create_user(session, username, password)
        return {'username': u.username}
@app.post('/token')
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    with Session(engine) as session:
        user = crud.authenticate_user(session, form_data.username, form_data.password)
        if not user:
            raise HTTPException(status_code=400, detail='Bad credentials')
        token = auth.create_access_token(user.username)
        return {'access_token': token, 'token_type': 'bearer'}
@app.get('/matches')
def list_matches():
    with Session(engine) as session:
        return crud.list_matches(session)
@app.get('/matches/{match_id}')
def get_match(match_id: int):
    with Session(engine) as session:
        m = crud.get_match(session, match_id)
        if not m:
            raise HTTPException(404)
        return m
@app.post('/import/api-football')
async def import_api_football():
    try:
        data = await fetch_fixtures()
    except Exception as e:
        raise HTTPException(502, f'Failed to fetch: {e}')
    imported = 0
    with Session(engine) as session:
        for it in data.get('response', [])[:50]:
            fixture = it.get('fixture', {})
            teams = it.get('teams', {})
            home = teams.get('home', {}).get('name')
            away = teams.get('away', {}).get('name')
            title = f"{home} vs {away}"
            crud.create_match(session, title=title, competition=it.get('league',{}).get('name'), date=fixture.get('date'))
            imported += 1
    return {'imported': imported}
