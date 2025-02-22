from fastapi import FastAPI
from routers import login
from util.auth import verify_password, get_password_hash, create_access_token
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# 🔑 CORS 設定 (允許 React 的開發伺服器訪問 API)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5173"],  # React 執行位址
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app = FastAPI(title="Modular FastAPI Project")

# 將不同路由模組註冊到主應用
app.include_router(login.router, prefix="/auth", tags=["Users"])

@app.get("/api/hello")
async def read_hello():
    return {"message": "Hello from FastAPI!"}
