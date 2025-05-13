from app.core.config import settings
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession

# Create the database engine
engine = create_async_engine(settings.DATABASE_URL, echo=True)

# session maker
async_session = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

# get db session
async def get_db():
    async with async_session() as session:
        yield session
        