from datetime import datetime
from pydantic import BaseModel


class DiaryCreate(BaseModel):
    content: str


class DiaryResponse(BaseModel):
    id: int
    content: str
    emotion: str | None
    created_at: datetime

    model_config = {"from_attributes": True}
