from fastapi import FastAPI
from routers import login
from util.auth import verify_password, get_password_hash, create_access_token
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Modular FastAPI Project")

origins = [
    "http://localhost",  # Vite React 開發環境
    "http://127.0.0.1",  # 有時瀏覽器會用 127.0.0.1
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],             # 可允許的來源
    allow_credentials=True,           # 是否允許攜帶 cookie
    allow_methods=["*"],              # 允許所有 HTTP 方法 (GET, POST, PUT, DELETE...)
    allow_headers=["*"],              # 允許所有 headers
)

# 將不同路由模組註冊到主應用
app.include_router(login.router, prefix="/auth", tags=["Users"])

# @app.get("/api/hello")
# async def read_hello():
#     return {"message": "Hello from FastAPI!"}
