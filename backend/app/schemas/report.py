from datetime import date, datetime
from pydantic import BaseModel


class WeeklyReportResponse(BaseModel):
    id: int
    week_start: date
    week_end: date
    summary: str
    dominant_emotion: str | None
    emotion_distribution: str | None
    created_at: datetime

    model_config = {"from_attributes": True}
