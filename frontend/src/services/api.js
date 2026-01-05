import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';
const API_KEY = process.env.REACT_APP_API_KEY || ''; // Set in .env file if auth is enabled

// Create axios instance with default config
const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: API_KEY ? { 'X-API-Key': API_KEY } : {},
});

// Add response interceptor for better error handling
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response) {
      // Server responded with error
      const status = error.response.status;
      const detail = error.response.data?.detail || 'Server error occurred';
      
      if (status === 401 || status === 403) {
        throw new Error('Authentication failed. Please check your API key.');
      } else if (status === 429) {
        throw new Error('Rate limit exceeded. Please try again later.');
      } else if (status === 413) {
        throw new Error('File or request too large. Please reduce the size.');
      } else {
        throw new Error(detail);
      }
    } else if (error.request) {
      throw new Error('No response from server. Make sure the API is running.');
    } else {
      throw new Error('Error setting up the request');
    }
  }
);

export const analyzeResume = async (resumeFile, jobDescription) => {
  const formData = new FormData();
  formData.append('resume_file', resumeFile);
  formData.append('job_description', jobDescription);

  const response = await apiClient.post('/api/analyze-file', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  });

  return response.data;
};

export const checkBias = async (resumeText, jobDescription) => {
  const response = await apiClient.post('/api/bias-check', {
    resume_text: resumeText,
    job_description: jobDescription,
  });

  return response.data;
};

export const batchAnalyze = async (resumeFiles, jobDescription) => {
  const formData = new FormData();
  formData.append('job_description', jobDescription);
  
  resumeFiles.forEach((file) => {
    formData.append('resume_files', file);
  });

  const response = await apiClient.post('/api/batch-analyze', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  });

  return response.data;
};
