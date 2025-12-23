"""
Feedback Storage System
Collects user feedback for future model improvements
"""

import sqlite3
import json
from datetime import datetime
from pathlib import Path
from typing import Optional, List, Dict
import logging

logger = logging.getLogger(__name__)


class FeedbackStorage:
    """Store and retrieve user feedback on resume analyses"""
    
    def __init__(self, db_path: str = "feedback.db"):
        """Initialize feedback storage with SQLite database"""
        self.db_path = db_path
        self._init_database()
    
    def _init_database(self):
        """Create feedback table if it doesn't exist"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS feedback (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                overall_score REAL,
                user_rating INTEGER,
                was_helpful BOOLEAN,
                comments TEXT,
                resume_text TEXT,
                job_description TEXT,
                matched_skills TEXT,
                missing_skills TEXT,
                score_breakdown TEXT,
                session_id TEXT,
                UNIQUE(session_id)
            )
        """)
        
        conn.commit()
        conn.close()
        logger.info(f"Feedback database initialized at {self.db_path}")
    
    def save_feedback(
        self,
        session_id: str,
        overall_score: float,
        user_rating: Optional[int] = None,
        was_helpful: Optional[bool] = None,
        comments: Optional[str] = None,
        resume_text: Optional[str] = None,
        job_description: Optional[str] = None,
        matched_skills: Optional[List[str]] = None,
        missing_skills: Optional[List[str]] = None,
        score_breakdown: Optional[Dict] = None
    ) -> bool:
        """
        Save user feedback
        
        Args:
            session_id: Unique identifier for this analysis
            overall_score: System's calculated score
            user_rating: User's rating (1-5)
            was_helpful: Boolean if analysis was helpful
            comments: User's text comments
            resume_text: Resume content (optional, for training data)
            job_description: Job posting content
            matched_skills: List of matched skills
            missing_skills: List of missing skills
            score_breakdown: Detailed scores
            
        Returns:
            bool: Success status
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT OR REPLACE INTO feedback 
                (timestamp, overall_score, user_rating, was_helpful, comments,
                 resume_text, job_description, matched_skills, missing_skills,
                 score_breakdown, session_id)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                datetime.now().isoformat(),
                overall_score,
                user_rating,
                was_helpful,
                comments,
                resume_text,
                job_description,
                json.dumps(matched_skills) if matched_skills else None,
                json.dumps(missing_skills) if missing_skills else None,
                json.dumps(score_breakdown) if score_breakdown else None,
                session_id
            ))
            
            conn.commit()
            conn.close()
            
            logger.info(f"Feedback saved for session {session_id}")
            return True
            
        except Exception as e:
            logger.error(f"Error saving feedback: {e}")
            return False
    
    def get_all_feedback(self, limit: int = 100) -> List[Dict]:
        """Get all feedback entries"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT * FROM feedback 
            ORDER BY timestamp DESC 
            LIMIT ?
        """, (limit,))
        
        columns = [desc[0] for desc in cursor.description]
        rows = cursor.fetchall()
        conn.close()
        
        return [dict(zip(columns, row)) for row in rows]
    
    def get_statistics(self) -> Dict:
        """Get feedback statistics"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Total count
        cursor.execute("SELECT COUNT(*) FROM feedback")
        total_count = cursor.fetchone()[0]
        
        # Average rating
        cursor.execute("SELECT AVG(user_rating) FROM feedback WHERE user_rating IS NOT NULL")
        avg_rating = cursor.fetchone()[0] or 0
        
        # Helpful percentage
        cursor.execute("SELECT COUNT(*) FROM feedback WHERE was_helpful = 1")
        helpful_count = cursor.fetchone()[0]
        
        # Score distribution
        cursor.execute("""
            SELECT 
                AVG(overall_score) as avg_score,
                MIN(overall_score) as min_score,
                MAX(overall_score) as max_score
            FROM feedback
        """)
        score_stats = cursor.fetchone()
        
        conn.close()
        
        return {
            "total_feedback": total_count,
            "average_rating": round(avg_rating, 2),
            "helpful_count": helpful_count,
            "helpful_percentage": round((helpful_count / total_count * 100) if total_count > 0 else 0, 2),
            "avg_score": round(score_stats[0], 2) if score_stats[0] else 0,
            "min_score": score_stats[1] or 0,
            "max_score": score_stats[2] or 0
        }
    
    def export_training_data(self, output_path: str = "training_data.json") -> int:
        """
        Export feedback data for model training
        
        Returns:
            Number of exported records
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Get entries with ratings and both texts
        cursor.execute("""
            SELECT resume_text, job_description, overall_score, user_rating
            FROM feedback
            WHERE resume_text IS NOT NULL 
            AND job_description IS NOT NULL
            AND user_rating IS NOT NULL
        """)
        
        rows = cursor.fetchall()
        conn.close()
        
        # Prepare training data
        training_data = []
        for row in rows:
            # Normalize rating (1-5) to score (0-1)
            normalized_score = row[3] / 5.0
            
            training_data.append({
                "resume_text": row[0],
                "job_text": row[1],
                "system_score": row[2],
                "user_score": normalized_score,
                "final_score": (row[2] + normalized_score) / 2  # Blend both scores
            })
        
        # Save to JSON
        with open(output_path, 'w') as f:
            json.dump(training_data, f, indent=2)
        
        logger.info(f"Exported {len(training_data)} training examples to {output_path}")
        return len(training_data)


# Singleton instance
_feedback_storage = None

def get_feedback_storage() -> FeedbackStorage:
    """Get or create feedback storage instance"""
    global _feedback_storage
    if _feedback_storage is None:
        _feedback_storage = FeedbackStorage()
    return _feedback_storage
