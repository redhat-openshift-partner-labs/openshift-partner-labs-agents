"""
Database connection and operations for the OpenShift Partner Labs Agents application.
"""
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.exc import SQLAlchemyError
from contextlib import contextmanager
from typing import Generator, Optional
import logging

from .config import config

logger = logging.getLogger(__name__)

# Create database engine
engine = create_engine(
    config.DATABASE_URL,
    echo=config.DEBUG,
    pool_pre_ping=True,
    pool_recycle=300,
)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def create_tables():
    """Create all database tables."""
    try:
        # Import Base and models from all agents
        from agents.form_agent.models.base import Base
        # Import models to register them with Base
        from agents.form_agent.models import request  # noqa: F401

        Base.metadata.create_all(bind=engine)
        logger.info("Database tables created successfully")
    except SQLAlchemyError as e:
        logger.error(f"Error creating database tables: {e}")
        raise

def drop_tables():
    """Drop all database tables."""
    try:
        # Import Base and models from all agents
        from agents.form_agent.models.base import Base
        # Import models to register them with Base
        from agents.form_agent.models import request  # noqa: F401

        Base.metadata.drop_all(bind=engine)
        logger.info("Database tables dropped successfully")
    except SQLAlchemyError as e:
        logger.error(f"Error dropping database tables: {e}")
        raise

@contextmanager
def get_db_session() -> Generator[Session, None, None]:
    """
    Context manager for database sessions.
    Automatically handles session lifecycle.
    """
    session = SessionLocal()
    try:
        yield session
        session.commit()
    except Exception as e:
        session.rollback()
        logger.error(f"Database session error: {e}")
        raise
    finally:
        session.close()

def get_db() -> Generator[Session, None, None]:
    """
    Dependency for FastAPI to get database session.
    """
    with get_db_session() as session:
        yield session

def test_connection() -> bool:
    """
    Test database connection.
    """
    try:
        with get_db_session() as session:
            session.execute(text("SELECT 1"))
            logger.info("Database connection successful")
            return True
    except SQLAlchemyError as e:
        logger.error(f"Database connection failed: {e}")
        return False



