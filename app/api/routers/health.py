from fastapi import APIRouter, status

router = APIRouter(tags=["health"])

@router.get("/health", response_model=dict, status_code=status.HTTP_200_OK)
async def health_status():
    return {"status": "ok"}
