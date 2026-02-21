import json
from datetime import datetime, timedelta, timezone
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.report import WeeklyReport
from app.services.rag_service import fetch_weekly_diaries
from app.services.emotion_service import aggregate_emotions, get_dominant_emotion
from app.services.llm_service import get_llm_response


class ReportService:
    async def generate_weekly_report(
        self, user_id: int, *, db: AsyncSession
    ) -> WeeklyReport:
        """일주일치 다이어리와 감정 데이터를 종합하여 주간 심리 리포트를 생성합니다."""
        now = datetime.now(timezone.utc)
        week_start = now - timedelta(days=7)

        diaries = await fetch_weekly_diaries(user_id, week_start, db=db)
        if not diaries:
            return await self._create_empty_report(user_id, week_start, now, db=db)

        emotion_dist = aggregate_emotions(diaries)
        dominant = get_dominant_emotion(emotion_dist)

        diary_texts = "\n---\n".join(
            f"[{d.created_at.strftime('%m/%d')}] ({d.emotion or '미분석'}) {d.content}"
            for d in diaries
        )
        prompt = (
            "당신은 공감 능력이 뛰어난 심리 상담사입니다. "
            "아래는 사용자의 일주일간 일기와 감정 기록입니다.\n\n"
            f"{diary_texts}\n\n"
            f"감정 분포: {json.dumps(emotion_dist, ensure_ascii=False)}\n\n"
            "위 내용을 바탕으로 따뜻하고 통찰력 있는 주간 심리 분석 리포트를 작성해주세요. "
            "패턴, 변화 추이, 구체적인 조언을 포함해주세요."
        )
        summary = await get_llm_response(prompt)

        report = WeeklyReport(
            user_id=user_id,
            week_start=week_start.date(),
            week_end=now.date(),
            summary=summary,
            dominant_emotion=dominant,
            emotion_distribution=json.dumps(emotion_dist, ensure_ascii=False),
        )
        db.add(report)
        await db.commit()
        await db.refresh(report)
        return report

    async def _create_empty_report(
        self, user_id: int, week_start: datetime, week_end: datetime, *, db: AsyncSession
    ) -> WeeklyReport:
        report = WeeklyReport(
            user_id=user_id,
            week_start=week_start.date(),
            week_end=week_end.date(),
            summary="이번 주에는 기록된 일기가 없습니다. 다음 주에는 하루 한 줄이라도 적어보세요.",
        )
        db.add(report)
        await db.commit()
        await db.refresh(report)
        return report


report_service = ReportService()
