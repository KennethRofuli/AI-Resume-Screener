"""
Scoring Engine for Resume-Job Matching
Implements composite scoring with multiple factors
"""

import numpy as np
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class ScoringWeights:
    """Configurable weights for different scoring factors"""
    semantic_similarity: float = 0.30
    skill_match: float = 0.35
    experience_match: float = 0.20
    education_match: float = 0.10
    keyword_match: float = 0.05
    
    def __post_init__(self):
        """Validate weights sum to 1.0"""
        total = (self.semantic_similarity + self.skill_match + 
                self.experience_match + self.education_match + 
                self.keyword_match)
        if abs(total - 1.0) > 0.01:
            raise ValueError(f"Weights must sum to 1.0, got {total}")


@dataclass
class ScoreBreakdown:
    """Detailed breakdown of scoring components"""
    overall_score: float
    semantic_similarity: float
    skill_match_score: float
    experience_score: float
    education_score: float
    keyword_score: float
    confidence: float
    matched_skills: List[str] = field(default_factory=list)
    missing_skills: List[str] = field(default_factory=list)
    strengths: List[str] = field(default_factory=list)
    weaknesses: List[str] = field(default_factory=list)


class ScoringEngine:
    """Composite scoring engine for resume-job matching"""
    
    def __init__(self, weights: Optional[ScoringWeights] = None):
        """
        Initialize scoring engine
        
        Args:
            weights: Custom scoring weights (uses defaults if None)
        """
        self.weights = weights or ScoringWeights()
        logger.info(f"Scoring engine initialized with weights: {self.weights}")
    
    def calculate_overall_score(self,
                               semantic_similarity: float,
                               skill_match_rate: float,
                               experience_score: float,
                               education_score: float,
                               keyword_score: float) -> float:
        """
        Calculate weighted composite score
        
        Args:
            semantic_similarity: Semantic similarity score (0-1)
            skill_match_rate: Skill match rate (0-1)
            experience_score: Experience score (0-1)
            education_score: Education score (0-1)
            keyword_score: Keyword match score (0-1)
            
        Returns:
            Overall score (0-100)
        """
        weighted_score = (
            semantic_similarity * self.weights.semantic_similarity +
            skill_match_rate * self.weights.skill_match +
            experience_score * self.weights.experience_match +
            education_score * self.weights.education_match +
            keyword_score * self.weights.keyword_match
        )
        
        # Convert to 0-100 scale
        return weighted_score * 100
    
    def score_skills(self, 
                    resume_skills: List[str],
                    required_skills: List[str],
                    skill_similarities: Optional[Dict[str, float]] = None) -> Dict[str, Any]:
        """
        Score skill matching
        
        Args:
            resume_skills: Skills from resume
            required_skills: Required skills from job
            skill_similarities: Optional similarity scores for fuzzy matching
            
        Returns:
            Dictionary with skill scoring details
        """
        if not required_skills:
            return {
                'score': 1.0,
                'matched': [],
                'missing': [],
                'match_rate': 1.0
            }
        
        if not resume_skills:
            return {
                'score': 0.0,
                'matched': [],
                'missing': required_skills,
                'match_rate': 0.0
            }
        
        # Normalize skills for comparison
        resume_skills_lower = [s.lower() for s in resume_skills]
        required_skills_lower = [s.lower() for s in required_skills]
        
        matched = []
        missing = []
        
        for req_skill in required_skills:
            req_skill_lower = req_skill.lower()
            
            # Exact match
            if req_skill_lower in resume_skills_lower:
                matched.append(req_skill)
            # Fuzzy match using similarities
            elif skill_similarities and req_skill in skill_similarities:
                if skill_similarities[req_skill] >= 0.7:
                    matched.append(req_skill)
                else:
                    missing.append(req_skill)
            else:
                missing.append(req_skill)
        
        match_rate = len(matched) / len(required_skills)
        
        return {
            'score': match_rate,
            'matched': matched,
            'missing': missing,
            'match_rate': match_rate,
            'total_required': len(required_skills),
            'total_matched': len(matched)
        }
    
    def score_experience(self,
                        resume_years: Optional[float],
                        required_years: Optional[float]) -> float:
        """
        Score experience match
        
        Args:
            resume_years: Years of experience from resume
            required_years: Required years from job
            
        Returns:
            Experience score (0-1)
        """
        if required_years is None or resume_years is None:
            return 0.5  # Neutral score if data missing
        
        if resume_years >= required_years:
            # Full score if meets or exceeds
            # Bonus for significantly more experience (up to 1.2x)
            excess = resume_years - required_years
            bonus = min(excess / required_years * 0.2, 0.2)
            return min(1.0 + bonus, 1.0)
        else:
            # Proportional score if less than required
            ratio = resume_years / required_years
            # Apply soft penalty curve
            return ratio ** 0.7
    
    def score_education(self,
                       resume_education: List[str],
                       required_education: Optional[str]) -> float:
        """
        Score education match
        
        Args:
            resume_education: Education entries from resume
            required_education: Required education from job
            
        Returns:
            Education score (0-1)
        """
        if not required_education:
            return 1.0  # No requirement
        
        if not resume_education:
            return 0.3  # Some base score for missing data
        
        # Education level hierarchy
        levels = {
            'high school': 1,
            'associate': 2,
            'bachelor': 3,
            'master': 4,
            'phd': 5,
            'doctorate': 5
        }
        
        # Determine required level
        required_level = 0
        req_lower = required_education.lower()
        for degree, level in levels.items():
            if degree in req_lower:
                required_level = level
                break
        
        # Determine candidate's highest level
        candidate_level = 0
        for edu in resume_education:
            edu_lower = edu.lower()
            for degree, level in levels.items():
                if degree in edu_lower:
                    candidate_level = max(candidate_level, level)
        
        if candidate_level >= required_level:
            return 1.0
        elif candidate_level == required_level - 1:
            return 0.7
        else:
            return 0.4
    
    def score_keywords(self,
                      resume_text: str,
                      job_keywords: List[str]) -> float:
        """
        Score keyword presence
        
        Args:
            resume_text: Full resume text
            job_keywords: Important keywords from job
            
        Returns:
            Keyword score (0-1)
        """
        if not job_keywords:
            return 1.0
        
        resume_lower = resume_text.lower()
        matches = sum(1 for kw in job_keywords if kw.lower() in resume_lower)
        
        return matches / len(job_keywords)
    
    def calculate_confidence(self, score_breakdown: Dict[str, float]) -> float:
        """
        Calculate confidence score based on data completeness
        
        Args:
            score_breakdown: Dictionary of component scores
            
        Returns:
            Confidence score (0-1)
        """
        # Check which components have valid data (not default/neutral values)
        valid_components = 0
        total_components = 5
        
        if score_breakdown.get('semantic_similarity', 0) > 0.1:
            valid_components += 1
        if score_breakdown.get('skill_match_score', 0) > 0:
            valid_components += 1
        if score_breakdown.get('experience_score', 0) not in [0, 0.5]:
            valid_components += 1
        if score_breakdown.get('education_score', 0) not in [0.3, 1.0]:
            valid_components += 1
        if score_breakdown.get('keyword_score', 0) > 0:
            valid_components += 1
        
        return valid_components / total_components
    
    def generate_strengths_weaknesses(self,
                                     score_breakdown: ScoreBreakdown) -> tuple:
        """
        Identify strengths and weaknesses
        
        Args:
            score_breakdown: Score breakdown object
            
        Returns:
            Tuple of (strengths, weaknesses)
        """
        strengths = []
        weaknesses = []
        
        # Check each component
        if score_breakdown.skill_match_score >= 0.8:
            strengths.append(f"Strong skill alignment ({len(score_breakdown.matched_skills)} matched skills)")
        elif score_breakdown.skill_match_score < 0.5:
            weaknesses.append(f"Missing key skills: {', '.join(score_breakdown.missing_skills[:3])}")
        
        if score_breakdown.semantic_similarity >= 0.8:
            strengths.append("Excellent semantic match with job description")
        elif score_breakdown.semantic_similarity < 0.5:
            weaknesses.append("Resume content differs significantly from job requirements")
        
        if score_breakdown.experience_score >= 0.9:
            strengths.append("Meets or exceeds experience requirements")
        elif score_breakdown.experience_score < 0.7:
            weaknesses.append("May lack required experience level")
        
        if score_breakdown.education_score >= 0.9:
            strengths.append("Meets education requirements")
        elif score_breakdown.education_score < 0.7:
            weaknesses.append("Education level may not meet requirements")
        
        return strengths, weaknesses


