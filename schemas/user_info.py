from decimal import Decimal
from pydantic import BaseModel, StrictInt, StrictStr


class MapInfo(BaseModel):
    map_id: StrictInt
    name: StrictStr
    persentage: Decimal


class UserInfo(BaseModel):
    user_id: StrictStr
    map_info: MapInfo
    money: StrictInt
