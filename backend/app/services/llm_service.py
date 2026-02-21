from app.config import settings


async def get_llm_response(prompt: str, context: str = "") -> str:
    """LLM API를 호출하여 응답을 반환합니다."""
    # TODO: langchain + Claude/GPT 연동
    raise NotImplementedError
