from sqlalchemy import MetaData, text
from core_system.models.database import engine
from sqlalchemy.orm import Session
from core_system.models import BattleEventLogic
# from models.user import User
# from models.char_temp import CharTemp
from core_system.models.npc import *
from core_system.models.event import EventResult
from core_system.models.maps import *
from core_system.models.user import *
from core_system.models.char_temp import *
from core_system.models.items import *
from core_system.models.monsters import *
from core_system.models.database import Base

UserTeamMember.__table__.drop(engine, checkfirst=True)
UserChar.__table__.drop(engine, checkfirst=True)
UserData.__table__.drop(engine, checkfirst=True)
User.__table__.drop(engine, checkfirst=True)
Base.metadata.create_all(bind=engine)


# with engine.connect() as connection:
#     connection.execute(text('ALTER TABLE users ADD COLUMN current_map_id INTEGER DEFAULT null'))

# with Session(engine) as session:
#     # 清空 BattleEventLogic 表
#     session.query(BattleEventLogic).delete()
#     session.commit()
#     print("BattleEventLogic 表已清空！")