import React, { useCallback } from 'react';
import './ResumeUpload.css';

const ResumeUpload = ({ onFileSelect, selectedFile }) => {
  const handleDrop = useCallback(
    (e) => {
      e.preventDefault();
      const file = e.dataTransfer.files[0];
      if (file && isValidFile(file)) {
        onFileSelect(file);
      }
    },
    [onFileSelect]
  );

  const handleDragOver = (e) => {
    e.preventDefault();
  };

  const handleFileInput = (e) => {
    const file = e.target.files[0];
    if (file && isValidFile(file)) {
      onFileSelect(file);
    }
  };

  const isValidFile = (file) => {
    const validTypes = ['application/pdf', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document', 'text/plain'];
    const validExtensions = ['.pdf', '.docx', '.txt'];
    
    const extension = file.name.substring(file.name.lastIndexOf('.')).toLowerCase();
    
    if (!validTypes.includes(file.type) && !validExtensions.includes(extension)) {
      alert('Please upload a PDF, DOCX, or TXT file');
      return false;
    }

    if (file.size > 10 * 1024 * 1024) {
      alert('File size must be less than 10MB');
      return false;
    }

    return true;
  };

  return (
    <div className="resume-upload">
      <div
        className={`dropzone ${selectedFile ? 'has-file' : ''}`}
        onDrop={handleDrop}
        onDragOver={handleDragOver}
      >
        <input
          type="file"
          id="resume-input"
          accept=".pdf,.docx,.txt"
          onChange={handleFileInput}
          style={{ display: 'none' }}
        />
        
        {selectedFile ? (
          <div className="file-selected">
            <div className="file-icon">📄</div>
            <div className="file-info">
              <p className="file-name">{selectedFile.name}</p>
              <p className="file-size">
                {(selectedFile.size / 1024).toFixed(2)} KB
              </p>
            </div>
            <button
              className="remove-file"
              onClick={(e) => {
                e.stopPropagation();
                onFileSelect(null);
              }}
            >
              ✕
            </button>
          </div>
        ) : (
          <label htmlFor="resume-input" className="upload-label">
            <div className="upload-icon">☁️</div>
            <p className="upload-text">
              <strong>Drop your resume here</strong> or click to browse
            </p>
            <p className="upload-hint">Supports PDF, DOCX, TXT (Max 10MB)</p>
          </label>
        )}
      </div>
    </div>
  );
};

export default ResumeUpload;
