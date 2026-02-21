from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.models.report import WeeklyReport
from app.schemas.report import WeeklyReportResponse

router = APIRouter()


@router.get("/", response_model=list[WeeklyReportResponse])
async def list_reports(db: AsyncSession = Depends(get_db)):
    """주간 리포트 목록을 반환합니다."""
    # TODO: 인증된 유저 ID로 필터링
    result = await db.execute(
        select(WeeklyReport).order_by(WeeklyReport.created_at.desc())
    )
    return result.scalars().all()


@router.get("/latest", response_model=WeeklyReportResponse | None)
async def latest_report(db: AsyncSession = Depends(get_db)):
    """가장 최근 주간 리포트를 반환합니다."""
    # TODO: 인증된 유저 ID로 필터링
    result = await db.execute(
        select(WeeklyReport).order_by(WeeklyReport.created_at.desc()).limit(1)
    )
    return result.scalar_one_or_none()
