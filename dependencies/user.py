# app/dependencies/user.py

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from pydantic import BaseModel
from sqlalchemy.orm import Session, joinedload, selectinload
from core_system.models.database import SessionLocal
from core_system.models.user import User, UserData, UserChar
from core_system.config import SECRET_KEY, ALGORITHM


# tokenUrl 應該指向你登入 API 的完整相對路徑
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")

class TokenData(BaseModel):
    id: int | None = None


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        # 解碼 JWT
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        # 從 payload 中取得 user_id (subject)
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
        token_data = TokenData(id=int(user_id))
    except (JWTError, ValueError):
        raise credentials_exception

    # 預先載入 (Eager Loading) 關聯資料，以避免 DetachedInstanceError
    # 並透過單一查詢提升效能，避免 N+1 問題。
    # - joinedload: 用於 one-to-one 或 many-to-one (User -> UserData)
    # - selectinload: 用於 one-to-many (UserData -> characters)
    user = (
        db.query(User)
        .options(
            joinedload(User.user_data).options(
                selectinload(UserData.characters).options(
                    joinedload(UserChar.template)  # 同時載入角色模板資訊
                )
            )
        )
        .filter(User.id == token_data.id)
        .first()
    )
    if user is None:
        raise credentials_exception

    return user
