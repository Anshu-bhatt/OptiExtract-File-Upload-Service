# backend/schemas.py
"""
Pydantic schemas for request validation and response serialization.
These schemas ensure data integrity and provide automatic API documentation.
"""
from pydantic import BaseModel, Field, validator
from datetime import datetime
from typing import Optional


class FileUploadResponse(BaseModel):
    """Response schema for successful file upload"""
    message: str
    file_id: int
    
    class Config:
        json_schema_extra = {
            "example": {
                "message": "File uploaded successfully",
                "file_id": 1
            }
        }


class FileMetadata(BaseModel):
    """Schema for file metadata response"""
    id: int
    original_filename: str
    system_filename: str
    file_size_bytes: int
    uploaded_at: Optional[datetime]
    
    class Config:
        from_attributes = True  # Allows conversion from ORM models
        json_schema_extra = {
            "example": {
                "id": 1,
                "original_filename": "document.pdf",
                "system_filename": "a1b2c3d4-e5f6-7890-abcd-ef1234567890_document.pdf",
                "file_size_bytes": 102400,
                "uploaded_at": "2025-10-30T12:00:00"
            }
        }


class FileListResponse(BaseModel):
    """Response schema for file listing"""
    files: list[FileMetadata]
    count: int
    
    class Config:
        json_schema_extra = {
            "example": {
                "files": [
                    {
                        "id": 1,
                        "original_filename": "document.pdf",
                        "system_filename": "uuid_document.pdf",
                        "file_size_bytes": 102400,
                        "uploaded_at": "2025-10-30T12:00:00"
                    }
                ],
                "count": 1
            }
        }


class ErrorResponse(BaseModel):
    """Schema for error responses"""
    detail: str
    
    class Config:
        json_schema_extra = {
            "example": {
                "detail": "An error occurred while processing your request"
            }
        }
