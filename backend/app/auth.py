from datetime import datetime, timedelta
from jose import jwt, JWTError
from passlib.context import CryptContext
import os
SECRET_KEY = os.getenv('FUT_SECRET', 'dev-secret')
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24
pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
def verify_password(plain, hashed):
    return pwd_context.verify(plain, hashed)
def get_password_hash(password):
    return pwd_context.hash(password)
def create_access_token(sub: str):
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode = {"exp": expire, "sub": sub}
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
def decode_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload.get('sub')
    except JWTError:
        return None
