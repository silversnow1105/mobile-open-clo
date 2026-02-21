import firebase_admin
from firebase_admin import credentials, messaging
from app.config import settings


class PushNotificationService:
    def __init__(self):
        self._initialized = False

    def _ensure_initialized(self):
        if self._initialized:
            return
        cred = credentials.Certificate(settings.FIREBASE_CREDENTIALS_PATH)
        firebase_admin.initialize_app(cred)
        self._initialized = True

    def send(self, fcm_token: str, title: str, body: str, data: dict | None = None) -> str:
        """단일 기기에 FCM 푸시 알림을 발송합니다."""
        self._ensure_initialized()
        message = messaging.Message(
            notification=messaging.Notification(title=title, body=body),
            data=data or {},
            token=fcm_token,
        )
        return messaging.send(message)

    def send_batch(self, fcm_tokens: list[str], title: str, body: str) -> messaging.BatchResponse:
        """여러 기기에 FCM 푸시 알림을 일괄 발송합니다."""
        self._ensure_initialized()
        message = messaging.MulticastMessage(
            notification=messaging.Notification(title=title, body=body),
            tokens=fcm_tokens,
        )
        return messaging.send_each_for_multicast(message)


push_service = PushNotificationService()
