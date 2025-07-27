from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from core_system.models.user import User
from core_system.models.database import SessionLocal
from dependencies.user import get_current_user  # 假設此函式用於驗證並取得當前使用者
from schemas.user import UserCharResponse

router = APIRouter(
    prefix="/user",
    tags=["User Game Data"],
    responses={404: {"description": "Not found"}},
)


@router.get("/chars", response_model=List[UserCharResponse])
def get_user_characters(
    current_user: User = Depends(get_current_user),
):
    """
    取得當前登入使用者所擁有的所有角色列表。
    """
    if not current_user.user_data:
        raise HTTPException(
            status_code=404, detail="User data not found for this user.")

    # 利用 SQLAlchemy 的 relationship，直接從 user_data 存取 characters
    # Pydantic 的 from_attributes=True 會自動處理 ORM 物件到 schema 的轉換
    return current_user.user_data.characters