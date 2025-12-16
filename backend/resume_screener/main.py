"""
Main Resume Analyzer - Orchestrates all components
"""

from pathlib import Path
from typing import Dict, Any, Optional, Union
import logging

from .models.nlp_models import SemanticMatcher
from .parsers.document_parser import ResumeParser, JobDescriptionParser
from .parsers.skill_extractor import SkillExtractor
from .scoring.scoring_engine import ScoringEngine, ScoreBreakdown, MatchClassifier
from .explainability.explainer import ExplainabilityEngine, Explanation

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class AnalysisResult:
    """Container for analysis results"""
    
    def __init__(self,
                 score: float,
                 classification: str,
                 recommendation: str,
                 score_breakdown: ScoreBreakdown,
                 explanation: Explanation,
                 resume_data: Dict[str, Any],
                 job_data: Dict[str, Any]):
        self.score = score
        self.classification = classification
        self.recommendation = recommendation
        self.score_breakdown = score_breakdown
        self.explanation = explanation
        self.resume_data = resume_data
        self.job_data = job_data
        self.matched_skills = score_breakdown.matched_skills
        self.missing_skills = score_breakdown.missing_skills
    
    def __repr__(self):
        return f"AnalysisResult(score={self.score:.1f}, classification='{self.classification}')"
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            'overall_score': round(self.score, 2),
            'classification': self.classification,
            'recommendation': self.recommendation,
            'confidence': round(self.score_breakdown.confidence, 2),
            'score_breakdown': {
                'semantic_similarity': round(self.score_breakdown.semantic_similarity * 100, 2),
                'skill_match': round(self.score_breakdown.skill_match_score * 100, 2),
                'experience': round(self.score_breakdown.experience_score * 100, 2),
                'education': round(self.score_breakdown.education_score * 100, 2),
                'keyword_match': round(self.score_breakdown.keyword_score * 100, 2)
            },
            'matched_skills': self.matched_skills,
            'missing_skills': self.missing_skills,
            'strengths': self.score_breakdown.strengths,
            'weaknesses': self.score_breakdown.weaknesses,
            'explanation_summary': self.explanation.summary,
            'key_factors': self.explanation.key_factors,
            'improvement_suggestions': self.explanation.improvement_suggestions
        }
    
    def print_summary(self):
        """Print formatted summary"""
        print("\n" + "=" * 80)
        print(f"{'RESUME ANALYSIS SUMMARY':^80}")
        print("=" * 80)
        print(f"\n📊 Overall Score: {self.score:.1f}/100")
        print(f"🏷️  Classification: {self.classification}")
        print(f"💡 Recommendation: {self.recommendation}")
        print(f"\n✅ Matched Skills ({len(self.matched_skills)}): {', '.join(self.matched_skills[:5])}")
        if len(self.matched_skills) > 5:
            print(f"   ... and {len(self.matched_skills) - 5} more")
        print(f"\n❌ Missing Skills ({len(self.missing_skills)}): {', '.join(self.missing_skills[:5])}")
        if len(self.missing_skills) > 5:
            print(f"   ... and {len(self.missing_skills) - 5} more")
        print("\n" + "=" * 80 + "\n")


