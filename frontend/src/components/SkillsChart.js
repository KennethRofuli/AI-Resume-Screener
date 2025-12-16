import React from 'react';
import './SkillsChart.css';

const SkillsChart = ({ matched, missing }) => {
  const total = matched + missing;
  const matchedPercent = total > 0 ? (matched / total) * 100 : 0;
  const missingPercent = total > 0 ? (missing / total) * 100 : 0;

  return (
    <div className="skills-chart">
      <div className="chart-bars">
        <div className="chart-bar">
          <div className="bar-label">Matched Skills</div>
          <div className="bar-container">
            <div
              className="bar-fill matched-bar"
              style={{ width: `${matchedPercent}%` }}
            >
              <span className="bar-value">{matched}</span>
            </div>
          </div>
        </div>

        <div className="chart-bar">
          <div className="bar-label">Missing Skills</div>
          <div className="bar-container">
            <div
              className="bar-fill missing-bar"
              style={{ width: `${missingPercent}%` }}
            >
              <span className="bar-value">{missing}</span>
            </div>
          </div>
        </div>
      </div>

      <div className="chart-summary">
        <div className="summary-item">
          <div className="summary-color matched"></div>
          <span>
            <strong>{matched}</strong> Matched ({matchedPercent.toFixed(1)}%)
          </span>
        </div>
        <div className="summary-item">
          <div className="summary-color missing"></div>
          <span>
            <strong>{missing}</strong> Missing ({missingPercent.toFixed(1)}%)
          </span>
        </div>
        <div className="summary-item total">
          <span>
            <strong>Total:</strong> {total} skills
          </span>
        </div>
      </div>
    </div>
  );
};

export default SkillsChart;
