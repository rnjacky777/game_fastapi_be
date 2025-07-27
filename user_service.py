from sqlalchemy.orm import Session
from core_system.models.user import User

# NOTE: 以下是根據您 router 中的 import 推斷出的既有函式。
# 您應該將新的函式 `create_user_with_defaults` 與這些函式放在同一個檔案中。

def add_user(db: Session, username: str, password: str) -> User:
    # 您的 add_user 實作...
    ...

def create_user_data(db: Session, user_id: int):
    # 您的 create_user_data 實作...
    ...

def create_user_char(db: Session, char_id: int, target_user_id: int):
    # 您的 create_user_char 實作...
    ...

def create_user_with_defaults(db: Session, username: str, password: str) -> User:
    """
    建立一個新使用者及其預設的關聯資料 (user_data, user_char)。
    此函式只執行操作，但 **不提交 (commit)** 交易。
    呼叫者 (router) 負責交易的 commit 或 rollback。
    """
    new_user = add_user(db=db, username=username, password=password)
    create_user_data(db=db, user_id=new_user.id)
    create_user_char(db=db, char_id=1, target_user_id=new_user.id)
    return new_user