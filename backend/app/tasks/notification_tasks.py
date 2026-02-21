from app.core.celery_app import celery_app


@celery_app.task
def send_proactive_notification(user_id: int):
    """프로액티브 알림을 비동기로 전송합니다."""
    # TODO: proactive_service 호출 + 푸시 알림
    pass
