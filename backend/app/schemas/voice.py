from pydantic import BaseModel


class TranscriptionResponse(BaseModel):
    text: str
    diary_id: int


class TTSRequest(BaseModel):
    text: str


class TTSResponse(BaseModel):
    audio_url: str
