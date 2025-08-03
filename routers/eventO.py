import logging
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import and_, select
from sqlalchemy.orm import Session
from sqlalchemy.orm import selectinload
from core_system.models.maps import UserMapProgress
from core_system.models.user import User, UserData, UserTeamMember
from core_system.services.user_service import create_team
from dependencies.db import get_db
from dependencies.user import get_current_user  # 假設此函式用於驗證並取得當前使用者
from schemas.user import UpdateTeamRequest, UserTeamMemberResponse, UserCharSimpleResponse

router = APIRouter(
    prefix="/event",
    tags=["Get event"],
    responses={404: {"description": "Not found"}},
)


@router.post("/draw")
def draw_map_event(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
   pass