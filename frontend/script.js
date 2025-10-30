// script.js - JavaScript for File Upload Page

const API_BASE_URL = "http://127.0.0.1:8000";
const MAX_FILE_SIZE = 50 * 1024 * 1024; // 50 MB

/**
 * Validates the selected file before upload
 * @param {File} file - The file to validate
 * @returns {Object} - Validation result with isValid flag and message
 */
function validateFile(file) {
    // Check if file exists
    if (!file) {
        return { isValid: false, message: "Please select a file first." };
    }
    
    // Check file size
    if (file.size === 0) {
        return { isValid: false, message: "Empty files are not allowed." };
    }
    
    if (file.size > MAX_FILE_SIZE) {
        const maxSizeMB = (MAX_FILE_SIZE / (1024 * 1024)).toFixed(0);
        return { isValid: false, message: `File too large. Maximum size is ${maxSizeMB} MB.` };
    }
    
    return { isValid: true, message: "File is valid." };
}

/**
 * Displays a status message to the user
 * @param {string} message - The message to display
 * @param {string} type - The message type (success, error, info)
 */
function showStatus(message, type = 'info') {
    const status = document.getElementById("status");
    status.textContent = message;
    status.className = `status ${type}`;
    status.style.display = "block";
}

/**
 * Uploads a file to the server
 */
async function uploadFile() {
    const fileInput = document.getElementById("fileInput");
    const uploadBtn = document.getElementById("uploadBtn");

    if (!fileInput.files.length) {
        showStatus("Please select a file first.", "error");
        return;
    }

    const file = fileInput.files[0];
    
    // Validate file
    const validation = validateFile(file);
    if (!validation.isValid) {
        showStatus(validation.message, "error");
        return;
    }
    
    const formData = new FormData();
    formData.append("file", file);

    // Disable button and show loading state
    uploadBtn.disabled = true;
    uploadBtn.textContent = "Uploading...";
    showStatus("Uploading file, please wait...", "info");

    try {
        const response = await fetch(`${API_BASE_URL}/upload-document`, {
            method: "POST",
            body: formData,
        });

        const result = await response.json();
        
        if (response.ok) {
            showStatus(`✓ ${result.message} (File ID: ${result.file_id})`, "success");
            fileInput.value = ""; // Clear the file input
        } else {
            showStatus(`✗ Upload failed: ${result.detail}`, "error");
        }
    } catch (error) {
        showStatus(`✗ Error: ${error.message}. Make sure the backend server is running.`, "error");
        console.error('Upload error:', error);
    } finally {
        // Re-enable button
        uploadBtn.disabled = false;
        uploadBtn.textContent = "Upload File";
    }
}

// Event listener for upload button
document.getElementById("uploadBtn").addEventListener("click", uploadFile);

// Show selected file information when a file is chosen
document.getElementById("fileInput").addEventListener("change", (e) => {
    if (e.target.files.length > 0) {
        const file = e.target.files[0];
        const fileSize = (file.size / 1024).toFixed(2);
        const fileSizeUnit = fileSize < 1024 ? 'KB' : 'MB';
        const displaySize = fileSize < 1024 ? fileSize : (fileSize / 1024).toFixed(2);
        
        showStatus(`Selected: ${file.name} (${displaySize} ${fileSizeUnit})`, "info");
    }
});
