# backend/models.py
"""
SQLAlchemy ORM models for database tables.
Defines the schema for the files table.
"""
from sqlalchemy import Column, Integer, String, DateTime, Index
from datetime import datetime
from .database import Base


class File(Base):
    """
    File model representing uploaded file metadata.
    
    Stores information about uploaded files including original and system filenames,
    file size, and upload timestamp.
    """
    __tablename__ = "files"
    
    # Primary key
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    
    # File information
    original_filename = Column(
        String(255),
        nullable=False,
        comment="Original name of the uploaded file"
    )
    
    system_filename = Column(
        String(255),
        nullable=False,
        unique=True,
        comment="Unique UUID-based filename used for storage"
    )
    
    file_size_bytes = Column(
        Integer,
        nullable=False,
        comment="Size of the file in bytes"
    )
    
    # Timestamp
    uploaded_at = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
        comment="Timestamp when the file was uploaded"
    )
    
    # Create index on uploaded_at for faster queries
    __table_args__ = (
        Index('idx_uploaded_at', 'uploaded_at'),
    )
    
    def __repr__(self):
        """String representation of the File object"""
        return f"<File(id={self.id}, original_filename='{self.original_filename}', size={self.file_size_bytes})>"
