# backend/main.py
"""
FastAPI application for file upload service.
Provides endpoints for uploading files and retrieving file history.
"""
import os
import uuid
from fastapi import FastAPI, File, UploadFile, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from typing import List
from pathlib import Path

from . import models, database, schemas

app = FastAPI(
    title="File Upload Service API",
    description="API for uploading files and managing file metadata",
    version="1.0.0"
)

# Add CORS middleware to allow frontend to communicate with backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create tables on startup
models.Base.metadata.create_all(bind=database.engine)

# Configuration
UPLOAD_DIR = Path("./backend/uploaded_files")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
MAX_FILE_SIZE = 50 * 1024 * 1024  # 50 MB limit

# Dependency to get DB session
def get_db():
    """
    Dependency that provides a database session.
    Ensures proper session lifecycle management.
    """
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post(
    "/upload-document",
    response_model=schemas.FileUploadResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Upload a file",
    description="Upload a file to the server. The file will be stored with a unique UUID-based filename.",
    responses={
        201: {"description": "File uploaded successfully"},
        400: {"description": "Invalid file or file too large"},
        500: {"description": "Internal server error"}
    }
)
async def upload_document(
    file: UploadFile = File(..., description="File to upload (any type)"),
    db: Session = Depends(get_db)
) -> schemas.FileUploadResponse:
    """
    Upload a file to the server.
    
    - Validates file presence
    - Generates unique UUID-based filename to prevent conflicts
    - Stores file in local filesystem
    - Saves metadata to SQLite database
    
    Returns the file ID and success message.
    """
    # Validate file
    if not file.filename:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No filename provided"
        )
    
    try:
        # Read file content
        content = await file.read()
        
        # Check file size
        if len(content) > MAX_FILE_SIZE:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"File too large. Maximum size is {MAX_FILE_SIZE / (1024*1024):.0f} MB"
            )
        
        if len(content) == 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Empty file is not allowed"
            )
        
        # Generate a unique filename using UUID
        file_extension = Path(file.filename).suffix
        unique_id = uuid.uuid4()
        system_filename = f"{unique_id}{file_extension}"
        file_path = UPLOAD_DIR / system_filename
        
        # Save the file locally with secure filename
        with open(file_path, "wb") as f:
            f.write(content)
        
        # Save metadata in database
        new_file = models.File(
            original_filename=file.filename,
            system_filename=system_filename,
            file_size_bytes=len(content),
        )
        db.add(new_file)
        db.commit()
        db.refresh(new_file)
        
        return schemas.FileUploadResponse(
            message="File uploaded successfully",
            file_id=new_file.id
        )
    
    except SQLAlchemyError as e:
        db.rollback()
        # Clean up file if database operation fails
        if file_path.exists():
            file_path.unlink()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error: {str(e)}"
        )
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error uploading file: {str(e)}"
        )

@app.get(
    "/files",
    response_model=schemas.FileListResponse,
    summary="Get all files",
    description="Retrieve metadata for all uploaded files from the database.",
    responses={
        200: {"description": "List of files retrieved successfully"},
        500: {"description": "Internal server error"}
    }
)
async def get_files(db: Session = Depends(get_db)) -> schemas.FileListResponse:
    """
    Retrieve all file metadata from the database.
    
    Performs a SELECT query to get all file records and returns them
    with proper serialization using Pydantic models.
    
    Returns a list of file metadata and the total count.
    """
    try:
        # Retrieve all file records from the database (SELECT operation)
        files = db.query(models.File).order_by(models.File.uploaded_at.desc()).all()
        
        # Convert ORM models to Pydantic schemas for validation and serialization
        file_metadata_list = [schemas.FileMetadata.from_orm(file) for file in files]
        
        return schemas.FileListResponse(
            files=file_metadata_list,
            count=len(file_metadata_list)
        )
    
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving files: {str(e)}"
        )


@app.get("/", summary="Root endpoint")
async def root():
    """
    Root endpoint providing API information.
    """
    return {
        "message": "File Upload Service API",
        "version": "1.0.0",
        "endpoints": {
            "upload": "/upload-document",
            "files": "/files",
            "docs": "/docs"
        }
    }
