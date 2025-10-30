# backend/database.py
"""
Database configuration and session management for SQLAlchemy.
Sets up SQLite database connection and provides session factory.
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# SQLite database URL (creates a file named 'files.db' in the current directory)
SQLALCHEMY_DATABASE_URL = "sqlite:///./files.db"

# Create SQLAlchemy engine
# check_same_thread=False is needed for SQLite to work with FastAPI's async nature
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    echo=False,  # Set to True for SQL query logging during development
    pool_pre_ping=True  # Verify connections before using them
)

# Create a SessionLocal class for database sessions
# Each instance of SessionLocal will be a database session
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# Create a Base class for declarative models
# All ORM models will inherit from this base class
Base = declarative_base()
