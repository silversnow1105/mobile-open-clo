from fastapi import APIRouter
from app.schemas.chat import ChatRequest, ChatResponse

router = APIRouter()


@router.post("/", response_model=ChatResponse)
async def chat(body: ChatRequest):
    # TODO: LLM 서비스 연동
    return ChatResponse(reply="챗 기능이 곧 연동됩니다.")
