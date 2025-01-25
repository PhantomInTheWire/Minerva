from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel
from ..config import Config

# Create async engine
async_engine = create_async_engine(
    url=Config.POSTGRES_URL,
    echo=True,  # Set to False in production
    future=True
)

# Session factory for background tasks and manual session management
SessionLocal = sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
    autocommit=False,
)

async def get_session() -> AsyncSession:
    """FastAPI dependency for request-scoped sessions"""
    async with SessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()

async def create_db_and_tables():
    """Create database tables (optional, for initialization)"""
    async with async_engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)