from pydantic import BaseModel, Field, ConfigDict
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