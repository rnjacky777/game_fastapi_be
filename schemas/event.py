from pydantic import BaseModel
from typing import List, Optional

class DrawEventRequest(BaseModel):
    map_id: int
    area_id: int  # 一起比對防竄改

class CharacterStateChange(BaseModel):
    char_id: int
    delta_hp: Optional[int]
    delta_exp: Optional[int]
    status_effects: Optional[List[str]] = []

class DrawEventResponse(BaseModel):
    event_type: str
    event_template_id: Optional[int]
    story_text: str  # 抽到的主劇情/前置
    result_text: str  # 根據 result 的回饋文
    character_changes: List[CharacterStateChange]
    extra: dict  # 例如 battle setup / loot / exploration progress