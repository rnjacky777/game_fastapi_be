from database import SessionLocal
from models.user import User
from util.auth import get_password_hash

db = SessionLocal()

# 要新增的用戶資料
username = "jacky"
existing_user = db.query(User).filter(User.username == username).first()

if existing_user:
    print(f"❌ 使用者 '{username}' 已存在！")
else:
    new_user = User(
        username=username,
        full_name="Test User",
        hashed_password=get_password_hash("test1234")
    )
    db.add(new_user)
    db.commit()
    print(f"✅ 使用者 '{username}' 已新增成功！")

db.close()
