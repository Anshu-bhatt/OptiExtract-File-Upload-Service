# Project Documentation

## A. Local Setup Guide

This guide will walk you through setting up and running the File Upload Service on your local machine.

### Prerequisites

- Python 3.8 or higher installed on your system
- Git (for cloning the repository)
- A web browser (Chrome, Firefox, Edge, etc.)

### Step 1: Clone the Repository

```bash
git clone <repository-url>
cd Task
```

### Step 2: Create a Virtual Environment

Creating a virtual environment ensures that project dependencies are isolated from your system Python installation.

**On Windows (PowerShell):**

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

**On Windows (Command Prompt):**

```cmd
python -m venv venv
venv\Scripts\activate.bat
```

**On macOS/Linux:**

```bash
python3 -m venv venv
source venv/bin/activate
```

You should see `(venv)` appear in your terminal prompt, indicating the virtual environment is active.

### Step 3: Install Dependencies

All required dependencies are listed in `requirements.txt`. Install them using:

```bash
pip install -r requirements.txt
```

**Dependencies installed:**

- `fastapi==0.104.1` - Modern web framework for building APIs
- `uvicorn[standard]==0.24.0` - ASGI server to run FastAPI
- `sqlalchemy==2.0.23` - SQL toolkit and ORM for database operations
- `python-multipart==0.0.6` - Required for file upload handling in FastAPI

### Step 4: Verify Project Structure

Ensure your project has the following structure:

```
Task/
├── backend/
│   ├── __init__.py
│   ├── main.py
│   ├── models.py
│   ├── database.py
│   ├── schemas.py
│   └── uploaded_files/    (created automatically)
├── frontend/
│   ├── index.html
│   ├── history.html
│   ├── script.js
│   ├── history.js
│   └── style.css
├── requirements.txt
└── start_server.ps1
```

### Step 5: Run the Backend Server

From the `Task` directory (with virtual environment activated):

```bash
uvicorn backend.main:app --reload
```

Or use the provided PowerShell script:

```powershell
.\start_server.ps1
```

You should see output similar to:

```
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process
INFO:     Application startup complete.
```

**Note:** The `--reload` flag enables auto-reload during development. The server will restart automatically when you make code changes.

### Step 6: Access the Frontend

Open your web browser and navigate to the frontend pages:

1. **Upload Page:** Open `frontend/index.html` directly in your browser
2. **History Page:** Open `frontend/history.html` directly in your browser

**Recommended:** For better development experience, use a local server:

- VS Code: Install "Live Server" extension and right-click on `index.html` → "Open with Live Server"
- Python: From the `frontend` directory, run `python -m http.server 5500`

### Step 7: Test the Application

1. **Upload a file:**

   - Go to the upload page
   - Click the file input and select any file
   - Click "Upload File"
   - You should see a success message

2. **View uploaded files:**
   - Go to the history page
   - You should see your uploaded file in the table with metadata

### Troubleshooting

**Issue:** "ModuleNotFoundError: No module named 'backend'"

- **Solution:** Make sure you're running the server from the `Task` directory, not from inside the `backend` folder.

**Issue:** "Failed to fetch" error in browser

- **Solution:** Ensure the backend server is running on `http://127.0.0.1:8000` before accessing the frontend.

**Issue:** CORS errors in browser console

- **Solution:** The CORS middleware is already configured. If you still see errors, try accessing the frontend via a local server instead of opening the HTML file directly.

**Issue:** Database errors

- **Solution:** Delete the `files.db` file and restart the server. The database will be recreated automatically.

---

## B. Project Overview & Rationale

### Project Structure

I organized the project into a clear separation between backend and frontend:

```
backend/     - All Python/FastAPI server code
frontend/    - All HTML/CSS/JavaScript client code
```

**Why this structure?**

1. **Separation of Concerns:** Keeping backend and frontend separate makes the codebase easier to navigate and maintain. A developer working on the API doesn't need to sift through HTML files, and vice versa.

2. **Modularity:** The backend is further divided into separate Python files:

   - `main.py` - API routes and application logic
   - `models.py` - Database table definitions (ORM)
   - `database.py` - Database connection and session management
   - `schemas.py` - Data validation and serialization

   This follows the Single Responsibility Principle - each file has one clear purpose.

3. **Scalability:** This structure makes it easy to add new features. For example, if we need authentication, we could add `auth.py` without cluttering existing files.

4. **Frontend Organization:** Each HTML page has its corresponding JavaScript file (`index.html` → `script.js`, `history.html` → `history.js`). The shared CSS is in a single `style.css` file to maintain consistent styling.

