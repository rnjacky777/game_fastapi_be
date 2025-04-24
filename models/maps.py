# app/models/map.py

from sqlalchemy import Column, Integer, String, Text, ForeignKey, Table
from sqlalchemy.orm import relationship, Mapped, mapped_column
from database import Base
from models.association_tables import map_connection
# 多地圖連結




class Map(Base):
    __tablename__ = "maps"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    image_url: Mapped[str] = mapped_column(String(255), nullable=True)

    # 與事件建立多對多關聯
    events: Mapped[list["Event"]] = relationship( # type: ignore
        "Event",
        secondary="map_event_association",
        back_populates="maps"
    )

    # 每個 map 會有多個使用者進度
    user_progresses: Mapped[list["UserMapProgress"]] = relationship(
        "UserMapProgress",
        back_populates="map"
    )

    # 小地圖
    areas: Mapped[list["MapArea"]] = relationship("MapArea", back_populates="map")

    # 多個地圖的連結
    connected_maps = relationship(
        "Map",
        secondary=map_connection,
        primaryjoin=id == map_connection.c.from_map_id,
        secondaryjoin=id == map_connection.c.to_map_id,
        backref="connected_from"
    )
# app/models/map.py (繼續加在同一個檔案裡)

class UserMapProgress(Base):
    __tablename__ = "user_map_progress"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    # user_id: Mapped[int] = mapped_column(ForeignKey("users.id")) Skip
    map_id: Mapped[int] = mapped_column(ForeignKey("maps.id"))
    
    # 進度數值可以是百分比、已完成事件數等
    progress: Mapped[int] = mapped_column(default=0)
    is_completed: Mapped[bool] = mapped_column(default=False)

    # 關聯
    user: Mapped["User"] = relationship("User", back_populates="current_progress") # type: ignore
    map: Mapped["Map"] = relationship("Map", back_populates="user_progresses")


class MapArea(Base):
    __tablename__ = "map_areas"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    map_id: Mapped[int] = mapped_column(ForeignKey("maps.id"), nullable=False)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    image_url: Mapped[str] = mapped_column(String(255), nullable=True)

    # 關聯可暫時註解或保留
    map = relationship("Map", back_populates="areas")  # 可暫時不使用
    events = relationship(
        "Event",  # <- 注意這裡是字串
        secondary="map_area_event_association",  # 表名（字串）
        back_populates="areas"
    )