"""
Bias Detection Module
Analyzes potential bias in resume screening
"""

import re
from typing import Dict, List, Any, Set
import logging
from collections import defaultdict

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class BiasDetector:
    """Detect potential bias in resume and screening process"""
    
    # Sensitive attributes that might indicate bias
    GENDER_INDICATORS = {
        'male': ['he', 'his', 'him', 'mr', 'gentleman', 'guy', 'brother', 'son', 'father', 'husband'],
        'female': ['she', 'her', 'hers', 'ms', 'mrs', 'miss', 'lady', 'woman', 'sister', 'daughter', 'mother', 'wife']
    }
    
    AGE_PATTERNS = [
        r'\b(19|20)\d{2}\b',  # Birth years
        r'\b\d{2}\s*years?\s*old\b',
        r'\baged?\s*\d{2}\b',
        r'\byoung\b',
        r'\bsenior\b',
        r'\bjunior\b',
        r'\brecent\s+graduate\b'
    ]
    
    ETHNICITY_INDICATORS = [
        'asian', 'caucasian', 'african', 'hispanic', 'latino', 'latina',
        'black', 'white', 'native', 'indigenous', 'minority'
    ]
    
    # University names that might indicate geography/background
    GEOGRAPHY_INDICATORS = [
        'country', 'region', 'city', 'hometown', 'nationality', 'citizen'
    ]
    
    # Other protected attributes
    PROTECTED_ATTRIBUTES = [
        'married', 'single', 'divorced', 'children', 'kids', 'family',
        'religion', 'religious', 'church', 'temple', 'mosque',
        'disability', 'disabled', 'veteran', 'military'
    ]
    
    def __init__(self):
        """Initialize bias detector"""
        self.bias_warnings = []
    
    def detect(self, resume_text: str, 
              job_description: str = None) -> Dict[str, Any]:
        """
        Detect potential bias in resume and/or job description
        
        Args:
            resume_text: Resume text to analyze
            job_description: Optional job description to analyze
            
        Returns:
            Dictionary with bias detection results
        """
        results = {
            'resume_bias': self._analyze_text(resume_text, 'resume'),
            'job_bias': None,
            'overall_risk': 'low',
            'warnings': [],
            'recommendations': []
        }
        
        if job_description:
            results['job_bias'] = self._analyze_text(job_description, 'job_description')
        
        # Calculate overall risk
        resume_risk = results['resume_bias']['risk_level']
        job_risk = results['job_bias']['risk_level'] if results['job_bias'] else 'low'
        
        if resume_risk == 'high' or job_risk == 'high':
            results['overall_risk'] = 'high'
        elif resume_risk == 'medium' or job_risk == 'medium':
            results['overall_risk'] = 'medium'
        
        # Generate warnings and recommendations
        results['warnings'] = self._generate_warnings(results)
        results['recommendations'] = self._generate_recommendations(results)
        
        return results
    
    def _analyze_text(self, text: str, text_type: str) -> Dict[str, Any]:
        """Analyze text for bias indicators"""
        text_lower = text.lower()
        
        findings = {
            'gender_indicators': self._detect_gender(text_lower),
            'age_indicators': self._detect_age(text_lower),
            'ethnicity_indicators': self._detect_ethnicity(text_lower),
            'protected_attributes': self._detect_protected_attributes(text_lower),
            'risk_level': 'low',
            'issues_found': []
        }
        
        # Count total issues
        total_issues = (
            len(findings['gender_indicators']) +
            len(findings['age_indicators']) +
            len(findings['ethnicity_indicators']) +
            len(findings['protected_attributes'])
        )
        
        # Determine risk level
        if total_issues >= 5:
            findings['risk_level'] = 'high'
        elif total_issues >= 2:
            findings['risk_level'] = 'medium'
        else:
            findings['risk_level'] = 'low'
        
        # List specific issues
        if findings['gender_indicators']:
            findings['issues_found'].append('Gender indicators detected')
        if findings['age_indicators']:
            findings['issues_found'].append('Age-related information found')
        if findings['ethnicity_indicators']:
            findings['issues_found'].append('Ethnicity/race indicators present')
        if findings['protected_attributes']:
            findings['issues_found'].append('Protected attributes mentioned')
        
        return findings
    
    def _detect_gender(self, text: str) -> List[str]:
        """Detect gender indicators"""
        found = []
        for gender, indicators in self.GENDER_INDICATORS.items():
            for indicator in indicators:
                if re.search(rf'\b{indicator}\b', text):
                    found.append(f"{indicator} ({gender})")
        return list(set(found))
    
    def _detect_age(self, text: str) -> List[str]:
        """Detect age indicators"""
        found = []
        for pattern in self.AGE_PATTERNS:
            matches = re.findall(pattern, text)
            if matches:
                found.extend(matches)
        return found
    
    def _detect_ethnicity(self, text: str) -> List[str]:
        """Detect ethnicity/race indicators"""
        found = []
        for indicator in self.ETHNICITY_INDICATORS:
            if re.search(rf'\b{indicator}\b', text):
                found.append(indicator)
        return list(set(found))
    
    def _detect_protected_attributes(self, text: str) -> List[str]:
        """Detect other protected attributes"""
        found = []
        for attr in self.PROTECTED_ATTRIBUTES:
            if re.search(rf'\b{attr}\b', text):
                found.append(attr)
        return list(set(found))
    
    def _generate_warnings(self, results: Dict[str, Any]) -> List[str]:
        """Generate bias warnings"""
        warnings = []
        
        resume_bias = results['resume_bias']
        if resume_bias['risk_level'] in ['medium', 'high']:
            warnings.append(
                f"⚠️ Resume contains potential bias indicators (Risk: {resume_bias['risk_level']})"
            )
            for issue in resume_bias['issues_found']:
                warnings.append(f"   - {issue}")
        
        job_bias = results.get('job_bias')
        if job_bias and job_bias['risk_level'] in ['medium', 'high']:
            warnings.append(
                f"⚠️ Job description contains potential bias indicators (Risk: {job_bias['risk_level']})"
            )
            for issue in job_bias['issues_found']:
                warnings.append(f"   - {issue}")
        
        return warnings
    
    def _generate_recommendations(self, results: Dict[str, Any]) -> List[str]:
        """Generate bias mitigation recommendations"""
        recommendations = []
        
        resume_bias = results['resume_bias']
        
        if resume_bias['gender_indicators']:
            recommendations.append(
                "🔧 Remove or redact gender-specific pronouns and titles"
            )
        
        if resume_bias['age_indicators']:
            recommendations.append(
                "🔧 Remove birth years, graduation dates, and age references"
            )
        
        if resume_bias['ethnicity_indicators']:
            recommendations.append(
                "🔧 Remove ethnicity/race indicators unless legally required"
            )
        
        if resume_bias['protected_attributes']:
            recommendations.append(
                "🔧 Remove personal information about marital status, religion, etc."
            )
        
        # General recommendations
        if results['overall_risk'] in ['medium', 'high']:
            recommendations.append(
                "🔧 Consider using blind resume screening process"
            )
            recommendations.append(
                "🔧 Focus evaluation on skills, experience, and qualifications only"
            )
            recommendations.append(
                "🔧 Use structured interview questions to reduce bias"
            )
        
        return recommendations
    
    def anonymize_resume(self, resume_text: str) -> str:
        """
        Anonymize resume by removing potential bias indicators
        
        Args:
            resume_text: Original resume text
            
        Returns:
            Anonymized resume text
        """
        anonymized = resume_text
        
        # Remove names (simple heuristic - first capitalized word on first line)
        lines = anonymized.split('\n')
        if lines:
            lines[0] = '[NAME REDACTED]'
        
        # Remove email addresses
        anonymized = re.sub(
            r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
            '[EMAIL REDACTED]',
            anonymized
        )
        
        # Remove phone numbers
        anonymized = re.sub(
            r'\b\d{3}[-.\s]?\d{3}[-.\s]?\d{4}\b',
            '[PHONE REDACTED]',
            anonymized
        )
        
        # Remove addresses (simple heuristic)
        anonymized = re.sub(
            r'\b\d+\s+[A-Za-z\s]+(?:Street|St|Avenue|Ave|Road|Rd|Boulevard|Blvd)\b',
            '[ADDRESS REDACTED]',
            anonymized,
            flags=re.IGNORECASE
        )
        
        # Remove gender pronouns
        gender_replacements = {
            r'\bhe\b': 'they',
            r'\bhis\b': 'their',
            r'\bhim\b': 'them',
            r'\bshe\b': 'they',
            r'\bher\b': 'their',
            r'\bhers\b': 'theirs'
        }
        for pattern, replacement in gender_replacements.items():
            anonymized = re.sub(pattern, replacement, anonymized, flags=re.IGNORECASE)
        
        # Remove age indicators
        anonymized = re.sub(
            r'\b(19|20)\d{2}\b',
            '[YEAR REDACTED]',
            anonymized
        )
        
        return '\n'.join(lines)


