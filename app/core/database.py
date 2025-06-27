from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import declarative_base
from sqlalchemy.exc import SQLAlchemyError, OperationalError
from app.core.config import settings
from typing import AsyncGenerator
import logging

SQLALCHEMY_DATABASE_URL = settings.DATABASE_URL

logger = logging.getLogger(__name__)
logger.info(f"Database URL: {SQLALCHEMY_DATABASE_URL}")

async_engine = create_async_engine(
    SQLALCHEMY_DATABASE_URL,
    pool_pre_ping=True,
    pool_recycle=3600,
)

AsyncSessionLocal = async_sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    autocommit=False,
    autoflush=False,
    expire_on_commit=False
)

Base = declarative_base()

"""
Dependency function that provides an asynchronous database session.
The session is automatically closed after the request is finished.
"""
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            # The 'async with' handles closing for AsyncSessionLocal
            pass

"""
Initializes the database by creating all defined tables.
This should be called when the application starts up.
"""
async def init_db():
    logger.info("Attempting to initialize database tables...")
    try:
        async with async_engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        logger.info("Database tables initialized.")
    except OperationalError as e:
        logger.error(
            f"Database connection failed during initialization: {e}. "
            f"Please check your database server status and connection credentials.",
            exc_info=True # This will print the full traceback in the logs
        )
        raise
    except SQLAlchemyError as e:
        logger.error(
            f"An SQLAlchemy error occurred during database initialization: {e}",
            exc_info=True
        )
        raise
    except Exception as e:
        # Catch any other unexpected errors
        logger.critical(
            f"An unexpected error occurred during database initialization: {e}",
            exc_info=True
        )
        raise