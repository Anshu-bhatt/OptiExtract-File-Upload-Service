// history.js - JavaScript for File History Page

const API_BASE_URL = "http://127.0.0.1:8000";

/**
 * Formats bytes to human-readable size
 * @param {number} bytes - Size in bytes
 * @returns {string} Formatted size string
 */
function formatFileSize(bytes) {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return Math.round(bytes / Math.pow(k, i) * 100) / 100 + ' ' + sizes[i];
}

/**
 * Formats ISO timestamp to readable date
 * @param {string} isoString - ISO format timestamp
 * @returns {string} Formatted date string
 */
function formatDate(isoString) {
    if (!isoString) return 'N/A';
    const date = new Date(isoString);
    return date.toLocaleString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit',
        second: '2-digit'
    });
}

/**
 * Creates a table row for a file entry
 * @param {Object} file - File metadata object
 * @returns {HTMLTableRowElement} Table row element
 */
function createFileRow(file) {
    const row = document.createElement('tr');
    row.innerHTML = `
        <td>${file.id}</td>
        <td class="filename" title="${file.original_filename}">${file.original_filename}</td>
        <td>${formatFileSize(file.file_size_bytes)}</td>
        <td>${formatDate(file.uploaded_at)}</td>
    `;
    return row;
}

/**
 * Displays an error message
 * @param {string} message - Error message to display
 */
function showError(message) {
    const error = document.getElementById('error');
    error.style.display = 'block';
    error.textContent = message;
}

/**
 * Fetches and displays file history from the API
 */
async function loadFileHistory() {
    const loading = document.getElementById('loading');
    const error = document.getElementById('error');
    const tableContainer = document.getElementById('fileTableContainer');
    const noFiles = document.getElementById('noFiles');
    const tableBody = document.getElementById('fileTableBody');

    try {
        // Reset UI state
        loading.style.display = 'block';
        error.style.display = 'none';
        tableContainer.style.display = 'none';
        noFiles.style.display = 'none';

        // Fetch files from API
        const response = await fetch(`${API_BASE_URL}/files`);
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();
        loading.style.display = 'none';

        // Validate response data
        if (!data.files || !Array.isArray(data.files)) {
            throw new Error('Invalid response format from server');
        }

        if (data.files.length > 0) {
            // Display table with files
            tableContainer.style.display = 'block';
            tableBody.innerHTML = '';

            // Create and append rows
            data.files.forEach(file => {
                const row = createFileRow(file);
                tableBody.appendChild(row);
            });
        } else {
            // No files found
            noFiles.style.display = 'block';
        }

    } catch (err) {
        loading.style.display = 'none';
        showError(`Error loading files: ${err.message}. Make sure the backend server is running.`);
        console.error('Error:', err);
    }
}

// Load files when page loads
document.addEventListener('DOMContentLoaded', loadFileHistory);
