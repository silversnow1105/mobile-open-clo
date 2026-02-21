from collections import Counter
from app.models.diary import Diary
from app.services.llm_service import get_llm_response


async def analyze_emotion(text: str) -> str:
    """텍스트에서 감정을 분석합니다."""
    prompt = (
        "다음 텍스트의 주요 감정을 한 단어로 분류해줘 "
        "(기쁨, 슬픔, 분노, 불안, 평온, 감사 중 하나): "
        f"\n\n{text}"
    )
    return await get_llm_response(prompt)


def aggregate_emotions(diaries: list[Diary]) -> dict[str, int]:
    """다이어리 목록에서 감정 분포를 집계합니다."""
    emotions = [d.emotion for d in diaries if d.emotion]
    return dict(Counter(emotions))


def get_dominant_emotion(distribution: dict[str, int]) -> str | None:
    """가장 빈도 높은 감정을 반환합니다."""
    if not distribution:
        return None
    return max(distribution, key=distribution.get)
