from datetime import datetime, timedelta, timezone
from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.diary import Diary


async def query_with_context(user_id: int, query: str, *, db: AsyncSession) -> str:
    """사용자 다이어리 기반 RAG 검색을 수행합니다."""
    # TODO: 벡터 DB 연동으로 교체 (현재는 최근 다이어리 기반 단순 컨텍스트)
    result = await db.execute(
        select(Diary)
        .where(Diary.user_id == user_id)
        .order_by(Diary.created_at.desc())
        .limit(20)
    )
    diaries = result.scalars().all()
    context = "\n---\n".join(d.content for d in diaries)
    return context


async def fetch_weekly_diaries(
    user_id: int, week_start: datetime, *, db: AsyncSession
) -> list[Diary]:
    """특정 주간의 다이어리를 조회합니다."""
    week_end = week_start + timedelta(days=7)
    result = await db.execute(
        select(Diary)
        .where(
            and_(
                Diary.user_id == user_id,
                Diary.created_at >= week_start,
                Diary.created_at < week_end,
            )
        )
        .order_by(Diary.created_at.asc())
    )
    return list(result.scalars().all())
