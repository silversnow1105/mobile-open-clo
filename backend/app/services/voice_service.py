import tempfile
from pathlib import Path
from openai import AsyncOpenAI
from app.config import settings


class VoiceService:
    def __init__(self):
        self._client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)

    async def transcribe(self, audio_bytes: bytes, filename: str = "audio.webm") -> str:
        """음성 파일을 텍스트로 변환합니다 (Whisper STT)."""
        suffix = Path(filename).suffix or ".webm"
        with tempfile.NamedTemporaryFile(suffix=suffix, delete=False) as tmp:
            tmp.write(audio_bytes)
            tmp.flush()
            with open(tmp.name, "rb") as audio_file:
                result = await self._client.audio.transcriptions.create(
                    model=settings.OPENAI_WHISPER_MODEL,
                    file=audio_file,
                )
        return result.text

    async def synthesize(self, text: str) -> bytes:
        """텍스트를 음성으로 변환합니다 (TTS)."""
        response = await self._client.audio.speech.create(
            model=settings.TTS_MODEL,
            voice=settings.TTS_VOICE,
            input=text,
        )
        return response.content


voice_service = VoiceService()
