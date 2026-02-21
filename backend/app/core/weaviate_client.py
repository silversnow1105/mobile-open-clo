import weaviate
from weaviate.classes.init import Auth
from app.config import settings

COLLECTION_NAME = "Diary"


def get_weaviate_client() -> weaviate.WeaviateClient:
    """Weaviate Cloud에 연결된 클라이언트를 반환합니다."""
    client = weaviate.connect_to_weaviate_cloud(
        cluster_url=settings.WEAVIATE_URL,
        auth_credentials=Auth.api_key(settings.WEAVIATE_API_KEY),
        headers={"X-OpenAI-Api-Key": settings.OPENAI_API_KEY},
    )
    return client


def ensure_collection(client: weaviate.WeaviateClient) -> None:
    """Diary 컬렉션이 없으면 생성합니다."""
    if client.collections.exists(COLLECTION_NAME):
        return

    from weaviate.classes.config import Configure, Property, DataType

    client.collections.create(
        name=COLLECTION_NAME,
        vectorizer_config=Configure.Vectorizer.text2vec_openai(),
        properties=[
            Property(name="user_id", data_type=DataType.INT),
            Property(name="content", data_type=DataType.TEXT),
            Property(name="emotion", data_type=DataType.TEXT),
            Property(name="diary_id", data_type=DataType.INT),
            Property(name="created_at", data_type=DataType.TEXT),
        ],
    )
