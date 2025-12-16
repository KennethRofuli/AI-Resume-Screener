"""
Enhanced Explainability Module with Detailed Analysis
Provides skill importance, ATS compatibility, learning resources, and industry benchmarking
"""

from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field
import re
import logging

from ..scoring.scoring_engine import ScoreBreakdown

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class SkillAnalysis:
    """Detailed analysis for a specific skill"""
    skill_name: str
    is_matched: bool
    importance: str  # "Critical", "Important", "Beneficial"
    reason: str
    market_demand: str  # "High demand", "Growing", "Stable", "Declining"
    learning_resources: List[str] = field(default_factory=list)
    estimated_learning_time: Optional[str] = None


@dataclass
class ATSCompatibility:
    """ATS (Applicant Tracking System) compatibility analysis"""
    overall_score: float  # 0-100
    is_ats_friendly: bool
    issues: List[str] = field(default_factory=list)
    recommendations: List[str] = field(default_factory=list)
    formatting_score: float = 0.0
    keyword_optimization: float = 0.0


@dataclass
class EnhancedExplanation:
    """Comprehensive explanation with detailed insights"""
    summary: str
    score_explanations: Dict[str, str]
    skill_analysis: List[SkillAnalysis]
    ats_compatibility: ATSCompatibility
    career_insights: Dict[str, Any]
    recommendations: List[str]
    learning_roadmap: List[Dict[str, Any]]
    industry_benchmark: Dict[str, Any]


