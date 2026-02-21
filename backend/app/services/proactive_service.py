from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user import User
from app.models.notification import Notification
from app.services.push_service import push_service


async def check_and_notify(user_id: int, *, db: AsyncSession) -> None:
    """사용자 상태를 확인하고 프로액티브 알림을 생성·발송합니다."""
    # TODO: 일정, 감정, 행동 패턴 기반 알림 메시지 결정 로직
    message = "오늘 하루는 어떠셨나요? 잠깐이라도 기록을 남겨보세요."

    notification = Notification(user_id=user_id, message=message)
    db.add(notification)
    await db.commit()

    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if user and user.fcm_token:
        push_service.send(
            fcm_token=user.fcm_token,
            title="오픈 클로",
            body=message,
        )
