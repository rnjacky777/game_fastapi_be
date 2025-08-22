from collections import defaultdict
import logging
import random
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import and_, select
from sqlalchemy.orm import Session
from sqlalchemy.orm import selectinload
from core_system.models.association_tables import MapAreaEventAssociation, MapEventAssociation
from core_system.models.event import Event, EventResult
from core_system.models.maps import UserMapProgress
from core_system.models.user import User, UserData, UserTeamMember
from core_system.services.map_area_service import get_area_or_raise
from core_system.services.map_service import get_map_by_id
from core_system.services.user_service import create_team
from dependencies.db import get_db
from dependencies.user import get_current_user  # 假設此函式用於驗證並取得當前使用者
from schemas.event import EventDrawRequest, EventDrawResponse
from schemas.user import UpdateTeamRequest, UserTeamMemberResponse, UserCharSimpleResponse

router = APIRouter(
    prefix="/event",
    tags=["Get event"],
    responses={404: {"description": "Not found"}},
)



def build_event_pool(db: Session, map_id: int, map_area_id: int)->Event:
    event_weights = defaultdict(float)
    # map-level pool（示意）
    map_event_pool = get_map_by_id(db, map_id).event_associations
    area_event_pool = get_area_or_raise(db,map_id,map_area_id).event_associations
    for event in map_event_pool + area_event_pool:
        event_weights[event] += event.probability

    # 隨機抽出一個 event_id
    logging.info(f"event_weights: {event_weights}")
    chosen_event:MapAreaEventAssociation|MapEventAssociation = random.choices(
        population=list(event_weights.keys()),     # event_id 列表
        weights=list(event_weights.values()),      # 對應的機率
        k=1
    )[0]

    return chosen_event.event
def check_result(team_members: List[UserTeamMember], event_results: List[EventResult]) -> EventResult:
    for result in event_results:
        all_conditions_met = True  # 假設該 result 的條件都符合
        for condition in result.get_condition_list():
            key = condition.condition_key
            value = int(condition.condition_value)
            
            # 檢查是否有至少一個 team_member 符合條件
            if key == "hp_above":
                if not any(tm.user_char.hp > value for tm in team_members):
                    all_conditions_met = False
                    break
            elif key == "level_above":
                if not any(tm.user_char.level > value for tm in team_members):
                    all_conditions_met = False
                    break
            elif key == "speed_above":
                if not any(tm.user_char.spd > value for tm in team_members):
                    all_conditions_met = False
                    break
            else:
                # 可加其他條件，或視為不符合
                all_conditions_met = False
                break
        
        if all_conditions_met:
            return result  # 找到第一個符合全部條件的 event_result

    raise ValueError("No match result")

@router.post("/draw")
def draw_event(req: EventDrawRequest, db: Session = Depends(get_db),current_user: User = Depends(get_current_user), ):

    event = build_event_pool(db=db, map_id=req.map_id, map_area_id=req.map_area_id)
    event_logic = event.general_logic
    event_results = event_logic.event_results
    event_results.sort(key=lambda x: x.prior)
    team_members = current_user.user_data.team_members
    result = check_result(team_members, event_results)

    return {
        "name": event.name,
        "eventId": event.id,
        "eventStory": event_logic.get_story_text(),
        "resultName": result.name,
        "resultStory": result.get_story_text(),
    }
    # 1) 驗證基本狀態（是否在該 map/area）— 視需求可加行鎖/樂觀鎖
    # TODO: 驗證 user_id/user_data_id/map_id/map_area_id 合法性

    # with db.begin():
    #     # 2) 取隊伍快照
    # team = current_user.user_data.team_members

    # # 3) 合併事件池
    # pool = build_event_pool(db, req.map_id, req.map_area_id)

    # # 4) 抽事件
    # event_id = draw_weighted_event(pool)

    # # 5) 判斷結果（計算）
    # result_text, payload = evaluate_event(db, event_id, team)

    # # 6) 套用結果（寫 DB）
    # rewards, char_changes = apply_event_outcome(db, req.user_data_id, payload)

    # # 7) 取得故事文本並持久化 event_result
    # story_text = fetch_event_story_text(db, event_id)
    # event_result_id = persist_event_result(
    #     db,
    #     user_data_id=req.user_data_id,
    #     event_id=event_id,
    #     story_text=story_text,
    #     result_text=result_text,
    #     rewards=rewards,
    #     char_changes=char_changes,
    #     extra={},
    # )

    # # 8) 回傳標準化結構
    # return EventDrawResponse(
    #     success=True,
    #     result=EventAppliedResult(
    #         event_id=event_id,
    #         story_text=story_text,
    #         result_text=result_text,
    #         rewards=rewards,
    #         char_changes=char_changes,
    #         extra={"event_result_id": event_result_id},
    #     ),
    # )

