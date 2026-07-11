from sqlmodel import SQLModel, create_engine, Session
from sqlalchemy.pool import StaticPool
from typing import Generator
from app.core.config import settings

# Create database engine
engine = create_engine(
    settings.DATABASE_URL,
    echo=False,  # Set to True for SQL query logging
    connect_args={"check_same_thread": False} if "sqlite" in settings.DATABASE_URL else {}
)

# For SQLite with StaticPool (useful for testing)
if "sqlite" in settings.DATABASE_URL:
    engine = create_engine(
        settings.DATABASE_URL,
        echo=False,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )


def create_db_and_tables():
    """Create database tables from SQLModel models."""
    SQLModel.metadata.create_all(engine)


def get_session() -> Generator[Session, None, None]:
    """
    Dependency for getting database sessions.
    
    Yields:
        Session: SQLModel database session
    """
    with Session(engine) as session:
        yield session