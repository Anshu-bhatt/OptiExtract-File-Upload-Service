# File Upload Service

A web application for uploading files with FastAPI backend and vanilla JavaScript frontend.

## Features

- **File Upload**: Upload any type of file (PDF, images, text files, etc.)
- **Local Storage**: Files are stored with unique UUID-based filenames
- **Database Metadata**: SQLite database stores file metadata
- **File History**: View all uploaded files in a table format

## Technology Stack

### Backend

- FastAPI
- SQLAlchemy
- SQLite
- Python 3.x

### Frontend

- HTML5
- CSS3
- Vanilla JavaScript

## Project Structure

```
Task/
├── backend/
│   ├── __init__.py
│   ├── main.py           # FastAPI application with endpoints
│   ├── models.py         # SQLAlchemy models
│   ├── database.py       # Database configuration
│   └── uploaded_files/   # Directory for storing uploaded files
├── frontend/
│   ├── index.html        # Upload page
│   ├── history.html      # File history page
│   ├── script.js         # Upload page logic
│   ├── history.js        # File history page logic
│   └── style.css         # Styles for both pages
├── requirements.txt      # Python dependencies
└── README.md            # This file
```

## Setup Instructions

### 1. Install Dependencies

```powershell
pip install -r requirements.txt
```

### 2. Run the Backend Server

From the `Task` directory, run:

```powershell
uvicorn backend.main:app --reload
```

The API will be available at: `http://127.0.0.1:8000`

You can view the auto-generated API documentation at:

- Swagger UI: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`

### 3. Open the Frontend

Open the frontend files in your browser:

- Upload Page: `frontend/index.html`
- File History: `frontend/history.html`

You can use VS Code's Live Server extension or any local web server.

## API Endpoints

### POST /upload-document

Upload a file to the server.

**Request:**

- Method: POST
- Content-Type: multipart/form-data
- Body: file (binary)

**Response:**

```json
{
  "message": "File uploaded successfully",
  "file_id": 1
}
```

### GET /files

Retrieve all uploaded files metadata.

**Response:**

```json
{
  "files": [
    {
      "id": 1,
      "original_filename": "example.pdf",
      "system_filename": "uuid_example.pdf",
      "file_size_bytes": 12345,
      "uploaded_at": "2025-10-30T12:00:00"
    }
  ],
  "count": 1
}
```

## Database Schema

### Files Table

- `id` (Integer, Primary Key): Auto-incremented file ID
- `original_filename` (String): Original name of the uploaded file
- `system_filename` (String): UUID-based filename used for storage
- `file_size_bytes` (Integer): File size in bytes
- `uploaded_at` (DateTime): Timestamp of upload

## Usage

1. **Upload a File:**

   - Navigate to the upload page (`index.html`)
   - Click on the file input to select a file
   - Click "Upload File" button
   - See the success/error message

2. **View File History:**
   - Navigate to the file history page (`history.html`)
   - View all uploaded files in a table format
   - See original filename, file size, and upload timestamp

## Notes

- The SQLite database file (`files.db`) will be created automatically in the root directory
- The `uploaded_files` directory will be created automatically when the first file is uploaded
- CORS is enabled for all origins (for development purposes)
- In production, update CORS settings to allow only specific origins

## Troubleshooting

**Issue:** "Failed to fetch" error in frontend

- **Solution:** Make sure the backend server is running on `http://127.0.0.1:8000`

**Issue:** Import errors in backend

- **Solution:** Make sure you're running the server from the `Task` directory using `uvicorn backend.main:app --reload`

**Issue:** Files not uploading

- **Solution:** Check that the `backend/uploaded_files` directory exists and has write permissions
