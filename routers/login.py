from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from util.auth import verify_password, create_access_token,get_password_hash
from datetime import timedelta
from routers.loginO import Token
from fastapi import APIRouter


router = APIRouter()

fake_users_db = {
    "testuser": {
        "username": "testuser",
        "full_name": "Test User",
        "hashed_password": get_password_hash("testpass"),
    }
}

@router.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = fake_users_db.get(form_data.username)
    if not user or not verify_password(form_data.password, user["hashed_password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password"
        )
    access_token = create_access_token(
        data={"sub": user["username"]},
        expires_delta=timedelta(minutes=30)
    )
    return {"access_token": access_token, "token_type": "bearer"}