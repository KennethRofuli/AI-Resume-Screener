"""
Explainability Module for Resume Screening
Provides detailed explanations for matching results
"""

from typing import Dict, List, Any
from dataclasses import dataclass
import logging

from ..scoring.scoring_engine import ScoreBreakdown

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class Explanation:
    """Structured explanation of matching results"""
    summary: str
    detailed_analysis: Dict[str, str]
    recommendations: List[str]
    key_factors: List[str]
    improvement_suggestions: List[str]


class ExplainabilityEngine:
    """Generate human-readable explanations for matching results"""
    
    def __init__(self):
        """Initialize explainability engine"""
        pass
    
    def explain(self, score_breakdown: ScoreBreakdown,
                resume_data: Dict[str, Any],
                job_data: Dict[str, Any]) -> Explanation:
        """
        Generate comprehensive explanation
        
        Args:
            score_breakdown: Scoring breakdown
            resume_data: Parsed resume data
            job_data: Parsed job data
            
        Returns:
            Explanation object
        """
        # Generate summary
        summary = self._generate_summary(score_breakdown)
        
        # Detailed component analysis
        detailed_analysis = self._analyze_components(score_breakdown)
        
        # Generate recommendations
        recommendations = self._generate_recommendations(score_breakdown)
        
        # Identify key factors
        key_factors = self._identify_key_factors(score_breakdown)
        
        # Improvement suggestions
        improvements = self._suggest_improvements(
            score_breakdown, 
            resume_data, 
            job_data
        )
        
        return Explanation(
            summary=summary,
            detailed_analysis=detailed_analysis,
            recommendations=recommendations,
            key_factors=key_factors,
            improvement_suggestions=improvements
        )
    
    def _generate_summary(self, score_breakdown: ScoreBreakdown) -> str:
        """Generate executive summary"""
        score = score_breakdown.overall_score
        confidence = score_breakdown.confidence
        
        # Determine match quality
        if score >= 85:
            quality = "excellent"
            verb = "strongly matches"
        elif score >= 70:
            quality = "strong"
            verb = "matches well with"
        elif score >= 55:
            quality = "moderate"
            verb = "partially matches"
        else:
            quality = "weak"
            verb = "does not strongly match"
        
        confidence_text = "high" if confidence >= 0.7 else "moderate" if confidence >= 0.5 else "low"
        
        summary = (
            f"This resume {verb} the job requirements with an overall score of "
            f"{score:.1f}/100 ({quality} match). "
            f"Confidence in this assessment is {confidence_text} ({confidence*100:.0f}%)."
        )
        
        # Add context about strengths
        if score_breakdown.strengths:
            summary += f" Key strengths: {score_breakdown.strengths[0]}"
        
        return summary
    
    def _analyze_components(self, score_breakdown: ScoreBreakdown) -> Dict[str, str]:
        """Analyze each scoring component"""
        analysis = {}
        
        # Semantic Similarity
        sem_score = score_breakdown.semantic_similarity * 100
        if sem_score >= 80:
            analysis['Semantic Match'] = (
                f"Excellent alignment ({sem_score:.1f}%). The resume content closely "
                "matches the job description's requirements and terminology."
            )
        elif sem_score >= 60:
            analysis['Semantic Match'] = (
                f"Good alignment ({sem_score:.1f}%). The resume addresses most job "
                "requirements with relevant experience and skills."
            )
        else:
            analysis['Semantic Match'] = (
                f"Limited alignment ({sem_score:.1f}%). The resume content differs "
                "significantly from what the job description requires."
            )
        
        # Skill Match
        skill_score = score_breakdown.skill_match_score * 100
        matched_count = len(score_breakdown.matched_skills)
        missing_count = len(score_breakdown.missing_skills)
        
        if skill_score >= 80:
            analysis['Skills'] = (
                f"Strong skill match ({skill_score:.1f}%). {matched_count} key skills "
                f"matched. {self._format_skill_list(score_breakdown.matched_skills[:5])}"
            )
        elif skill_score >= 50:
            analysis['Skills'] = (
                f"Partial skill match ({skill_score:.1f}%). {matched_count} skills matched, "
                f"but {missing_count} required skills are missing: "
                f"{self._format_skill_list(score_breakdown.missing_skills[:5])}"
            )
        else:
            analysis['Skills'] = (
                f"Weak skill match ({skill_score:.1f}%). Most required skills are missing: "
                f"{self._format_skill_list(score_breakdown.missing_skills[:5])}"
            )
        
        # Experience
        exp_score = score_breakdown.experience_score * 100
        if exp_score >= 90:
            analysis['Experience'] = (
                f"Meets or exceeds experience requirements ({exp_score:.1f}%)."
            )
        elif exp_score >= 70:
            analysis['Experience'] = (
                f"Adequate experience level ({exp_score:.1f}%), though may be "
                "slightly below optimal."
            )
        else:
            analysis['Experience'] = (
                f"Experience level may be insufficient ({exp_score:.1f}%)."
            )
        
        # Education
        edu_score = score_breakdown.education_score * 100
        if edu_score >= 90:
            analysis['Education'] = f"Meets education requirements ({edu_score:.1f}%)."
        elif edu_score >= 70:
            analysis['Education'] = (
                f"Education level is close to requirements ({edu_score:.1f}%)."
            )
        else:
            analysis['Education'] = (
                f"Education level may not meet requirements ({edu_score:.1f}%)."
            )
        
        return analysis
    
    def _generate_recommendations(self, score_breakdown: ScoreBreakdown) -> List[str]:
        """Generate actionable recommendations"""
        recommendations = []
        score = score_breakdown.overall_score
        
        if score >= 85:
            recommendations.append(
                "✅ Highly recommend scheduling an interview - strong candidate"
            )
            recommendations.append(
                "Focus interview on validating top skills and cultural fit"
            )
        elif score >= 70:
            recommendations.append(
                "✅ Recommend phone screening to assess fit"
            )
            recommendations.append(
                "Verify experience with missing skills during interview"
            )
        elif score >= 55:
            recommendations.append(
                "⚠️ Consider if willing to train on missing skills"
            )
            recommendations.append(
                "May be suitable for junior/mid-level variant of role"
            )
        else:
            recommendations.append(
                "❌ Not recommended for this position"
            )
            recommendations.append(
                "Significant gaps in required qualifications"
            )
        
        # Add specific recommendations based on weaknesses
        if score_breakdown.missing_skills:
            recommendations.append(
                f"Address skill gaps: {', '.join(score_breakdown.missing_skills[:3])}"
            )
        
        return recommendations
    
    def _identify_key_factors(self, score_breakdown: ScoreBreakdown) -> List[str]:
        """Identify factors most influencing the score"""
        factors = []
        
        # Add positive factors
        if score_breakdown.skill_match_score >= 0.8:
            factors.append(f"✓ Strong skill alignment ({len(score_breakdown.matched_skills)} matches)")
        
        if score_breakdown.semantic_similarity >= 0.8:
            factors.append("✓ Excellent semantic match with job description")
        
        if score_breakdown.experience_score >= 0.9:
            factors.append("✓ Meets experience requirements")
        
        # Add negative factors
        if score_breakdown.skill_match_score < 0.5:
            factors.append(f"✗ Missing critical skills ({len(score_breakdown.missing_skills)} gaps)")
        
        if score_breakdown.semantic_similarity < 0.5:
            factors.append("✗ Resume content differs from job requirements")
        
        if score_breakdown.experience_score < 0.7:
            factors.append("✗ May lack required experience level")
        
        return factors
    
    def _suggest_improvements(self,
                            score_breakdown: ScoreBreakdown,
                            resume_data: Dict[str, Any],
                            job_data: Dict[str, Any]) -> List[str]:
        """Suggest resume improvements"""
        suggestions = []
        
        # Skill-based suggestions
        if score_breakdown.missing_skills:
            missing_top = score_breakdown.missing_skills[:3]
            suggestions.append(
                f"💡 Add these skills if applicable: {', '.join(missing_top)}"
            )
            suggestions.append(
                "💡 Highlight projects demonstrating these missing skills"
            )
        
        # Semantic match suggestions
        if score_breakdown.semantic_similarity < 0.7:
            suggestions.append(
                "💡 Tailor resume language to better match job description terminology"
            )
            suggestions.append(
                "💡 Add keywords and phrases from the job posting"
            )
        
        # Experience suggestions
        if score_breakdown.experience_score < 0.8:
            suggestions.append(
                "💡 Emphasize relevant experience more prominently"
            )
            suggestions.append(
                "💡 Quantify achievements with metrics and impact"
            )
        
        # General suggestions
        if score_breakdown.overall_score < 70:
            suggestions.append(
                "💡 Consider adding a summary section targeting this role"
            )
            suggestions.append(
                "💡 Reorganize to prioritize most relevant experience"
            )
        
        return suggestions
    
    @staticmethod
    def _format_skill_list(skills: List[str]) -> str:
        """Format skill list for display"""
        if not skills:
            return "none"
        if len(skills) <= 3:
            return ", ".join(skills)
        return ", ".join(skills[:3]) + f" (and {len(skills)-3} more)"
    
    def generate_report(self, explanation: Explanation) -> str:
        """
        Generate formatted text report
        
        Args:
            explanation: Explanation object
            
        Returns:
            Formatted report string
        """
        report = []
        
        report.append("=" * 80)
        report.append("RESUME SCREENING REPORT")
        report.append("=" * 80)
        report.append("")
        
        # Summary
        report.append("SUMMARY")
        report.append("-" * 80)
        report.append(explanation.summary)
        report.append("")
        
        # Key Factors
        report.append("KEY FACTORS")
        report.append("-" * 80)
        for factor in explanation.key_factors:
            report.append(f"  {factor}")
        report.append("")
        
        # Detailed Analysis
        report.append("DETAILED ANALYSIS")
        report.append("-" * 80)
        for component, analysis in explanation.detailed_analysis.items():
            report.append(f"\n{component}:")
            report.append(f"  {analysis}")
        report.append("")
        
        # Recommendations
        report.append("RECOMMENDATIONS")
        report.append("-" * 80)
        for rec in explanation.recommendations:
            report.append(f"  {rec}")
        report.append("")
        
        # Improvement Suggestions
        if explanation.improvement_suggestions:
            report.append("IMPROVEMENT SUGGESTIONS")
            report.append("-" * 80)
            for suggestion in explanation.improvement_suggestions:
                report.append(f"  {suggestion}")
            report.append("")
        
        report.append("=" * 80)
        
        return "\n".join(report)


if __name__ == "__main__":
    # Test explainability engine
    from ..scoring.scoring_engine import ScoreBreakdown
    
    print("Testing Explainability Engine...")
    
    # Create sample score breakdown
    breakdown = ScoreBreakdown(
        overall_score=78.5,
        semantic_similarity=0.82,
        skill_match_score=0.75,
        experience_score=0.85,
        education_score=1.0,
        keyword_score=0.70,
        confidence=0.8,
        matched_skills=['Python', 'Django', 'Docker'],
        missing_skills=['AWS', 'Kubernetes'],
        strengths=['Strong skill alignment', 'Excellent semantic match'],
        weaknesses=['Missing cloud experience']
    )
    
    engine = ExplainabilityEngine()
    explanation = engine.explain(
        breakdown,
        resume_data={},
        job_data={}
    )
    
    # Generate report
    report = engine.generate_report(explanation)
    print(report)
