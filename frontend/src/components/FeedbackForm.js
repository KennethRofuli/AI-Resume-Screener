import React, { useState, useEffect } from 'react';
import './FeedbackForm.css';

const FeedbackForm = ({ results, resumeText, jobDescription }) => {
  const [rating, setRating] = useState(0);
  const [hoveredRating, setHoveredRating] = useState(0);
  const [wasHelpful, setWasHelpful] = useState(null);
  const [comments, setComments] = useState('');
  const [submitted, setSubmitted] = useState(false);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [sessionId] = useState(() => 
    `session-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`
  );

  const handleSubmit = async () => {
    if (wasHelpful === null || rating === 0) {
      alert('Please provide a rating and indicate if this was helpful');
      return;
    }

    setIsSubmitting(true);

    const feedbackData = {
      session_id: sessionId,
      overall_score: results.overall_score,
      matched_skills: results.matched_skills,
      missing_skills: results.missing_skills,
      score_breakdown: results.score_breakdown,
      resume_text: resumeText,
      job_description: jobDescription,
      user_rating: rating,
      was_helpful: wasHelpful,
      comments: comments.trim() || null
    };

    try {
      const response = await fetch('http://localhost:8000/api/feedback', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(feedbackData),
      });

      if (response.ok) {
        setSubmitted(true);
      } else {
        const errorData = await response.json().catch(() => ({}));
        console.error('Feedback submission failed:', errorData);
        alert(`Failed to submit feedback: ${errorData.detail || 'Please try again.'}`);
      }
    } catch (error) {
      console.error('Error submitting feedback:', error);
      alert('Error submitting feedback. Please check your connection and ensure the backend is running.');
    } finally {
      setIsSubmitting(false);
    }
  };

  if (submitted) {
    return (
      <div className="card feedback-card">
        <div className="feedback-success">
          <div className="success-icon">✅</div>
          <h3>Thank You for Your Feedback!</h3>
          <p>Your input helps us improve the AI Resume Screener.</p>
        </div>
      </div>
    );
  }

  return (
    <div className="card feedback-card">
      <h3>📝 Help Us Improve</h3>
      <p className="feedback-subtitle">Your feedback trains our AI to be more accurate</p>
      
      <div className="feedback-section">
        <label className="feedback-label">How accurate was this analysis?</label>
        <div className="star-rating">
          {[1, 2, 3, 4, 5].map((star) => (
            <span
              key={star}
              className={`star ${star <= (hoveredRating || rating) ? 'filled' : ''}`}
              onClick={() => setRating(star)}
              onMouseEnter={() => setHoveredRating(star)}
              onMouseLeave={() => setHoveredRating(0)}
            >
              ★
            </span>
          ))}
        </div>
        <div className="rating-labels">
          <span>Poor</span>
          <span>Excellent</span>
        </div>
      </div>

      <div className="feedback-section">
        <label className="feedback-label">Was this analysis helpful?</label>
        <div className="helpful-buttons">
          <button
            className={`helpful-btn ${wasHelpful === true ? 'active' : ''}`}
            onClick={() => setWasHelpful(true)}
          >
            👍 Yes, helpful
          </button>
          <button
            className={`helpful-btn ${wasHelpful === false ? 'active' : ''}`}
            onClick={() => setWasHelpful(false)}
          >
            👎 Not helpful
          </button>
        </div>
      </div>

      <div className="feedback-section">
        <label className="feedback-label">
          Additional comments (optional)
        </label>
        <textarea
          className="feedback-textarea"
          placeholder="Tell us what we got right or wrong..."
          value={comments}
          onChange={(e) => setComments(e.target.value)}
          rows={4}
        />
      </div>

      <button
        className="submit-feedback-btn"
        onClick={handleSubmit}
        disabled={isSubmitting}
      >
        {isSubmitting ? 'Submitting...' : 'Submit Feedback'}
      </button>
    </div>
  );
};

export default FeedbackForm;
