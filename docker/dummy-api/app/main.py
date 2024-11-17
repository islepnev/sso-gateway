# docker/dummy-api/app/main.py

from fastapi import FastAPI, Header, HTTPException

app = FastAPI()

@app.get("/api/data")
async def get_data(x_remote_user: str = Header(None)):
    if not x_remote_user:
        raise HTTPException(status_code=401, detail="Unauthorized")
    return {"message": f"Hello, {x_remote_user}!"}

@app.post("/api/data")
async def post_data(data: dict, x_remote_user: str = Header(None)):
    if not x_remote_user:
        raise HTTPException(status_code=401, detail="Unauthorized")
    return {"message": f"Data received from {x_remote_user}", "data": data}