### Design Choices

#### 1. Unique System Filename Generation

**Method Chosen:** UUID4 + Original File Extension

**Implementation:**

```python
file_extension = Path(file.filename).suffix
unique_id = uuid.uuid4()
system_filename = f"{unique_id}{file_extension}"
```

**Why this approach?**

- **Guaranteed Uniqueness:** UUID4 generates a 128-bit random identifier with virtually zero collision probability. Even with millions of files, we won't have naming conflicts.

- **Preserves File Type:** By keeping the original file extension (`.pdf`, `.jpg`, etc.), we maintain file type information, which is useful for:

  - Operating system file associations
  - MIME type detection
  - Future download functionality

- **Security:** Random UUIDs prevent users from guessing other file names, which would be possible with sequential IDs or timestamps.

- **Simplicity:** UUID generation is a single function call - no need to maintain counters or check for existing filenames.

**Alternative approaches I considered:**

- Sequential numbering: Rejected because it's predictable and requires database queries to find the next number
- Timestamp-based: Rejected because multiple uploads in the same millisecond could collide
- Hash of file content: Rejected because it's computationally expensive and identical files would have the same name

#### 2. File and Database Synchronization

**The Challenge:** We need to save both the physical file AND the database record. If one fails, we could end up with:

- A file on disk with no database record (orphaned file)
- A database record with no actual file (broken reference)

**My Solution:**

1. **Order of Operations:**

   ```python
   # Step 1: Save file to disk first
   with open(file_path, "wb") as f:
       f.write(content)

   # Step 2: Save metadata to database
   db.add(new_file)
   db.commit()
   ```

2. **Error Handling with Cleanup:**
   ```python
   except SQLAlchemyError as e:
       db.rollback()
       # Clean up the file if database save failed
       if file_path.exists():
           file_path.unlink()
       raise HTTPException(...)
   ```

**Why this approach?**

- **File First:** I save the file before the database because it's easier to delete a file (if DB fails) than to restore a deleted file (if DB succeeds but file save fails).

- **Atomic Transaction:** The database operations use SQLAlchemy's session management, which provides transaction support. If anything goes wrong during commit, we can rollback.

- **Cleanup on Failure:** If the database save fails, I immediately delete the file to prevent orphaned files accumulating on disk.

- **All-or-Nothing:** The try-except block ensures that either both operations succeed, or neither does. This maintains data consistency.

**Trade-offs:**

- There's a tiny window where the file exists but isn't in the database (between saving the file and committing to DB). In a high-traffic production system, I would use database transactions that can also manage file operations, or implement a background cleanup job for orphaned files.

### Challenges Faced and Solutions

#### Challenge 1: CORS Issues During Development

**Problem:** Initially, when I tried to test the frontend by opening HTML files directly (`file:///`), the browser blocked API requests due to CORS policy.

**Solution:**

