import asyncio
from sqlalchemy import select
from app.core.celery_app import celery_app
from app.core.database import async_session
from app.models.user import User
from app.services.proactive_service import check_and_notify


@celery_app.task
def send_proactive_notification(user_id: int):
    """특정 사용자에게 프로액티브 알림을 비동기로 전송합니다."""
    asyncio.run(_send_notification(user_id))


@celery_app.task
def send_proactive_notifications_all():
    """모든 사용자에게 프로액티브 알림을 전송합니다 (Celery Beat에서 주기적 호출)."""
    asyncio.run(_send_all())


async def _send_notification(user_id: int):
    async with async_session() as db:
        await check_and_notify(user_id, db=db)


async def _send_all():
    async with async_session() as db:
        result = await db.execute(select(User.id))
        user_ids = result.scalars().all()
        for user_id in user_ids:
            await check_and_notify(user_id, db=db)
