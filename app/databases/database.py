import aiomysql
from app.core.config import settings

async def get_connection():
    return await aiomysql.connect(
        host=settings.HOST,
        port=settings.PORT,
        user=settings.DB_USER,
        password=settings.DB_PASSWORD,
        db=settings.DB_NAME
    )
