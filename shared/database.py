from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import declarative_base, declared_attr
from typing import AsyncGenerator
from shared.config import settings

# Create async engine for high-concurrency connections
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG,
    future=True,
    pool_size=20,
    max_overflow=10
)

# Async session factory
async_session = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False
)

# Declarative base model incorporating automatic plural tablenames
class CustomBase:
    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower() + "s"

Base = declarative_base(cls=CustomBase)

async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    """Dependency helper providing thread-safe scoped database sessions."""
    async with async_session() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()