class EnhancedExplainabilityEngine:
    """Advanced explainability with detailed skill analysis and ATS checking"""
    
    # Skill importance database based on common job requirements
    SKILL_IMPORTANCE = {
        # Programming Languages
        'python': {'importance': 'Critical', 'demand': 'High demand', 'learning_time': '3-6 months'},
        'java': {'importance': 'Critical', 'demand': 'High demand', 'learning_time': '3-6 months'},
        'javascript': {'importance': 'Critical', 'demand': 'High demand', 'learning_time': '2-4 months'},
        'typescript': {'importance': 'Important', 'demand': 'Growing', 'learning_time': '1-2 months'},
        'c': {'importance': 'Critical', 'demand': 'Stable', 'learning_time': '4-8 months'},
        'c++': {'importance': 'Critical', 'demand': 'Stable', 'learning_time': '4-8 months'},
        'golang': {'importance': 'Important', 'demand': 'Growing', 'learning_time': '2-3 months'},
        'go': {'importance': 'Important', 'demand': 'Growing', 'learning_time': '2-3 months'},
        'rust': {'importance': 'Important', 'demand': 'Growing', 'learning_time': '4-6 months'},
        'ruby': {'importance': 'Important', 'demand': 'Stable', 'learning_time': '2-3 months'},
        'php': {'importance': 'Important', 'demand': 'Stable', 'learning_time': '2-3 months'},
        'swift': {'importance': 'Important', 'demand': 'Stable', 'learning_time': '3-4 months'},
        'kotlin': {'importance': 'Important', 'demand': 'Growing', 'learning_time': '2-3 months'},
        
        # Databases
        'sql': {'importance': 'Critical', 'demand': 'High demand', 'learning_time': '2-3 months'},
        'postgresql': {'importance': 'Important', 'demand': 'High demand', 'learning_time': '1-2 months'},
        'mysql': {'importance': 'Important', 'demand': 'High demand', 'learning_time': '1-2 months'},
        'mongodb': {'importance': 'Important', 'demand': 'Growing', 'learning_time': '1-2 months'},
        'redis': {'importance': 'Important', 'demand': 'Growing', 'learning_time': '1 month'},
        'oracle': {'importance': 'Important', 'demand': 'Stable', 'learning_time': '2-3 months'},
        
        # Cloud & DevOps
        'aws': {'importance': 'Critical', 'demand': 'High demand', 'learning_time': '3-6 months'},
        'azure': {'importance': 'Critical', 'demand': 'High demand', 'learning_time': '3-6 months'},
        'gcp': {'importance': 'Important', 'demand': 'Growing', 'learning_time': '3-6 months'},
        'docker': {'importance': 'Critical', 'demand': 'High demand', 'learning_time': '1-2 months'},
        'kubernetes': {'importance': 'Critical', 'demand': 'High demand', 'learning_time': '2-4 months'},
        'terraform': {'importance': 'Important', 'demand': 'Growing', 'learning_time': '1-2 months'},
        'jenkins': {'importance': 'Important', 'demand': 'Stable', 'learning_time': '1 month'},
        'ci/cd': {'importance': 'Important', 'demand': 'High demand', 'learning_time': '1-2 months'},
        
        # Web & Frameworks
        'react': {'importance': 'Critical', 'demand': 'High demand', 'learning_time': '2-3 months'},
        'angular': {'importance': 'Important', 'demand': 'Stable', 'learning_time': '2-3 months'},
        'vue': {'importance': 'Important', 'demand': 'Growing', 'learning_time': '1-2 months'},
        'node.js': {'importance': 'Critical', 'demand': 'High demand', 'learning_time': '2-3 months'},
        'django': {'importance': 'Important', 'demand': 'Stable', 'learning_time': '2-3 months'},
        'flask': {'importance': 'Important', 'demand': 'Stable', 'learning_time': '1-2 months'},
        'spring': {'importance': 'Critical', 'demand': 'High demand', 'learning_time': '2-4 months'},
        'express': {'importance': 'Important', 'demand': 'High demand', 'learning_time': '1-2 months'},
        
        # Data & AI
        'machine learning': {'importance': 'Critical', 'demand': 'High demand', 'learning_time': '6-12 months'},
        'deep learning': {'importance': 'Important', 'demand': 'High demand', 'learning_time': '6-12 months'},
        'tensorflow': {'importance': 'Important', 'demand': 'High demand', 'learning_time': '3-6 months'},
        'pytorch': {'importance': 'Important', 'demand': 'High demand', 'learning_time': '3-6 months'},
        'data analysis': {'importance': 'Critical', 'demand': 'High demand', 'learning_time': '3-6 months'},
        'pandas': {'importance': 'Important', 'demand': 'High demand', 'learning_time': '1-2 months'},
        'numpy': {'importance': 'Important', 'demand': 'High demand', 'learning_time': '1-2 months'},
        
        # Specialized
        'voip': {'importance': 'Critical', 'demand': 'Stable', 'learning_time': '3-6 months'},
        'sip': {'importance': 'Critical', 'demand': 'Stable', 'learning_time': '2-3 months'},
        'rtp': {'importance': 'Important', 'demand': 'Stable', 'learning_time': '1-2 months'},
        'webrtc': {'importance': 'Important', 'demand': 'Growing', 'learning_time': '2-3 months'},
        
        # Soft Skills
        'leadership': {'importance': 'Important', 'demand': 'High demand', 'learning_time': '6-12 months'},
        'mentoring': {'importance': 'Important', 'demand': 'High demand', 'learning_time': '3-6 months'},
        'communication': {'importance': 'Critical', 'demand': 'High demand', 'learning_time': 'Ongoing'},
        'problem solving': {'importance': 'Critical', 'demand': 'High demand', 'learning_time': 'Ongoing'},
    }
    
    # Learning resources database
    LEARNING_RESOURCES = {
        'python': [
            'Python.org Official Tutorial (Free)',
            'Real Python (realPython.com)',
            'Python for Everybody (Coursera - Free)',
            'Automate the Boring Stuff (Free eBook)'
        ],
        'golang': [
            'Tour of Go (tour.golang.org - Free)',
            'Go by Example (gobyexample.com - Free)',
            'Effective Go (golang.org/doc/effective_go - Free)',
            'Go Web Development (Udemy)'
        ],
        'go': [
            'Tour of Go (tour.golang.org - Free)',
            'Go by Example (gobyexample.com - Free)',
            'Effective Go (golang.org/doc/effective_go - Free)'
        ],
        'c': [
            'C Programming Language (Book by K&R)',
            'CS50 Introduction to Computer Science (edX - Free)',
            'Learn-C.org (Interactive - Free)',
            'The C Programming Language (Coursera)'
        ],
        'sql': [
            'SQLBolt (sqlbolt.com - Free)',
            'Mode SQL Tutorial (mode.com/sql-tutorial - Free)',
            'W3Schools SQL (Free)',
            'SQL for Data Science (Coursera)'
        ],
        'postgresql': [
            'PostgreSQL Documentation (Free)',
            'PostgreSQL Tutorial (postgresqltutorial.com - Free)',
            'The Art of PostgreSQL (Book)',
            'Database Design and PostgreSQL (Udemy)'
        ],
        'voip': [
            'VoIP Fundamentals (Cisco - Free)',
            'SIP School (sipschool.com - Free)',
            'VoIP Technologies (LinkedIn Learning)',
            'Kamailio Documentation (Free)'
        ],
        'sip': [
            'SIP: Understanding the Session Initiation Protocol (Book)',
            'SIP School (sipschool.com - Free)',
            'RFC 3261 - SIP Specification (Free)',
            'Practical SIP (Udemy)'
        ],
        'docker': [
            'Docker Get Started (docs.docker.com - Free)',
            'Docker Deep Dive (Book)',
            'Docker Mastery (Udemy)',
            'Play with Docker (labs.play-with-docker.com - Free)'
        ],
        'kubernetes': [
            'Kubernetes Documentation (Free)',
            'Kubernetes Basics (kubernetes.io/docs - Free)',
            'Certified Kubernetes Administrator (CNCF)',
            'Kubernetes the Hard Way (GitHub - Free)'
        ],
        'aws': [
            'AWS Training and Certification (Free tier)',
            'AWS Certified Solutions Architect (Official)',
            'A Cloud Guru (Subscription)',
            'AWS Documentation (Free)'
        ],
        'react': [
            'React Documentation (react.dev - Free)',
            'React for Beginners (Free)',
            'Full Stack Open (fullstackopen.com - Free)',
            'Epic React (epicreact.dev)'
        ],
        'machine learning': [
            'Machine Learning by Andrew Ng (Coursera)',
            'fast.ai Practical Deep Learning (Free)',
            'Hands-On Machine Learning (Book)',
            'Google Machine Learning Crash Course (Free)'
        ],
    }
    
    def __init__(self):
        """Initialize enhanced explainability engine"""
        pass
    
    def explain(self, 
                score_breakdown: ScoreBreakdown,
                resume_data: Dict[str, Any],
                job_data: Dict[str, Any],
                resume_text: Optional[str] = None) -> EnhancedExplanation:
        """
        Generate comprehensive explanation with detailed insights
        
        Args:
            score_breakdown: Scoring breakdown
            resume_data: Parsed resume data
            job_data: Parsed job data
            resume_text: Raw resume text for ATS checking
            
        Returns:
            EnhancedExplanation object
        """
        # Generate summary
        summary = self._generate_enhanced_summary(score_breakdown)
        
        # Explain each score component in detail
        score_explanations = self._explain_score_components(score_breakdown)
        
        # Detailed skill analysis
        skill_analysis = self._analyze_skills_detailed(
            score_breakdown.matched_skills,
            score_breakdown.missing_skills,
            job_data
        )
        
        # ATS compatibility check
        ats_compat = self._check_ats_compatibility(
            resume_text or resume_data.get('text', ''),
            resume_data,
            job_data
        )
        
        # Career insights
        career_insights = self._generate_career_insights(
            score_breakdown,
            resume_data,
            job_data
        )
        
        # Recommendations
        recommendations = self._generate_detailed_recommendations(
            score_breakdown,
            skill_analysis,
            ats_compat
        )
        
        # Learning roadmap
        learning_roadmap = self._create_learning_roadmap(skill_analysis)
        
        # Industry benchmark
        industry_benchmark = self._generate_benchmark(score_breakdown)
        
        return EnhancedExplanation(
            summary=summary,
            score_explanations=score_explanations,
            skill_analysis=skill_analysis,
            ats_compatibility=ats_compat,
            career_insights=career_insights,
            recommendations=recommendations,
            learning_roadmap=learning_roadmap,
            industry_benchmark=industry_benchmark
        )
    
    def _generate_enhanced_summary(self, score_breakdown: ScoreBreakdown) -> str:
        """Generate detailed executive summary"""
        score = score_breakdown.overall_score
        confidence = score_breakdown.confidence
        
        if score >= 85:
            quality = "exceptional"
            action = "This candidate should be prioritized for immediate interview."
        elif score >= 70:
            quality = "strong"
            action = "This candidate is well-qualified and recommended for interview."
        elif score >= 60:
            quality = "moderate"
            action = "This candidate may be suitable depending on team needs and other applicants."
        elif score >= 50:
            quality = "fair"
            action = "This candidate has some relevant experience but significant gaps exist."
        else:
            quality = "weak"
            action = "This candidate does not meet the minimum requirements for this role."
        
        confidence_text = "high" if confidence >= 0.7 else "moderate" if confidence >= 0.5 else "low"
        
        summary = (
            f"**Overall Assessment:** {quality.upper()} match ({score:.1f}/100) with "
            f"{confidence_text} confidence ({confidence*100:.0f}%).\n\n"
            f"{action}\n\n"
        )
        
        if score_breakdown.strengths:
            summary += f"**Key Strengths:** {', '.join(score_breakdown.strengths[:3])}\n\n"
        
        if score_breakdown.weaknesses:
            summary += f"**Areas of Concern:** {', '.join(score_breakdown.weaknesses[:3])}"
        
        return summary
    
    def _explain_score_components(self, score_breakdown: ScoreBreakdown) -> Dict[str, str]:
        """Explain what each score component means"""
        explanations = {}
        
        # Semantic Similarity (30%)
        sem_score = score_breakdown.semantic_similarity * 100
        explanations['Semantic Similarity (30% weight)'] = (
            f"**Score: {sem_score:.1f}/100**\n\n"
            f"**What this measures:** How well the overall content and context of the resume "
            f"matches the job description using AI language understanding. This goes beyond "
            f"keyword matching to understand meaning and relevance.\n\n"
            f"**What it means:** "
        )
        
        if sem_score >= 80:
            explanations['Semantic Similarity (30% weight)'] += (
                "Excellent alignment! The resume demonstrates experience and language that "
                "closely matches what the employer is looking for. The candidate speaks the "
                "same 'language' as the job requirements."
            )
        elif sem_score >= 60:
            explanations['Semantic Similarity (30% weight)'] += (
                "Good alignment. The resume addresses most requirements with relevant experience, "
                "though some areas could be better articulated using job description terminology."
            )
        else:
            explanations['Semantic Similarity (30% weight)'] += (
                "Limited alignment. The resume content differs significantly from job requirements. "
                "Consider rephrasing experience to better match the role's language and focus areas."
            )
        
        # Skill Match (35%)
        skill_score = score_breakdown.skill_match_score * 100
        matched_count = len(score_breakdown.matched_skills)
        total_required = matched_count + len(score_breakdown.missing_skills)
        
        explanations['Skill Match (35% weight)'] = (
            f"**Score: {skill_score:.1f}/100** ({matched_count}/{total_required} required skills)\n\n"
            f"**What this measures:** Percentage of required technical and soft skills present "
            f"in the resume.\n\n"
            f"**What it means:** "
        )
        
        if skill_score >= 80:
            explanations['Skill Match (35% weight)'] += (
                f"Excellent! {matched_count} of {total_required} required skills matched. "
                "This candidate has most of the technical capabilities needed for this role."
            )
        elif skill_score >= 50:
            explanations['Skill Match (35% weight)'] += (
                f"Partial match. {matched_count} of {total_required} skills found. "
                f"Missing {len(score_breakdown.missing_skills)} key skills that should be "
                "developed or added to resume if possessed."
            )
        else:
            explanations['Skill Match (35% weight)'] += (
                f"Weak match. Only {matched_count} of {total_required} required skills found. "
                "Significant skill gaps exist for this particular role."
            )
        
        # Experience (20%)
        exp_score = score_breakdown.experience_score * 100
        explanations['Experience Level (20% weight)'] = (
            f"**Score: {exp_score:.1f}/100**\n\n"
            f"**What this measures:** Years of relevant professional experience and career progression.\n\n"
            f"**What it means:** "
        )
        
        if exp_score >= 80:
            explanations['Experience Level (20% weight)'] += (
                "Strong experience match! The candidate has the required years of experience "
                "and demonstrates career growth."
            )
        elif exp_score >= 50:
            explanations['Experience Level (20% weight)'] += (
                "Moderate experience. The candidate may have slightly less experience than ideal, "
                "but could still be viable depending on skill strength."
            )
        else:
            explanations['Experience Level (20% weight)'] += (
                "Limited experience for this role. The position may require more years or "
                "more senior-level experience than currently demonstrated."
            )
        
        # Education (10%)
        edu_score = score_breakdown.education_score * 100
        explanations['Education (10% weight)'] = (
            f"**Score: {edu_score:.1f}/100**\n\n"
            f"**What this measures:** Educational background alignment with job requirements.\n\n"
            f"**What it means:** "
        )
        
        if edu_score >= 80:
            explanations['Education (10% weight)'] += (
                "Education requirements met. The candidate has the appropriate educational background."
            )
        elif edu_score >= 30:
            explanations['Education (10% weight)'] += (
                "Education information present but may not perfectly match requirements. "
                "Experience can often compensate for educational differences."
            )
        else:
            explanations['Education (10% weight)'] += (
                "Education section unclear or missing. If you have relevant education, "
                "ensure it's prominently listed."
            )
        
        # Keywords (5%)
        kw_score = score_breakdown.keyword_score * 100
        explanations['Keyword Match (5% weight)'] = (
            f"**Score: {kw_score:.1f}/100**\n\n"
            f"**What this measures:** Presence of exact keywords from job description (important for ATS systems).\n\n"
            f"**What it means:** "
        )
        
        if kw_score >= 70:
            explanations['Keyword Match (5% weight)'] += (
                "Good keyword optimization. Resume uses terminology from the job description "
                "that will help it pass automated screening systems (ATS)."
            )
        elif kw_score >= 40:
            explanations['Keyword Match (5% weight)'] += (
                "Moderate keyword usage. Consider incorporating more exact phrases from the "
                "job description to improve ATS compatibility."
            )
        else:
            explanations['Keyword Match (5% weight)'] += (
                "Low keyword match. Resume may struggle with automated screening systems. "
                "Add more specific keywords from the job posting."
            )
        
        return explanations
    
    def _analyze_skills_detailed(self,
                                 matched_skills: List[str],
                                 missing_skills: List[str],
                                 job_data: Dict[str, Any]) -> List[SkillAnalysis]:
        """Create detailed analysis for each skill"""
        analyses = []
        
        # Analyze matched skills
        for skill in matched_skills:
            skill_lower = skill.lower()
            skill_info = self.SKILL_IMPORTANCE.get(skill_lower, {
                'importance': 'Important',
                'demand': 'Stable',
                'learning_time': 'Varies'
            })
            
            analyses.append(SkillAnalysis(
                skill_name=skill,
                is_matched=True,
                importance=skill_info['importance'],
                reason=f"✅ You have this skill - great! This is {skill_info['importance'].lower()} "
                       f"for the role and shows {skill_info['demand'].lower()} in the job market.",
                market_demand=skill_info['demand'],
                learning_resources=[],
                estimated_learning_time=None
            ))
        
        # Analyze missing skills with learning resources
        for skill in missing_skills:
            skill_lower = skill.lower()
            skill_info = self.SKILL_IMPORTANCE.get(skill_lower, {
                'importance': 'Important',
                'demand': 'Stable',
                'learning_time': 'Varies'
            })
            
            resources = self.LEARNING_RESOURCES.get(skill_lower, [
                f'Search for "{skill} tutorial" on YouTube or Udemy',
                f'Check {skill} documentation',
                f'FreeCodeCamp or Codecademy for {skill}'
            ])
            
            reason = self._generate_skill_missing_reason(skill, skill_info)
            
            analyses.append(SkillAnalysis(
                skill_name=skill,
                is_matched=False,
                importance=skill_info['importance'],
                reason=reason,
                market_demand=skill_info['demand'],
                learning_resources=resources,
                estimated_learning_time=skill_info['learning_time']
            ))
        
        # Sort by importance (Critical first)
        importance_order = {'Critical': 0, 'Important': 1, 'Beneficial': 2}
        analyses.sort(key=lambda x: (not x.is_matched, importance_order.get(x.importance, 3)))
        
        return analyses
    
    def _generate_skill_missing_reason(self, skill: str, skill_info: Dict) -> str:
        """Generate explanation for why a missing skill matters"""
        importance = skill_info['importance']
        demand = skill_info['demand']
        
        if importance == 'Critical':
            return (
                f"❌ **CRITICAL SKILL MISSING** - {skill} is essential for this role. "
                f"This skill is in {demand.lower()} and is likely required for day-to-day tasks. "
                f"**Priority: HIGH** - Address this gap immediately."
            )
        elif importance == 'Important':
            return (
                f"⚠️ **Important skill missing** - {skill} is strongly preferred for this position. "
                f"Market demand: {demand}. While not mandatory, having this skill would "
                f"significantly strengthen your application. **Priority: MEDIUM**"
            )
        else:
            return (
                f"ℹ️ **Beneficial skill** - {skill} would be nice to have but isn't essential. "
                f"Market trend: {demand}. **Priority: LOW**"
            )
    
    def _check_ats_compatibility(self,
                                 resume_text: str,
                                 resume_data: Dict[str, Any],
                                 job_data: Dict[str, Any]) -> ATSCompatibility:
        """
        Check if resume is ATS (Applicant Tracking System) friendly
        """
        issues = []
        recommendations = []
        formatting_score = 100.0
        
        # Check for problematic formatting
        if not resume_text:
            issues.append("Unable to parse resume text")
            formatting_score -= 50
        
        # Check for tables (ATS systems often struggle with these)
        if '|' in resume_text or '\t\t' in resume_text:
            issues.append("Resume may contain tables - ATS systems often have trouble parsing these")
            recommendations.append("Convert tables to simple bullet points or lists")
            formatting_score -= 15
        
        # Check for images/graphics indicators
        if len(resume_text) < 100:
            issues.append("Very little text detected - resume may be image-based or heavily formatted")
            recommendations.append("Ensure resume is text-based, not image-based (no scanned documents)")
            formatting_score -= 30
        
        # Check for standard sections
        standard_sections = ['experience', 'education', 'skills']
        resume_lower = resume_text.lower()
        missing_sections = []
        
        for section in standard_sections:
            if section not in resume_lower:
                missing_sections.append(section.title())
        
        if missing_sections:
            issues.append(f"Standard sections may be missing or not clearly labeled: {', '.join(missing_sections)}")
            recommendations.append(f"Add clear section headers: {', '.join(missing_sections)}")
            formatting_score -= (len(missing_sections) * 10)
        
        # Check for headers/footers (can confuse ATS)
        lines = resume_text.split('\n')
        if len(lines) > 5:
            # Check if first/last lines repeat (possible header/footer)
            if lines[0] == lines[-1]:
                issues.append("Possible header/footer detected - may confuse ATS")
                recommendations.append("Remove headers and footers, or use simple text only")
                formatting_score -= 10
        
        # Check for special characters
        special_chars = ['§', '©', '®', '™', '•']
        found_special = [char for char in special_chars if char in resume_text]
        if found_special:
            issues.append(f"Special characters found: {', '.join(found_special)} - may not parse correctly")
            recommendations.append("Replace special characters with standard text (e.g., (C) instead of ©)")
            formatting_score -= 5
        
        # Check for file format indicators (if available)
        # Note: This would require file metadata, assuming good format for now
        
        # Check keyword optimization
        job_skills = job_data.get('skills', [])
        job_text_lower = job_data.get('text', '').lower()
        keywords_found = sum(1 for skill in job_skills if skill.lower() in resume_lower)
        keyword_optimization = (keywords_found / len(job_skills) * 100) if job_skills else 50
        
        if keyword_optimization < 50:
            issues.append(f"Only {keywords_found}/{len(job_skills)} key skills mentioned explicitly")
            recommendations.append("Add more keywords from the job description to improve ATS matching")
        
        # Check for contact information
        has_email = '@' in resume_text and '.' in resume_text
        has_phone = re.search(r'\d{3}[-.]?\d{3}[-.]?\d{4}', resume_text)
        
        if not has_email:
            issues.append("Email address not clearly visible")
            recommendations.append("Ensure email address is clearly stated at the top")
            formatting_score -= 10
        
        if not has_phone:
            issues.append("Phone number not clearly visible")
            recommendations.append("Include phone number in a standard format")
            formatting_score -= 5
        
        # Overall assessment
        overall_score = (formatting_score + keyword_optimization) / 2
        is_ats_friendly = overall_score >= 70 and len(issues) <= 3
        
        if not issues:
            recommendations.append("✅ Resume appears to be ATS-friendly!")
        
        return ATSCompatibility(
            overall_score=max(0, overall_score),
            is_ats_friendly=is_ats_friendly,
            issues=issues,
            recommendations=recommendations,
            formatting_score=max(0, formatting_score),
            keyword_optimization=keyword_optimization
        )
    
    def _generate_career_insights(self,
                                  score_breakdown: ScoreBreakdown,
                                  resume_data: Dict[str, Any],
                                  job_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate career progression and fit insights"""
        insights = {
            'career_level': 'Unknown',
            'role_fit': 'Unknown',
            'growth_potential': [],
            'alternative_roles': []
        }
        
        # Determine career level from experience
        exp_score = score_breakdown.experience_score
        if exp_score >= 0.8:
            insights['career_level'] = 'Senior/Lead level'
            insights['alternative_roles'] = [
                'Senior Software Engineer',
                'Tech Lead',
                'Engineering Manager'
            ]
        elif exp_score >= 0.5:
            insights['career_level'] = 'Mid-level'
            insights['alternative_roles'] = [
                'Software Engineer',
                'Backend Developer',
                'Full Stack Developer'
            ]
        else:
            insights['career_level'] = 'Junior/Entry level'
            insights['alternative_roles'] = [
                'Junior Developer',
                'Associate Engineer',
                'Software Engineer I'
            ]
        
        # Role fit analysis
        overall_score = score_breakdown.overall_score
        if overall_score >= 75:
            insights['role_fit'] = 'Excellent fit for this specific role'
        elif overall_score >= 60:
            insights['role_fit'] = 'Good fit with some development areas'
        elif overall_score >= 45:
            insights['role_fit'] = 'Moderate fit - consider lateral moves or skill development'
        else:
            insights['role_fit'] = 'Limited fit - significant reskilling needed or explore different roles'
        
        # Growth potential
        matched_skills = len(score_breakdown.matched_skills)
        missing_skills = len(score_breakdown.missing_skills)
        
        if missing_skills <= 2:
            insights['growth_potential'].append('Close to role requirements - minimal upskilling needed')
        elif missing_skills <= 5:
            insights['growth_potential'].append('3-6 months of focused learning could close skill gaps')
        else:
            insights['growth_potential'].append('6-12 months of learning recommended to meet requirements')
        
        if score_breakdown.skill_match_score >= 0.7:
            insights['growth_potential'].append('Strong foundation - ready for advanced topics')
        
        return insights
    
    def _generate_detailed_recommendations(self,
                                          score_breakdown: ScoreBreakdown,
                                          skill_analysis: List[SkillAnalysis],
                                          ats_compat: ATSCompatibility) -> List[str]:
        """Generate actionable recommendations"""
        recommendations = []
        
        # Priority recommendations based on score
        if score_breakdown.overall_score < 60:
            recommendations.append(
                "🎯 **PRIORITY ACTION:** Focus on acquiring the 2-3 most critical missing skills. "
                "This will have the biggest impact on your score."
            )
        
        # Skill-based recommendations
        critical_missing = [s for s in skill_analysis if not s.is_matched and s.importance == 'Critical']
        if critical_missing:
            skills_list = ', '.join([s.skill_name for s in critical_missing[:3]])
            recommendations.append(
                f"📚 **Learn Critical Skills:** Focus on {skills_list}. "
                f"These are essential for the role and in high demand."
            )
        
        # ATS recommendations
        if not ats_compat.is_ats_friendly:
            recommendations.append(
                "🤖 **Improve ATS Compatibility:** Your resume may not pass automated screening. "
                f"See ATS analysis for specific fixes (current score: {ats_compat.overall_score:.0f}%)."
            )
        
        # Keyword optimization
        if score_breakdown.keyword_score < 0.5:
            recommendations.append(
                "🔑 **Add Keywords:** Incorporate more exact phrases from the job description. "
                "This helps with both ATS systems and recruiter scanning."
            )
        
        # Experience articulation
        if score_breakdown.semantic_similarity < 0.6:
            recommendations.append(
                "✍️ **Rephrase Experience:** Use language from the job description to describe "
                "your experience. Match their terminology and focus areas."
            )
        
        # Positive reinforcement
        if score_breakdown.skill_match_score >= 0.7:
            recommendations.append(
                "✅ **Highlight Strengths:** You have strong relevant skills. Make sure they're "
                "prominently featured in your resume summary and experience sections."
            )
        
        return recommendations
    
    def _create_learning_roadmap(self, skill_analysis: List[SkillAnalysis]) -> List[Dict[str, Any]]:
        """Create prioritized learning roadmap for missing skills"""
        roadmap = []
        
        # Filter missing skills and prioritize
        missing = [s for s in skill_analysis if not s.is_matched]
        
        # Group by priority
        critical = [s for s in missing if s.importance == 'Critical']
        important = [s for s in missing if s.importance == 'Important']
        beneficial = [s for s in missing if s.importance == 'Beneficial']
        
        phase = 1
        
        # Phase 1: Critical skills
        if critical:
            for skill in critical:
                roadmap.append({
                    'phase': phase,
                    'priority': 'Critical',
                    'skill': skill.skill_name,
                    'estimated_time': skill.estimated_learning_time,
                    'market_demand': skill.market_demand,
                    'resources': skill.learning_resources,
                    'reason': 'Essential for this role'
                })
            phase += 1
        
        # Phase 2: Important skills
        if important:
            for skill in important[:3]:  # Limit to top 3
                roadmap.append({
                    'phase': phase,
                    'priority': 'Important',
                    'skill': skill.skill_name,
                    'estimated_time': skill.estimated_learning_time,
                    'market_demand': skill.market_demand,
                    'resources': skill.learning_resources,
                    'reason': 'Strongly recommended'
                })
            if len(important) > 3:
                phase += 1
        
        # Phase 3: Beneficial skills (only if time permits)
        if beneficial and len(roadmap) < 6:
            for skill in beneficial[:2]:  # Limit to top 2
                roadmap.append({
                    'phase': min(phase + 1, 3),
                    'priority': 'Beneficial',
                    'skill': skill.skill_name,
                    'estimated_time': skill.estimated_learning_time,
                    'market_demand': skill.market_demand,
                    'resources': skill.learning_resources,
                    'reason': 'Nice to have'
                })
        
        return roadmap
    
    def _generate_benchmark(self, score_breakdown: ScoreBreakdown) -> Dict[str, Any]:
        """Generate industry benchmark comparison"""
        score = score_breakdown.overall_score
        
        # Simulated benchmark data (in production, this would come from real data)
        return {
            'your_score': score,
            'average_applicant': 62,
            'top_10_percent': 82,
            'top_25_percent': 74,
            'percentile': self._calculate_percentile(score),
            'interpretation': self._get_benchmark_interpretation(score)
        }
    
    def _calculate_percentile(self, score: float) -> int:
        """Calculate approximate percentile based on score"""
        # Simplified percentile calculation
        if score >= 85:
            return 95
        elif score >= 75:
            return 80
        elif score >= 65:
            return 60
        elif score >= 55:
            return 40
        elif score >= 45:
            return 25
        else:
            return 10
    
    def _get_benchmark_interpretation(self, score: float) -> str:
        """Interpret benchmark position"""
        percentile = self._calculate_percentile(score)
        
        if percentile >= 90:
            return "You're in the top 10% of applicants for this role!"
        elif percentile >= 75:
            return "You're above average and competitive for this position."
        elif percentile >= 50:
            return "You're around the average applicant for this role."
        elif percentile >= 25:
            return "You're below average. Focus on skill development to improve."
        else:
            return "Significant gaps exist. Consider additional training or different roles."
