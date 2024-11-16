from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def error_page():
    return {"error": "An error occurred during authentication."}