class FairnessMetrics:
    """Calculate fairness metrics for screening results"""
    
    @staticmethod
    def calculate_selection_rate(results: List[Dict[str, Any]], 
                                 threshold: float = 70) -> float:
        """
        Calculate selection rate (percentage passing threshold)
        
        Args:
            results: List of analysis results
            threshold: Score threshold for selection
            
        Returns:
            Selection rate (0-1)
        """
        if not results:
            return 0.0
        
        selected = sum(1 for r in results if r.get('score', 0) >= threshold)
        return selected / len(results)
    
    @staticmethod
    def calculate_adverse_impact(group1_results: List[Dict[str, Any]],
                                group2_results: List[Dict[str, Any]],
                                threshold: float = 70) -> Dict[str, float]:
        """
        Calculate adverse impact ratio (80% rule)
        
        Args:
            group1_results: Results for group 1
            group2_results: Results for group 2
            threshold: Score threshold
            
        Returns:
            Dictionary with fairness metrics
        """
        rate1 = FairnessMetrics.calculate_selection_rate(group1_results, threshold)
        rate2 = FairnessMetrics.calculate_selection_rate(group2_results, threshold)
        
        # Adverse impact ratio (should be >= 0.8)
        if rate2 > 0:
            impact_ratio = rate1 / rate2
        else:
            impact_ratio = 0.0
        
        passes_80_rule = impact_ratio >= 0.8
        
        return {
            'group1_selection_rate': rate1,
            'group2_selection_rate': rate2,
            'adverse_impact_ratio': impact_ratio,
            'passes_80_percent_rule': passes_80_rule,
            'is_fair': passes_80_rule
        }


if __name__ == "__main__":
    # Test bias detection
    print("Testing Bias Detector...")
    
    detector = BiasDetector()
    
    sample_resume = """
    John Smith
    john.smith@email.com | (555) 123-4567
    
    27 years old, married with two children
    Born in 1996
    
    A dedicated professional with strong work ethic.
    He has 5 years of experience...
    """
    
    sample_job = """
    Looking for a young, energetic developer
    Must be a recent graduate
    Native English speaker preferred
    """
    
    results = detector.detect(sample_resume, sample_job)
    
    print("\n📊 Bias Detection Results:")
    print(f"Overall Risk: {results['overall_risk'].upper()}")
    print(f"\nResume Risk: {results['resume_bias']['risk_level']}")
    print(f"Issues: {results['resume_bias']['issues_found']}")
    print(f"\nJob Description Risk: {results['job_bias']['risk_level']}")
    print(f"Issues: {results['job_bias']['issues_found']}")
    
    print("\n⚠️ Warnings:")
    for warning in results['warnings']:
        print(f"  {warning}")
    
    print("\n🔧 Recommendations:")
    for rec in results['recommendations']:
        print(f"  {rec}")
    
    print("\n🔒 Anonymized Resume:")
    print(detector.anonymize_resume(sample_resume))
