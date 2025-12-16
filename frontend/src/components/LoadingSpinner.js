import React from 'react';
import './LoadingSpinner.css';

const LoadingSpinner = () => {
  return (
    <div className="loading-overlay">
      <div className="loading-container">
        <div className="spinner"></div>
        <h3>Analyzing Resume...</h3>
        <p>Using advanced NLP and semantic matching</p>
        <div className="loading-steps">
          <div className="loading-step">📄 Parsing resume</div>
          <div className="loading-step">🧠 Computing embeddings</div>
          <div className="loading-step">🎯 Matching skills</div>
          <div className="loading-step">📊 Generating insights</div>
        </div>
      </div>
    </div>
  );
};

export default LoadingSpinner;
