from sqlmodel import select
from .models import User, Match
from .auth import get_password_hash, verify_password
def create_user(session, username, password, is_admin=False):
    user = User(username=username, hashed_password=get_password_hash(password), is_admin=is_admin)
    session.add(user); session.commit(); session.refresh(user)
    return user
def authenticate_user(session, username, password):
    user = session.exec(select(User).where(User.username == username)).first()
    if not user: return None
    if not verify_password(password, user.hashed_password): return None
    return user
def create_match(session, **fields):
    m = Match(**fields)
    session.add(m); session.commit(); session.refresh(m)
    return m
def list_matches(session, limit=100):
    return session.exec(select(Match).limit(limit)).all()
def get_match(session, match_id):
    return session.get(Match, match_id)
def delete_match(session, match_id):
    m = session.get(Match, match_id)
    if m:
        session.delete(m); session.commit(); return True
    return False
