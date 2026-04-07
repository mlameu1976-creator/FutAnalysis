from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db

router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)


@router.post("/login")
def login(username: str, password: str, db: Session = Depends(get_db)):
    """
    Endpoint simples de login (placeholder).
    Ajuste depois para JWT / OAuth se desejar.
    """

    if not username or not password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Usuário e senha são obrigatórios"
        )

    # ⚠️ Login fictício (exemplo)
    if username != "admin" or password != "admin":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciais inválidas"
        )

    return {
        "access_token": "fake-token",
        "token_type": "bearer"
    }
