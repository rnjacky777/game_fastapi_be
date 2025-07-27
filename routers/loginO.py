from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from core_system.models.user import User
from core_system.services.user_service import add_user, authenticate_user, AuthenticationError, create_user_char, create_user_data, get_all_user
from dependencies.db import get_db
from schemas.login import LoginRequest, Token, RegisterRequest


router = APIRouter()


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


@router.post("/register")
def register(data: RegisterRequest, db: Session = Depends(get_db)):
    new_user = add_user(db=db,
                        username=data.username,
                        password=data.password)
    create_user_data(db=db,user_id=new_user.id)
    create_user_char(db=db, char_id=1, target_user_id=new_user.id)
    

    return {"message": "success"}

# 暫時用
@router.get("/userinfo")
def user_info(db: Session = Depends(get_db)):
    return {"current_map_id": "cave",
            "user_id": "12345", }