class ResumeAnalyzer:
    """
    Main Resume Analyzer Class
    Orchestrates document parsing, skill extraction, semantic matching, 
    scoring, and explainability
    """
    
    def __init__(self, 
                 use_sbert: bool = True,
                 use_spacy: bool = True,
                 custom_weights: Optional[Dict[str, float]] = None):
        """
        Initialize Resume Analyzer
        
        Args:
            use_sbert: Use Sentence-BERT for embeddings
            use_spacy: Use spaCy for skill extraction
            custom_weights: Custom scoring weights
        """
        logger.info("Initializing Resume Analyzer...")
        
        # Initialize components
        self.semantic_matcher = SemanticMatcher(use_sbert=use_sbert, use_bert=False)
        self.resume_parser = ResumeParser()
        self.job_parser = JobDescriptionParser()
        self.skill_extractor = SkillExtractor(use_spacy=use_spacy)
        self.scoring_engine = ScoringEngine()
        self.explainer = ExplainabilityEngine()
        
        logger.info("Resume Analyzer initialized successfully")
    
    def analyze(self,
                resume_path: Optional[str] = None,
                resume_text: Optional[str] = None,
                job_description: Optional[str] = None,
                job_path: Optional[str] = None,
                required_skills: Optional[list] = None) -> AnalysisResult:
        """
        Analyze resume against job description
        
        Args:
            resume_path: Path to resume file (PDF, DOCX, TXT)
            resume_text: Resume text (alternative to resume_path)
            job_description: Job description text
            job_path: Path to job description file
            required_skills: Optional list of required skills
            
        Returns:
            AnalysisResult object
        """
        logger.info("Starting resume analysis...")
        
        # Parse resume
        if resume_path:
            logger.info(f"Parsing resume from file: {resume_path}")
            resume_data = self.resume_parser.parse(resume_path)
        elif resume_text:
            logger.info("Using provided resume text")
            resume_data = {'raw_text': resume_text}
        else:
            raise ValueError("Either resume_path or resume_text must be provided")
        
        # Parse job description
        if job_path:
            logger.info(f"Parsing job description from file: {job_path}")
            job_data = self.job_parser.parse(job_path)
        elif job_description:
            logger.info("Using provided job description text")
            job_data = self.job_parser.parse(job_description)
        else:
            raise ValueError("Either job_description or job_path must be provided")
        
        # Extract skills
        logger.info("Extracting skills from resume and job description...")
        resume_skills = self.skill_extractor.extract(resume_data['raw_text'])
        job_skills = required_skills or self.skill_extractor.extract(job_data['raw_text'])
        
        logger.info(f"Found {len(resume_skills)} skills in resume")
        logger.info(f"Found {len(job_skills)} required skills in job description")
        
        # Semantic matching
        logger.info("Computing semantic similarity...")
        semantic_result = self.semantic_matcher.match_resume_to_job(
            resume_data['raw_text'],
            job_data['raw_text']
        )
        semantic_similarity = semantic_result['overall_similarity']
        
        # Skill matching
        logger.info("Matching skills...")
        skill_match_result = self.semantic_matcher.match_skills(
            resume_skills,
            job_skills
        )
        
        # Score experience
        resume_years = resume_data.get('experience_years')
        required_years = self._extract_required_years(job_data['raw_text'])
        experience_score = self.scoring_engine.score_experience(
            resume_years,
            required_years
        )
        
        # Score education
        resume_education = resume_data.get('education', [])
        required_education = self._extract_required_education(job_data['raw_text'])
        education_score = self.scoring_engine.score_education(
            resume_education,
            required_education
        )
        
        # Score keywords
        job_keywords = self._extract_keywords(job_data['raw_text'])
        keyword_score = self.scoring_engine.score_keywords(
            resume_data['raw_text'],
            job_keywords
        )
        
        # Calculate overall score
        logger.info("Calculating overall score...")
        overall_score = self.scoring_engine.calculate_overall_score(
            semantic_similarity=semantic_similarity,
            skill_match_rate=skill_match_result['match_rate'],
            experience_score=experience_score,
            education_score=education_score,
            keyword_score=keyword_score
        )
        
        # Create score breakdown
        score_breakdown = ScoreBreakdown(
            overall_score=overall_score,
            semantic_similarity=semantic_similarity,
            skill_match_score=skill_match_result['match_rate'],
            experience_score=experience_score,
            education_score=education_score,
            keyword_score=keyword_score,
            confidence=self.scoring_engine.calculate_confidence({
                'semantic_similarity': semantic_similarity,
                'skill_match_score': skill_match_result['match_rate'],
                'experience_score': experience_score,
                'education_score': education_score,
                'keyword_score': keyword_score
            }),
            matched_skills=skill_match_result['matched_skills'],
            missing_skills=skill_match_result['missing_skills']
        )
        
        # Add strengths and weaknesses
        strengths, weaknesses = self.scoring_engine.generate_strengths_weaknesses(score_breakdown)
        score_breakdown.strengths = strengths
        score_breakdown.weaknesses = weaknesses
        
        # Generate explanation
        logger.info("Generating explanation...")
        explanation = self.explainer.explain(
            score_breakdown,
            resume_data,
            job_data
        )
        
        # Classify and recommend
        classification = MatchClassifier.classify(overall_score)
        recommendation = MatchClassifier.get_recommendation(
            overall_score,
            score_breakdown.confidence
        )
        
        logger.info(f"Analysis complete. Score: {overall_score:.1f}/100")
        
        return AnalysisResult(
            score=overall_score,
            classification=classification,
            recommendation=recommendation,
            score_breakdown=score_breakdown,
            explanation=explanation,
            resume_data=resume_data,
            job_data=job_data
        )
    
    def batch_analyze(self,
                     resume_paths: list,
                     job_description: str) -> list:
        """
        Analyze multiple resumes against one job description
        
        Args:
            resume_paths: List of resume file paths
            job_description: Job description text
            
        Returns:
            List of AnalysisResult objects, sorted by score
        """
        logger.info(f"Starting batch analysis of {len(resume_paths)} resumes...")
        
        results = []
        for i, resume_path in enumerate(resume_paths, 1):
            logger.info(f"Analyzing resume {i}/{len(resume_paths)}: {resume_path}")
            try:
                result = self.analyze(
                    resume_path=resume_path,
                    job_description=job_description
                )
                results.append(result)
            except Exception as e:
                logger.error(f"Error analyzing {resume_path}: {str(e)}")
                continue
        
        # Sort by score (descending)
        results.sort(key=lambda x: x.score, reverse=True)
        
        logger.info("Batch analysis complete")
        return results
    
    @staticmethod
    def _extract_required_years(job_text: str) -> Optional[float]:
        """Extract required years of experience from job description"""
        import re
        pattern = r'(\d+)\+?\s*years?\s+(?:of\s+)?experience'
        match = re.search(pattern, job_text, re.IGNORECASE)
        if match:
            return float(match.group(1))
        return None
    
    @staticmethod
    def _extract_required_education(job_text: str) -> Optional[str]:
        """Extract education requirements from job description"""
        education_keywords = ['Bachelor', 'Master', 'PhD', 'Doctorate', 'degree']
        job_lower = job_text.lower()
        
        for keyword in education_keywords:
            if keyword.lower() in job_lower:
                return keyword
        return None
    
    @staticmethod
    def _extract_keywords(text: str, top_n: int = 20) -> list:
        """Extract important keywords from text"""
        import re
        from collections import Counter
        
        # Remove common words
        stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 
                     'for', 'of', 'with', 'is', 'are', 'was', 'were', 'be', 'been'}
        
        # Extract words
        words = re.findall(r'\b[a-z]{3,}\b', text.lower())
        words = [w for w in words if w not in stop_words]
        
        # Count frequency
        counter = Counter(words)
        return [word for word, _ in counter.most_common(top_n)]


