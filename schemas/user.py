from typing import List, Optional
from pydantic import BaseModel, Field, ConfigDict, model_validator, root_validator
from .char import CharTempBase


class MapNameResponse(BaseModel):
    """用於 API 回應的地圖名稱"""
    name: str
    model_config = ConfigDict(from_attributes=True)


class AreaNameResponse(BaseModel):
    """用於 API 回應的區域名稱"""
    name: str
    model_config = ConfigDict(from_attributes=True)


class UserDataResponse(BaseModel):
    """用於 API 回應的使用者遊戲資料"""
    money: int
    # 透過 relationship 直接取得地圖與區域的物件，並由 Pydantic 自動轉換
    current_map: MapNameResponse
    current_area: AreaNameResponse
    model_config = ConfigDict(from_attributes=True)


class UserCharResponse(BaseModel):
    """用於 API 回應的使用者角色結構"""
    id: int
    level: int
    exp: int
    hp: int
    mp: int
    atk: int
    spd: int
    # 在 SQLAlchemy 模型中為 'def_'，在 JSON 中輸出為 'def'
    def_: int = Field(alias="def")
    status_effects: dict
    is_locked: bool
    template: CharTempBase  # 嵌套角色的模板資訊

    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,  # 允許 alias 正常運作
    )
class UpdateTeamRequest(BaseModel):
    """用於更新使用者隊伍的請求結構"""
    char_ids: list[int] = Field(
        ...,
        max_length=6,
        description="要設定為隊伍的角色 ID 列表，最多 6 位"
    )
    @model_validator(mode='after')
    def check_unique_char_ids(self) -> 'UpdateTeamRequest':
        if len(self.char_ids) != len(set(self.char_ids)):
            raise ValueError('隊伍中的角色 ID 不可重複')
        return self


class UserTeamMemberResponse(BaseModel):
    """用於 API 回應的使用者隊伍成員簡化資訊"""
    user_char_id: int
    char_temp_id: int
    name: str
    level: int
    position: int
    image_sm_url: str | None = None


class UserCharSimpleResponse(BaseModel):
    """用於 API 回應的使用者角色簡化資訊"""
    user_char_id: int
    char_temp_id: int
    name: str
    level: int
    image_sm_url:str