class MatchClassifier:
    """Classify resume-job matches into categories"""
    
    THRESHOLDS = {
        'excellent': 85,
        'strong': 70,
        'moderate': 55,
        'weak': 40
    }
    
    @classmethod
    def classify(cls, overall_score: float) -> str:
        """
        Classify match quality
        
        Args:
            overall_score: Overall score (0-100)
            
        Returns:
            Classification label
        """
        if overall_score >= cls.THRESHOLDS['excellent']:
            return 'Excellent Match'
        elif overall_score >= cls.THRESHOLDS['strong']:
            return 'Strong Match'
        elif overall_score >= cls.THRESHOLDS['moderate']:
            return 'Moderate Match'
        elif overall_score >= cls.THRESHOLDS['weak']:
            return 'Weak Match'
        else:
            return 'Poor Match'
    
    @classmethod
    def get_recommendation(cls, overall_score: float, confidence: float) -> str:
        """
        Get hiring recommendation
        
        Args:
            overall_score: Overall score (0-100)
            confidence: Confidence in score (0-1)
            
        Returns:
            Recommendation text
        """
        classification = cls.classify(overall_score)
        
        if confidence < 0.5:
            return "Insufficient data for strong recommendation - manual review suggested"
        
        if overall_score >= cls.THRESHOLDS['excellent']:
            return "Highly Recommended - Strong candidate for interview"
        elif overall_score >= cls.THRESHOLDS['strong']:
            return "Recommended - Good candidate worth interviewing"
        elif overall_score >= cls.THRESHOLDS['moderate']:
            return "Consider - May be suitable depending on other factors"
        else:
            return "Not Recommended - Poor match for this position"


if __name__ == "__main__":
    # Test scoring engine
    print("Testing Scoring Engine...")
    
    engine = ScoringEngine()
    
    # Test composite scoring
    score = engine.calculate_overall_score(
        semantic_similarity=0.85,
        skill_match_rate=0.75,
        experience_score=0.90,
        education_score=1.0,
        keyword_score=0.80
    )
    
    print(f"\nOverall Score: {score:.2f}/100")
    print(f"Classification: {MatchClassifier.classify(score)}")
    print(f"Recommendation: {MatchClassifier.get_recommendation(score, 0.8)}")
    
    # Test skill scoring
    resume_skills = ["Python", "Django", "PostgreSQL", "Docker"]
    required_skills = ["Python", "Flask", "Docker", "AWS"]
    
    skill_result = engine.score_skills(resume_skills, required_skills)
    print(f"\nSkill Match: {skill_result}")
