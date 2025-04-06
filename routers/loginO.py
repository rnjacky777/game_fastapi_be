from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from models.user import User
from services.auth_service import authenticate_user, AuthenticationError
from database import SessionLocal
from schemas.login import LoginRequest, Token


router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/login", response_model=Token)
async def login(form_data: LoginRequest, db: Session = Depends(get_db)):
    try:
        access_token = authenticate_user(
            db, form_data.username, form_data.password)
        return {"access_token": access_token, "token_type": "bearer"}
    except AuthenticationError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e)
        )
