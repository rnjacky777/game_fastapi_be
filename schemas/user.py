from pydantic import BaseModel, Field, ConfigDict
from .char import CharTempBase


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