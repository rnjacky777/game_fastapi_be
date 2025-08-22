from pydantic import BaseModel, Field
from typing import List, Optional


class EventDrawRequest(BaseModel):
    map_id: int = Field(..., description="所在地圖 ID")
    map_area_id: int = Field(..., description="所在地圖區域 ID")


class ItemReward(BaseModel):

    item_id: int
    qty: int = 1


class CharacterDelta(BaseModel):

    char_id: int
    hp_delta: int = 0
    mp_delta: int = 0
    atk_delta: int = 0
    def_delta: int = 0
    spd_delta: int = 0
    # 其他狀態變化...


class EventAppliedResult(BaseModel):

    event_id: int
    story_text: str
    result_text: str
    rewards: List[ItemReward] = []
    char_changes: List[CharacterDelta] = []
    # 其他：例如探索度變化、觸發後續事件 id 等


class EventDrawResponse(BaseModel):

    success: bool
    result: Optional[EventAppliedResult] = None
    message: Optional[str] = None