if __name__ == "__main__":
    # Example usage
    print("Resume Analyzer Test")
    
    analyzer = ResumeAnalyzer()
    
    # Sample data
    sample_resume = """
    John Doe
    Software Engineer
    john.doe@email.com
    
    EXPERIENCE
    Senior Software Engineer at TechCorp (2019-Present)
    - 5 years of Python development experience
    - Built REST APIs using Django and Flask
    - Deployed applications on AWS using Docker
    
    EDUCATION
    Master of Science in Computer Science
    
    SKILLS
    Python, Django, Flask, JavaScript, Docker, PostgreSQL, Git
    """
    
    sample_job = """
    Senior Python Developer
    
    We're looking for an experienced Python developer with 4+ years of experience.
    
    Requirements:
    - Strong Python programming skills
    - Experience with Django or Flask
    - Knowledge of Docker and AWS
    - Database experience (PostgreSQL preferred)
    - REST API development
    - Bachelor's degree in Computer Science or related field
    
    Nice to have:
    - Kubernetes experience
    - React or Vue.js
    - CI/CD pipelines
    """
    
    # Analyze
    result = analyzer.analyze(
        resume_text=sample_resume,
        job_description=sample_job
    )
    
    # Print results
    result.print_summary()
    
    print("\n📋 Detailed Explanation:")
    print(analyzer.explainer.generate_report(result.explanation))
