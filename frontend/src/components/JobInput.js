import React, { useState } from 'react';
import './JobInput.css';

const JobInput = ({ jobDescription, setJobDescription, jobUrl, setJobUrl }) => {
  const [activeTab, setActiveTab] = useState('paste');

  const handleFetchFromUrl = async () => {
    if (!jobUrl) {
      alert('Please enter a job posting URL');
      return;
    }

    // For now, we'll just notify the user
    alert('URL fetching feature coming soon! For now, please copy and paste the job description.');
    setActiveTab('paste');
  };

  return (
    <div className="job-input">
      <div className="tabs">
        <button
          className={`tab ${activeTab === 'paste' ? 'active' : ''}`}
          onClick={() => setActiveTab('paste')}
        >
          📝 Paste Description
        </button>
        <button
          className={`tab ${activeTab === 'url' ? 'active' : ''}`}
          onClick={() => setActiveTab('url')}
        >
          🔗 From URL
        </button>
      </div>

      <div className="tab-content">
        {activeTab === 'paste' ? (
          <div className="paste-tab">
            <textarea
              className="job-textarea"
              placeholder="Paste the job description here...&#10;&#10;Include:&#10;- Job title&#10;- Requirements&#10;- Responsibilities&#10;- Required skills&#10;- Experience needed"
              value={jobDescription}
              onChange={(e) => setJobDescription(e.target.value)}
              rows={12}
            />
            <div className="char-count">
              {jobDescription.length} characters
            </div>
          </div>
        ) : (
          <div className="url-tab">
            <p className="url-hint">
              Enter the URL of a job posting (LinkedIn, Indeed, etc.)
            </p>
            <input
              type="url"
              className="job-url-input"
              placeholder="https://example.com/job-posting"
              value={jobUrl}
              onChange={(e) => setJobUrl(e.target.value)}
            />
            <button className="fetch-button" onClick={handleFetchFromUrl}>
              🔍 Fetch Job Description
            </button>
            <p className="feature-note">
              ⚠️ Note: URL fetching is coming soon. Please use paste for now.
            </p>
          </div>
        )}
      </div>
    </div>
  );
};

export default JobInput;
