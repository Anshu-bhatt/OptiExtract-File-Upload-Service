# Quick Start Guide

## Step-by-Step Setup

### Step 1: Install Python Dependencies

Open PowerShell in the `Task` directory and run:

```powershell
pip install -r requirements.txt
```

### Step 2: Start the Backend Server

You have two options:

**Option A: Use the startup script**

```powershell
.\start_server.ps1
```

**Option B: Run uvicorn directly**

```powershell
uvicorn backend.main:app --reload
```

You should see output like:

```
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

### Step 3: Open the Frontend

Open the frontend pages in your web browser:

1. **Upload Page**: Open `frontend/index.html` in your browser
2. **History Page**: Open `frontend/history.html` in your browser

**Recommended**: Use a local development server like:

- VS Code Live Server extension
- Python's built-in server: `python -m http.server 5500` (from the frontend directory)

### Step 4: Test the Application

1. **Test File Upload:**

   - Go to the upload page
   - Select any file from your computer
   - Click "Upload File"
   - You should see a success message

2. **Test File History:**
   - Go to the history page
   - You should see the uploaded file in the table
   - Verify the original filename, file size, and timestamp

## Verification Checklist

- [ ] Backend server is running without errors
- [ ] Frontend pages open in the browser
- [ ] File upload works successfully
- [ ] File history displays uploaded files
- [ ] Files are saved in `backend/uploaded_files/` directory
- [ ] Database file `files.db` is created in the Task directory

## Common Issues

### Issue: ModuleNotFoundError when starting the server

**Solution:** Make sure you're in the `Task` directory when running the uvicorn command:

```powershell
cd d:\internship\OptiExtract\Task
uvicorn backend.main:app --reload
```

### Issue: CORS error in browser console

**Solution:** The backend already has CORS enabled. Make sure:

1. The backend is running on http://127.0.0.1:8000
2. You're not using a file:// URL for the frontend (use a local server)

### Issue: "Failed to fetch" error

**Solution:** Ensure the backend server is running before trying to upload files or view history.

## File Locations

- **Uploaded Files**: `backend/uploaded_files/`
- **Database**: `files.db` (root of Task directory)
- **Backend Code**: `backend/` directory
- **Frontend Code**: `frontend/` directory

## API Testing

You can test the API directly:

1. **Interactive API Docs**: http://127.0.0.1:8000/docs
2. **Alternative Docs**: http://127.0.0.1:8000/redoc

These pages allow you to test the endpoints directly from your browser.
