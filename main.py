import logging
from fastapi import FastAPI
from routers import loginO
from fastapi.middleware.cors import CORSMiddleware
from core_system.models.database import Base, engine

# --- 加入這段來設定日誌 ---
# 設定日誌的基本組態
logging.basicConfig(
    level=logging.INFO,  # 設定要顯示的最低日誌級別 (INFO, WARNING, ERROR, CRITICAL 都會顯示)
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",  # 設定日誌輸出的格式
    handlers=[
        logging.StreamHandler()  # 確保日誌輸出到控制台 (終端機)
    ]
)

app = FastAPI(title="Modular FastAPI Project")

origins = [
    "http://localhost",  # Vite React 開發環境
    "http://127.0.0.1",  # 有時瀏覽器會用 127.0.0.1
    "http://localhost:5173"
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,             # 可允許的來源
    allow_credentials=True,           # 是否允許攜帶 cookie
    allow_methods=["*"],              # 允許所有 HTTP 方法 (GET, POST, PUT, DELETE...)
    allow_headers=["*"],              # 允許所有 headers
)
Base.metadata.create_all(bind=engine)
# 將不同路由模組註冊到主應用
app.include_router(router=loginO.router,prefix="/api/auth")


# BO
# app.include_router(router=users.router,prefix="/admin/users")
