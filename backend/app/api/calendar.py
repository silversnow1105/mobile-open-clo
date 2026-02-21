from fastapi import APIRouter

router = APIRouter()


@router.get("/events")
async def get_events(start_date: str, end_date: str):
    # TODO: Google Calendar API 연동
    return {"events": []}


@router.post("/sync")
async def sync_calendar(access_token: str):
    # TODO: Google Calendar 동기화
    return {"status": "synced"}
