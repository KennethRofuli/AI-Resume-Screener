import React from 'react';
import './ScoreCard.css';

const ScoreCard = ({ label, score, icon }) => {
  const getScoreColor = (score) => {
    if (score >= 80) return '#4caf50';
    if (score >= 60) return '#2196f3';
    if (score >= 40) return '#ff9800';
    return '#f44336';
  };

  const getScoreLevel = (score) => {
    if (score >= 80) return 'Excellent';
    if (score >= 60) return 'Good';
    if (score >= 40) return 'Fair';
    return 'Poor';
  };

  return (
    <div className="score-card">
      <div className="score-card-icon">{icon}</div>
      <div className="score-card-label">{label}</div>
      <div className="score-card-value" style={{ color: getScoreColor(score) }}>
        {score.toFixed(1)}%
      </div>
      <div className="score-card-bar">
        <div
          className="score-card-fill"
          style={{
            width: `${score}%`,
            backgroundColor: getScoreColor(score),
          }}
        />
      </div>
      <div className="score-card-level" style={{ color: getScoreColor(score) }}>
        {getScoreLevel(score)}
      </div>
    </div>
  );
};

export default ScoreCard;
