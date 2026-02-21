from datetime import datetime, timedelta, timezone
from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession
from weaviate.classes.query import Filter
from app.core.weaviate_client import get_weaviate_client, ensure_collection, COLLECTION_NAME
from app.models.diary import Diary


async def index_diary(diary: Diary) -> None:
    """다이어리를 Weaviate 벡터 DB에 인덱싱합니다."""
    client = get_weaviate_client()
    try:
        ensure_collection(client)
        collection = client.collections.get(COLLECTION_NAME)
        collection.data.insert(
            properties={
                "user_id": diary.user_id,
                "content": diary.content,
                "emotion": diary.emotion or "",
                "diary_id": diary.id,
                "created_at": diary.created_at.isoformat(),
            }
        )
    finally:
        client.close()


async def query_with_context(user_id: int, query: str, *, db: AsyncSession) -> str:
    """Weaviate 벡터 검색으로 관련 다이어리 컨텍스트를 반환합니다."""
    client = get_weaviate_client()
    try:
        collection = client.collections.get(COLLECTION_NAME)
        results = collection.query.near_text(
            query=query,
            filters=Filter.by_property("user_id").equal(user_id),
            limit=10,
        )
        if not results.objects:
            return ""
        return "\n---\n".join(obj.properties["content"] for obj in results.objects)
    finally:
        client.close()


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
