import logging
import os
from fastapi import FastAPI
from routers import loginO, user, eventO
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware
from core_system.models.database import Base, engine
load_dotenv()
# --- 加入這段來設定日誌 ---
# 設定日誌的基本組態
logging.basicConfig(
    level=logging.DEBUG,  # 設定要顯示的最低日誌級別 (INFO, WARNING, ERROR, CRITICAL 都會顯示)
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",  # 設定日誌輸出的格式
    handlers=[
        logging.StreamHandler()  # 確保日誌輸出到控制台 (終端機)
    ]
)

app = FastAPI(title="Modular FastAPI Project",
              openapi_version="3.1.0",
              root_path="/game_api")

origins = os.getenv("CORS_ORIGINS", "*").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,             # 可允許的來源
    allow_credentials=True,           # 是否允許攜帶 cookie
    # 允許所有 HTTP 方法 (GET, POST, PUT, DELETE...)
    allow_methods=["*"],
    allow_headers=["*"],              # 允許所有 headers
)
if os.getenv("INIT_DB", "false").lower() == "true":
    Base.metadata.create_all(bind=engine)
# 將不同路由模組註冊到主應用
app.include_router(router=loginO.router, prefix="/auth")
app.include_router(router=user.router, prefix="")
app.include_router(router=eventO.router, prefix="")

# BO
# app.include_router(router=users.router,prefix="/admin/users")
