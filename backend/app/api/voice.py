from fastapi import APIRouter, Depends, UploadFile, File
from fastapi.responses import Response
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.models.diary import Diary
from app.schemas.voice import TranscriptionResponse, TTSRequest
from app.services.voice_service import voice_service
from app.services.rag_service import index_diary

router = APIRouter()


@router.post("/transcribe", response_model=TranscriptionResponse)
async def transcribe_audio(
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
):
    """음성을 텍스트로 변환하고 다이어리로 저장합니다."""
    audio_bytes = await file.read()
    text = await voice_service.transcribe(audio_bytes, file.filename or "audio.webm")

    # TODO: 인증된 유저 ID로 교체
    diary = Diary(user_id=1, content=text)
    db.add(diary)
    await db.commit()
    await db.refresh(diary)
    await index_diary(diary)
    return TranscriptionResponse(text=text, diary_id=diary.id)


@router.post("/tts")
async def text_to_speech(body: TTSRequest):
    """텍스트를 음성으로 변환하여 오디오 바이너리를 반환합니다."""
    audio_bytes = await voice_service.synthesize(body.text)
    return Response(content=audio_bytes, media_type="audio/mpeg")
