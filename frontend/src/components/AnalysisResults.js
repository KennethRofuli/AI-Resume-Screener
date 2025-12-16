import React from 'react';
import './AnalysisResults.css';
import ScoreCard from './ScoreCard';
import SkillsChart from './SkillsChart';

const AnalysisResults = ({ results }) => {
  const getScoreColor = (score) => {
    if (score >= 85) return '#4caf50';
    if (score >= 70) return '#2196f3';
    if (score >= 55) return '#ff9800';
    return '#f44336';
  };

  const getClassificationEmoji = (classification) => {
    if (classification.includes('Excellent')) return '🌟';
    if (classification.includes('Strong')) return '💪';
    if (classification.includes('Moderate')) return '👍';
    return '📊';
  };

  return (
    <div className="analysis-results">
      {/* Overall Score Section */}
      <div className="score-header">
        <div className="score-circle" style={{ borderColor: getScoreColor(results.overall_score) }}>
          <div className="score-value">{results.overall_score.toFixed(1)}</div>
          <div className="score-label">/ 100</div>
        </div>
        <div className="score-info">
          <h2>
            {getClassificationEmoji(results.classification)} {results.classification}
          </h2>
          <p className="recommendation">{results.recommendation}</p>
          <div className="confidence-badge">
            Confidence: {(results.confidence * 100).toFixed(0)}%
          </div>
        </div>
      </div>

      {/* Score Breakdown */}
      <div className="card">
        <h3>📊 Score Breakdown</h3>
        <div className="score-breakdown">
          <ScoreCard
            label="Semantic Match"
            score={results.score_breakdown.semantic_similarity}
            icon="🎯"
          />
          <ScoreCard
            label="Skill Match"
            score={results.score_breakdown.skill_match}
            icon="🛠️"
          />
          <ScoreCard
            label="Experience"
            score={results.score_breakdown.experience}
            icon="💼"
          />
          <ScoreCard
            label="Education"
            score={results.score_breakdown.education}
            icon="🎓"
          />
          <ScoreCard
            label="Keywords"
            score={results.score_breakdown.keyword_match}
            icon="🔑"
          />
        </div>
      </div>

      {/* Skills Analysis */}
      <div className="skills-section">
        <div className="card skills-card">
          <h3>✅ Matched Skills ({results.matched_skills.length})</h3>
          <div className="skills-list">
            {results.matched_skills.length > 0 ? (
              results.matched_skills.map((skill, index) => (
                <span key={index} className="skill-badge matched">
                  {skill}
                </span>
              ))
            ) : (
              <p className="no-skills">No matched skills found</p>
            )}
          </div>
        </div>

        <div className="card skills-card">
          <h3>❌ Missing Skills ({results.missing_skills.length})</h3>
          <div className="skills-list">
            {results.missing_skills.length > 0 ? (
              results.missing_skills.map((skill, index) => (
                <span key={index} className="skill-badge missing">
                  {skill}
                </span>
              ))
            ) : (
              <p className="no-skills">All required skills are present! 🎉</p>
            )}
          </div>
        </div>
      </div>

      {/* Skills Chart */}
      <div className="card">
        <h3>📈 Skills Visualization</h3>
        <SkillsChart
          matched={results.matched_skills.length}
          missing={results.missing_skills.length}
        />
      </div>

      {/* Strengths */}
      {results.strengths && results.strengths.length > 0 && (
        <div className="card">
          <h3>💪 Key Strengths</h3>
          <ul className="insights-list">
            {results.strengths.map((strength, index) => (
              <li key={index} className="strength-item">
                <span className="bullet">✓</span> {strength}
              </li>
            ))}
          </ul>
        </div>
      )}

      {/* Weaknesses */}
      {results.weaknesses && results.weaknesses.length > 0 && (
        <div className="card">
          <h3>⚠️ Areas for Improvement</h3>
          <ul className="insights-list">
            {results.weaknesses.map((weakness, index) => (
              <li key={index} className="weakness-item">
                <span className="bullet">!</span> {weakness}
              </li>
            ))}
          </ul>
        </div>
      )}

      {/* Explanation */}
      {results.explanation_summary && (
        <div className="card">
          <h3>📝 Detailed Analysis</h3>
          <p className="explanation-text">{results.explanation_summary}</p>
        </div>
      )}

      {/* Key Factors */}
      {results.key_factors && results.key_factors.length > 0 && (
        <div className="card">
          <h3>🔑 Key Decision Factors</h3>
          <ul className="insights-list">
            {results.key_factors.map((factor, index) => (
              <li key={index} className="factor-item">
                {factor}
              </li>
            ))}
          </ul>
        </div>
      )}

      {/* Improvement Suggestions */}
      {results.improvement_suggestions && results.improvement_suggestions.length > 0 && (
        <div className="card suggestions-card">
          <h3>💡 Suggestions for Improvement</h3>
          <ul className="insights-list">
            {results.improvement_suggestions.map((suggestion, index) => (
              <li key={index} className="suggestion-item">
                {suggestion}
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
};

export default AnalysisResults;
