from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from app.core.config import settings

connect_args = {"statement_cache_size": 0}
if settings.DATABASE_URL.startswith("postgresql+asyncpg") and settings.DATABASE_SSL:
    connect_args["ssl"] = "require"

engine = create_async_engine(
    settings.DATABASE_URL,
    echo=settings.DB_ECHO,
    pool_pre_ping=True,
    connect_args=connect_args,
)

AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

Base = declarative_base()

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
