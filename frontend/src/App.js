import React, { useState } from 'react';
import './App.css';
import ResumeUpload from './components/ResumeUpload';
import JobInput from './components/JobInput';
import AnalysisResults from './components/AnalysisResults';
import LoadingSpinner from './components/LoadingSpinner';
import { analyzeResume } from './services/api';

function App() {
  const [resumeFile, setResumeFile] = useState(null);
  const [jobDescription, setJobDescription] = useState('');
  const [jobUrl, setJobUrl] = useState('');
  const [loading, setLoading] = useState(false);
  const [results, setResults] = useState(null);
  const [error, setError] = useState(null);

  const handleAnalyze = async () => {
    if (!resumeFile) {
      setError('Please upload a resume');
      return;
    }

    if (!jobDescription && !jobUrl) {
      setError('Please provide a job description or URL');
      return;
    }

    setLoading(true);
    setError(null);
    setResults(null);

    try {
      let jobText = jobDescription;

      // If URL is provided, fetch the job description
      if (jobUrl && !jobDescription) {
        // For now, ask user to paste content
        // In production, you'd use a backend scraper
        setError('URL scraping not implemented yet. Please paste the job description.');
        setLoading(false);
        return;
      }

      const data = await analyzeResume(resumeFile, jobText);
      setResults(data);
    } catch (err) {
      setError(err.message || 'An error occurred during analysis');
    } finally {
      setLoading(false);
    }
  };

  const handleReset = () => {
    setResumeFile(null);
    setJobDescription('');
    setJobUrl('');
    setResults(null);
    setError(null);
  };

  return (
    <div className="App">
      <header className="App-header">
        <div className="header-content">
          <h1>🎯 AI Resume Screener</h1>
          <p>Intelligent resume screening powered by NLP and machine learning</p>
        </div>
      </header>

      <main className="App-main">
        {!results ? (
          <div className="input-section">
            <div className="card">
              <h2>Upload Resume</h2>
              <ResumeUpload
                onFileSelect={setResumeFile}
                selectedFile={resumeFile}
              />
            </div>

            <div className="card">
              <h2>Job Description</h2>
              <JobInput
                jobDescription={jobDescription}
                setJobDescription={setJobDescription}
                jobUrl={jobUrl}
                setJobUrl={setJobUrl}
              />
            </div>

            {error && (
              <div className="error-message">
                <span>⚠️ {error}</span>
              </div>
            )}

            <button
              className="analyze-button"
              onClick={handleAnalyze}
              disabled={loading || !resumeFile || (!jobDescription && !jobUrl)}
            >
              {loading ? 'Analyzing...' : '🔍 Analyze Resume'}
            </button>
          </div>
        ) : (
          <div className="results-section">
            <button className="reset-button" onClick={handleReset}>
              ← Analyze Another Resume
            </button>
            <AnalysisResults results={results} />
          </div>
        )}

        {loading && <LoadingSpinner />}
      </main>

      <footer className="App-footer">
        <p>Powered by Sentence-BERT & Advanced NLP | Built with React & FastAPI</p>
      </footer>
    </div>
  );
}

export default App;