- Added CORS middleware to FastAPI with `allow_origins=["*"]`
- Documented the need to use a local server for the frontend (Live Server or Python's http.server)
- Added note in documentation that in production, specific origins should be whitelisted

**Learning:** Understanding the difference between serving files via `file://` protocol vs. `http://` protocol and how browsers enforce same-origin policy.

#### Challenge 2: Database Session Management

**Problem:** Early on, I had issues with database connections not closing properly, which could lead to connection pool exhaustion.

**Solution:**

- Implemented proper dependency injection using FastAPI's `Depends()`
- Used a generator function with try/finally to guarantee session cleanup:
  ```python
  def get_db():
      db = database.SessionLocal()
      try:
          yield db
      finally:
          db.close()
  ```

**Learning:** The importance of resource cleanup in web applications and how FastAPI's dependency injection handles it elegantly.

#### Challenge 3: File Size Validation

**Problem:** Without size limits, users could upload extremely large files, potentially filling up disk space or causing memory issues.

**Solution:**

- Implemented a 50 MB limit on the server side
- Added client-side validation for immediate user feedback
- Read file content into memory first, check size, then save:
  ```python
  content = await file.read()
  if len(content) > MAX_FILE_SIZE:
      raise HTTPException(...)
  ```

**Learning:** Always validate on both client and server. Client-side gives better UX, but server-side is essential for security.

#### Challenge 4: Pydantic Schema Integration

**Problem:** Initially returning raw dictionaries from endpoints. This lacked validation and proper API documentation.

**Solution:**

- Created `schemas.py` with Pydantic models for all responses
- Used `response_model` parameter in route decorators
- Enabled automatic OpenAPI documentation

**Learning:** Pydantic schemas provide type safety, validation, and self-documenting APIs. The small upfront effort pays off in maintainability.

---

## C. Adaptation & Aesthetics

### 1. Aesthetics

The frontend follows a **minimalist beige design** with these principles:

**Design Choices:**

- **Color Palette:** Soft beige tones (#f5f5dc, #e8dcc4, #c9b896) create a calm, professional appearance
- **Simple Layout:** Clean, uncluttered interface focusing on functionality
- **Responsive Design:** Media queries ensure the app works on mobile devices
- **User Feedback:** Clear status messages (success in green, errors in red) keep users informed
- **Navigation:** Simple tab-like navigation between upload and history pages

**CSS Highlights:**

- Minimal use of shadows and gradients for a flat, modern look
- Consistent spacing and padding throughout
- Hover effects for better interactivity
- Loading states to indicate async operations

### 2. Code Commenting

I added comprehensive comments throughout the codebase:

**Python Comments:**

- Module-level docstrings explaining each file's purpose
- Function docstrings with parameter and return descriptions
- Inline comments for complex logic (UUID generation, file cleanup)
- Type hints for clarity

**JavaScript Comments:**

- JSDoc-style function documentation
- Explanatory comments for validation logic
- Comments on async operations

**Example from `main.py`:**

```python
def get_db():
    """
    Dependency that provides a database session.
    Ensures proper session lifecycle management.
    """
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()  # Guaranteed cleanup even if exceptions occur
```

### 3. AI Tool Usage & Contribution

**My Development Process:**

I started this project with about **30% boilerplate code** already in place:

- Basic FastAPI app structure
- Simple file upload endpoint
- Minimal frontend HTML
- Basic models and database setup

**What I Added (70% of the work):**

1. **Enhanced Backend (40%):**

   - Created complete Pydantic schemas for validation
   - Added comprehensive error handling and rollback logic
   - Implemented file size validation
   - Enhanced database models with indexes and constraints
   - Added API documentation and proper HTTP status codes
   - Improved security with unique filename generation

2. **Improved Frontend (20%):**

   - Redesigned UI with minimalist beige theme
   - Added client-side validation
   - Implemented better error messaging
   - Created responsive design
   - Added loading states and user feedback
   - Improved code organization with modular functions

3. **Documentation & Code Quality (10%):**
   - Added comprehensive docstrings and comments
   - Created detailed documentation files
   - Implemented proper code organization
   - Added JSDoc comments to JavaScript

**AI Assistance Used:**

While I wrote the majority of the code myself, I used AI assistance (GitHub Copilot) for:

- **Code Enhancement (~30% contribution):** Reviewing and suggesting improvements to my existing code structure
- **Pydantic Schemas:** Helping generate the initial schema templates which I then customized
- **CSS Refinement:** Suggesting color harmonies for the beige theme
- **Best Practices:** Pointing out where I could improve error handling and validation

**My Own Contributions:**

- Overall architecture and file organization decisions
- Database synchronization strategy and rollback logic
- UUID-based filename generation approach
- Frontend validation logic and user experience flow
- Problem-solving for CORS and session management issues
- All design decisions explained in the "Rationale" section above

**Learning Outcomes:**

This project taught me:

1. How to properly structure a full-stack application with clear separation of concerns
2. The importance of data consistency (file + database synchronization)
3. Building RESTful APIs with proper validation and error handling
4. Managing database sessions and transactions in a web application
5. Creating user-friendly interfaces with proper feedback mechanisms

---

## API Documentation

Once the server is running, you can access interactive API documentation at:

- **Swagger UI:** http://127.0.0.1:8000/docs
- **ReDoc:** http://127.0.0.1:8000/redoc

These auto-generated docs allow you to test the API endpoints directly from your browser.

---

## Future Enhancements

If I were to extend this project, I would add:

1. **File Download:** Endpoint to download uploaded files
2. **File Deletion:** Allow users to delete uploaded files
3. **Authentication:** User login and file ownership
4. **File Type Restrictions:** Limit uploads to specific file types
5. **Pagination:** For the file history when dealing with many files
6. **Search/Filter:** Search files by name or filter by date/size
7. **Drag-and-Drop:** Improve upload UX with drag-and-drop interface
8. **Progress Bar:** Show upload progress for large files
9. **Database Migration:** Use Alembic for schema versioning
10. **Deployment:** Docker containerization for easy deployment

---

_This documentation was created as part of a learning project to demonstrate understanding of full-stack development with FastAPI, SQLAlchemy, and vanilla JavaScript._
