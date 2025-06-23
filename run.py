# -*- coding: utf-8 -*-
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from api.router import router as api_router
from fastapi.staticfiles import StaticFiles

app = FastAPI()

# 允许所有源访问（开发阶段用，生产环境应限制来源）
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 或改为 ["http://127.0.0.1:5500"] 等你HTML页面实际来源
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 挂载 static 目录用于托管 HTML、JS、CSS 等静态资源
app.mount("/static", StaticFiles(directory="/static"), name="static")
app.include_router(api_router)

@app.get("/health")
async def health():
    return {"status": "OK"}

@app.get("/")
async def read_root():
    return RedirectResponse(url="/static/index.html")


if __name__ == '__main__':
    import uvicorn
    # 让 FastAPI 应用监听所有的网络接口，包括：本机、内网(局域网)、外网(公网)
    uvicorn.run("run:app", host="0.0.0.0", port=8000, reload=True, workers=1)

