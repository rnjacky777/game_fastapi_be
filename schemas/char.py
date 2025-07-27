from pydantic import BaseModel, ConfigDict


class CharTempBase(BaseModel):
    """角色的基礎模板資訊"""
    id: int
    name: str
    rarity: int
    description: str | None = None
    base_hp: int
    base_mp: int
    base_atk: int
    base_spd: int
    base_def: int

    # Pydantic V2: 'from_attributes' replaces 'orm_mode'
    model_config = ConfigDict(from_attributes=True)