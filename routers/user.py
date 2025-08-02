import logging
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.orm import selectinload
from core_system.models.user import User, UserData, UserTeamMember
from core_system.services.user_service import create_team
from dependencies.db import get_db
from dependencies.user import get_current_user  # 假設此函式用於驗證並取得當前使用者
from schemas.user import UpdateTeamRequest, UserTeamMemberResponse, UserCharSimpleResponse

router = APIRouter(
    prefix="/user",
    tags=["User Game Data"],
    responses={404: {"description": "Not found"}},
)


def _create_team_response(team_members: List[UserTeamMember]) -> List[UserTeamMemberResponse]:
    """輔助函式，從 UserTeamMember 物件建立隊伍回應。"""
    logging.info([member.user_char.id for member in team_members])
    return [
        UserTeamMemberResponse(
            user_char_id=member.user_char.id,
            char_temp_id=member.user_char.template.id,
            name=member.user_char.template.name,
            level=member.user_char.level,
            position=member.position,
            image_sm_url=member.user_char.template.image_sm_url,
        )
        for member in team_members
    ]


@router.get("/chars", response_model=List[UserCharSimpleResponse])
def get_user_characters(
    current_user: User = Depends(get_current_user),
):
    """
    取得當前登入使用者所擁有的所有角色列表。
    """
    if not current_user.user_data:
        raise HTTPException(
            status_code=404, detail="User data not found for this user.")

    # 手動建立回應以符合簡化後的模型
    return [
        UserCharSimpleResponse(
            user_char_id=char.id,
            char_temp_id=char.char_temp_id,
            name=char.template.name,
            level=char.level,
            image_sm_url=char.template.image_sm_url,
        )
        for char in current_user.user_data.characters
    ]


@router.get("/teams", response_model=List[UserTeamMemberResponse])
def get_user_team(
    current_user: User = Depends(get_current_user),
):
    """
    取得當前登入使用者的隊伍。

    隊伍角色會依照儲存的位置排序。
    """
    if not current_user.user_data:
        raise HTTPException(
            status_code=404, detail="User data not found for this user."
        )

    return _create_team_response(current_user.user_data.team_members)


@router.post("/teams", response_model=List[UserTeamMemberResponse])
def update_user_team(
    team_data: UpdateTeamRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),  # 其 .id 可用，但不要直接用它的 relationship
):
    """
    更新當前登入使用者的隊伍。將舊隊伍完全替換為新隊伍。
    """
    # 1. 重新在這個 session 裡查出 user_data（避免 detached instance）
    stmt = (
        select(UserData)
        .join(User)
        .where(User.id == current_user.id)
        .options(
            selectinload(UserData.team_members)
        )
    )
    user_data = db.scalar(stmt)
    if not user_data:
        raise HTTPException(status_code=404, detail="User data not found for this user.")

    try:
        create_team(
            db=db,
            user_data=user_data,
            selected_char_ids=team_data.char_ids,
        )
        db.commit()
        # 不需要 refresh current_user，也不要用 current_user.user_data（它可能不是同一 session）
        # 回傳更新後的隊伍：用 user_data 裡的 team_members（這個 instance 是 session 綁定的）
        return _create_team_response(user_data.team_members)
    except ValueError as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        db.rollback()
        logging.error(f"An unexpected error occurred while updating user team: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="An internal server error occurred.")