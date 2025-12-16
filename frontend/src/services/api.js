import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

export const analyzeResume = async (resumeFile, jobDescription) => {
  try {
    const formData = new FormData();
    formData.append('resume_file', resumeFile);
    formData.append('job_description', jobDescription);

    const response = await axios.post(
      `${API_BASE_URL}/api/analyze-file`,
      formData,
      {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      }
    );

    return response.data;
  } catch (error) {
    if (error.response) {
      throw new Error(error.response.data.detail || 'Server error occurred');
    } else if (error.request) {
      throw new Error('No response from server. Make sure the API is running.');
    } else {
      throw new Error('Error setting up the request');
    }
  }
};

export const checkBias = async (resumeText, jobDescription) => {
  try {
    const response = await axios.post(`${API_BASE_URL}/api/bias-check`, {
      resume_text: resumeText,
      job_description: jobDescription,
    });

    return response.data;
  } catch (error) {
    throw new Error(error.response?.data?.detail || 'Bias check failed');
  }
};

export const batchAnalyze = async (resumeFiles, jobDescription) => {
  try {
    const formData = new FormData();
    formData.append('job_description', jobDescription);
    
    resumeFiles.forEach((file) => {
      formData.append('resume_files', file);
    });

    const response = await axios.post(
      `${API_BASE_URL}/api/batch-analyze`,
      formData,
      {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      }
    );

    return response.data;
  } catch (error) {
    throw new Error(error.response?.data?.detail || 'Batch analysis failed');
  }
};
