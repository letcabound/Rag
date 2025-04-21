from fastapi import FastAPI
from api.router import router as api_router

app = FastAPI()
app.include_router(api_router)

@app.get("/health")
def health():
    return {"status": "OK"}


if __name__ == '__main__':
    import uvicorn
    # 让 FastAPI 应用监听所有的网络接口，包括：本机、内网(局域网)、外网(公网)
    uvicorn.run("run:app", host="0.0.0.0", port=8000, reload=True, workers=1)
