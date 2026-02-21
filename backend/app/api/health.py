from fastapi import APIRouter

router = APIRouter()


@router.get("/")
async def get_health_data():
    # TODO: 건강 데이터 연동
    return {"data": []}
