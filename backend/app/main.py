from fastapi import FastAPI
from app.api import auth, diary, chat, calendar, health, voice, report

app = FastAPI(title="Mobile Open CLO", version="0.1.0")

app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
app.include_router(diary.router, prefix="/api/diary", tags=["diary"])
app.include_router(chat.router, prefix="/api/chat", tags=["chat"])
app.include_router(calendar.router, prefix="/api/calendar", tags=["calendar"])
app.include_router(health.router, prefix="/api/health", tags=["health"])
app.include_router(voice.router, prefix="/api/voice", tags=["voice"])
app.include_router(report.router, prefix="/api/report", tags=["report"])


@app.get("/healthcheck")
async def healthcheck():
    return {"status": "ok"}
