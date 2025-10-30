# Run this script to start the backend server
# Make sure you've installed dependencies first: pip install -r requirements.txt

Write-Host "Starting File Upload Service Backend..." -ForegroundColor Green
Write-Host "API will be available at: http://127.0.0.1:8000" -ForegroundColor Cyan
Write-Host "API Docs will be available at: http://127.0.0.1:8000/docs" -ForegroundColor Cyan
Write-Host ""
Write-Host "Press Ctrl+C to stop the server" -ForegroundColor Yellow
Write-Host ""

# Start the uvicorn server
uvicorn backend.main:app --reload
