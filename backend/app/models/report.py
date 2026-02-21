from datetime import date, datetime, timezone
from sqlalchemy import ForeignKey, Text, Date
from sqlalchemy.orm import Mapped, mapped_column
from app.core.database import Base


class WeeklyReport(Base):
    __tablename__ = "weekly_reports"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    week_start: Mapped[date] = mapped_column(Date)
    week_end: Mapped[date] = mapped_column(Date)
    summary: Mapped[str] = mapped_column(Text)
    dominant_emotion: Mapped[str | None] = mapped_column(default=None)
    emotion_distribution: Mapped[str | None] = mapped_column(Text, default=None)
    created_at: Mapped[datetime] = mapped_column(default=lambda: datetime.now(timezone.utc))
