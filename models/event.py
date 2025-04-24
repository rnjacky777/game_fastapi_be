from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column
from database import Base


class Event(Base):
    __tablename__ = "events"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    # "battle", "normal", "special"
    type: Mapped[str] = mapped_column(String(50))
    description: Mapped[str] = mapped_column(Text)

    maps: Mapped[list["Map"]] = relationship( # type: ignore
        "Map",
        secondary="map_event_association",
        back_populates="events"
    )
    areas = relationship(
        "MapArea",  # <- 注意這裡是字串
        secondary="map_area_event_association",
        back_populates="events"
    )
    # 其他欄位如事件劇情、條件、結果等在這邊擴充

class EventResult(Base):
    __tablename__ = 'event_results'
    id = Column(Integer, primary_key=True)
    reward_pool_id = Column(Integer, ForeignKey('reward_pools.id'))
    status_effects_json = Column(Text)  # e.g., {"poison": 3, "heal": 100}

    reward_pool = relationship("RewardPool", back_populates="event_results")


class RewardPool(Base):
    __tablename__ = 'reward_pools'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)

    # 關聯到 pool_items
    items = relationship("RewardPoolItem", back_populates="pool", cascade="all, delete-orphan")
    monsters = relationship("Monster", back_populates="drop_pool")  # 哪些怪物使用這個 pool
    event_results = relationship("EventResult", back_populates="reward_pool")  # 哪些事件結果使用這個 pool



class GeneralEventLogic(Base):
    __tablename__ = 'general_event_logic'
    id = Column(Integer, primary_key=True)
    event_id = Column(Integer, ForeignKey('events.id'))
    story_text = Column(Text)  # 可為 JSON 字串，支援多段落
    condition_json = Column(Text)  # 儲存條件，例如 {"has_item": "torch"}
    success_result_id = Column(Integer, ForeignKey('event_results.id'))
    fail_result_id = Column(Integer, ForeignKey('event_results.id'))

    event = relationship("Event", backref="general_logic")


# class BattleEventLogic(Base):
#     __tablename__ = 'battle_event_logic'
#     id = Column(Integer, primary_key=True)
#     event_id = Column(Integer, ForeignKey('events.id'))
#     story_text = Column(Text)
#     monster_pool_id = Column(Integer, ForeignKey('monster_pools.id'))
#     reward_pool_id = Column(Integer, ForeignKey('reward_pools.id'))

#     event = relationship("Event", backref="battle_logic")
