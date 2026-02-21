from celery import Celery
from celery.schedules import crontab
from app.config import settings

celery_app = Celery("mobile_open_clo", broker=settings.REDIS_URL, backend=settings.REDIS_URL)
celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="Asia/Seoul",
)

celery_app.conf.beat_schedule = {
    "weekly-report-every-monday": {
        "task": "app.tasks.report_tasks.generate_all_weekly_reports",
        "schedule": crontab(hour=9, minute=0, day_of_week=1),
    },
    "proactive-notification-daily": {
        "task": "app.tasks.notification_tasks.send_proactive_notifications_all",
        "schedule": crontab(hour=20, minute=0),
    },
}
