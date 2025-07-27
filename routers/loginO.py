import logging

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, ConfigDict
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from core_system.services.user_service import (
    AuthenticationError,
    authenticate_user,
    create_user_with_defaults,
)
from dependencies.db import get_db  # get_db 其實可以從 dependencies.user 引入
from dependencies.user import get_current_user
from schemas.login import LoginRequest, RegisterRequest, Token
from schemas.user import UserDataResponse
from core_system.models.user import User

router = APIRouter()


# 建議為回傳的使用者資訊建立一個 Pydantic 模型
# 這樣可以避免意外洩漏敏感資料，例如 hashed_password
class UserOut(BaseModel):
    id: int
    username: str
    user_data: UserDataResponse | None = None

    model_config = ConfigDict(from_attributes=True)


@router.post("/login", response_model=Token)
def login(form_data: LoginRequest, db: Session = Depends(get_db)):
    try:
        access_token = authenticate_user(
            db, form_data.username, form_data.password)
        return {"access_token": access_token, "token_type": "bearer"}
    except AuthenticationError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e)
        )


@router.post("/register", response_model=UserOut, status_code=status.HTTP_201_CREATED)
def register(data: RegisterRequest, db: Session = Depends(get_db)):
    logging.info(f"Registration attempt for username: '{data.username}'")
    try:
        # 將三個資料庫操作封裝成一個服務層函式呼叫
        logging.info("Step 1/4: Calling create_user_with_defaults service.")
        new_user = create_user_with_defaults(
            db=db, username=data.username, password=data.password
        )
        logging.info(f"Step 2/4: Committing transaction for user '{data.username}'.")
        db.commit()  # 確保所有操作都成功後再提交

        logging.info(f"Step 3/4: Refreshing user object for '{data.username}'.")
        db.refresh(new_user)  # 刷新 new_user 物件以獲取最新的資料庫狀態

        logging.info(f"Step 4/4: Successfully registered user '{data.username}' with ID {new_user.id}.")
        return new_user
    except IntegrityError as e:
        logging.warning(f"Registration failed for username '{data.username}': Username already exists. Rolling back transaction.", exc_info=True)
        db.rollback()  # 如果發生錯誤（例如使用者名稱重複），則回滾交易
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Username already registered"
        )
    except Exception as e:
        logging.error(f"An unexpected error occurred during registration for '{data.username}'. Rolling back transaction.", exc_info=True)
        db.rollback()  # 處理其他可能的錯誤
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An internal server error occurred."
        )


# 修正後的 userinfo 端點
@router.get("/userinfo", response_model=UserOut)
def read_users_me(current_user: User = Depends(get_current_user)):
    """
    取得當前登入使用者的資訊。
    這個端點受 token 保護，可以用來驗證 token 的有效性。
    """
    # 因為 get_current_user 已經從資料庫中取得了 user 物件，
    # 我們可以直接回傳它。Pydantic 的 response_model 會自動過濾掉敏感資料。
    return current_user
