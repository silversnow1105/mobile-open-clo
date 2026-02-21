from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.models.diary import Diary
from app.schemas.diary import DiaryCreate, DiaryResponse
from app.services.rag_service import index_diary

router = APIRouter()


@router.post("/", response_model=DiaryResponse, status_code=201)
async def create_diary(body: DiaryCreate, db: AsyncSession = Depends(get_db)):
    # TODO: 현재 유저 ID를 인증에서 가져오기
    diary = Diary(user_id=1, content=body.content)
    db.add(diary)
    await db.commit()
    await db.refresh(diary)
    await index_diary(diary)
    return diary


@router.get("/", response_model=list[DiaryResponse])
async def list_diaries(db: AsyncSession = Depends(get_db)):
    # TODO: 현재 유저 ID로 필터링
    result = await db.execute(select(Diary).order_by(Diary.created_at.desc()))
    return result.scalars().all()
