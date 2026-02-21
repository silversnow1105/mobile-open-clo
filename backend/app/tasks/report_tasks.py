import asyncio
from sqlalchemy import select
from app.core.celery_app import celery_app
from app.core.database import async_session
from app.models.user import User
from app.services.report_service import report_service


@celery_app.task
def generate_all_weekly_reports():
    """모든 사용자의 주간 심리 리포트를 생성합니다 (Celery Beat에서 주 1회 호출)."""
    asyncio.run(_generate_reports())


async def _generate_reports():
    async with async_session() as db:
        result = await db.execute(select(User.id))
        user_ids = result.scalars().all()
        for user_id in user_ids:
            await report_service.generate_weekly_report(user_id, db=db)
