"""
Test the Enhanced Analysis Features
Shows detailed explanations, ATS compatibility, and learning resources
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from resume_screener import ResumeAnalyzer
from resume_screener.explainability.enhanced_explainer import EnhancedExplainabilityEngine
from resume_screener.parsers.document_parser import JobDescriptionParser

# Sample job description
JOB_DESCRIPTION = """
Requirements

Successful Candidates will have proficient skills in C, Python and GoLang.
Experience with SQL is a must. We use PostgreSQL for many of our applications.
An Understanding of VoIP Protocols (SIP, RTP) and real time communication will be useful.
A minimum of 5 years of professional software development experience.
Experience in mentoring Jr. members of our development team.
Results oriented, enjoys working with people to solve technical issues.
"""

# Sample resume text
SAMPLE_RESUME = """
John Doe
Software Engineer
john.doe@email.com | (555) 123-4567

PROFESSIONAL EXPERIENCE

Senior Software Engineer | TechCorp Inc | 2018 - Present
- Developed backend services using Python and Django
- Implemented REST APIs serving 100K+ daily requests
- Mentored 2 junior developers on best practices
- Optimized database queries in PostgreSQL, improving performance by 40%
- Led migration from monolithic to microservices architecture

Software Engineer | StartupXYZ | 2016 - 2018
- Built web applications with JavaScript and React
- Worked with SQL databases for data management
- Collaborated with cross-functional teams

EDUCATION
B.S. Computer Science | State University | 2016

SKILLS
Python, JavaScript, SQL, PostgreSQL, Docker, REST APIs, React, Django, Git
"""

def print_section(title):
    """Print a section header"""
    print("\n" + "=" * 80)
    print(f"  {title}")
    print("=" * 80 + "\n")

def main():
    print("\n🚀 ENHANCED RESUME ANALYSIS DEMO")
    print("=" * 80)
    
    # Initialize components
    print("\n📦 Loading AI models...")
    analyzer = ResumeAnalyzer(use_sbert=True, use_spacy=False)
    enhanced_explainer = EnhancedExplainabilityEngine()
    job_parser = JobDescriptionParser()
    
    # Analyze resume
    print("✅ Models loaded!")
    print("\n📊 Analyzing resume against job description...")
    
    # Parse job description
    job_data = job_parser.parse(JOB_DESCRIPTION)
    
    # Create a temporary resume file
    import tempfile
    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
        f.write(SAMPLE_RESUME)
        temp_resume_path = f.name
    
    try:
        # Basic analysis
        result = analyzer.analyze(
            resume_path=temp_resume_path,
            job_description=JOB_DESCRIPTION
        )
        
        # Get the score breakdown from the result object
        score_breakdown = result.score_breakdown
        
        # Enhanced analysis
        from resume_screener.parsers.document_parser import ResumeParser
        resume_parser = ResumeParser()
        resume_data = resume_parser.parse(temp_resume_path)
        
        enhanced_result = enhanced_explainer.explain(
            score_breakdown=score_breakdown,
            resume_data=resume_data,
            job_data=job_data,
            resume_text=SAMPLE_RESUME
        )
        
        # Display results
        print_section("📊 OVERALL SCORE")
        print(f"Score: {result.score:.1f}/100")
        print(f"Confidence: {result.confidence*100:.0f}%")
        print(f"Classification: {result.classification}")
        print(f"\n{enhanced_result.summary}")
        
        # Score breakdowns
        print_section("📈 DETAILED SCORE EXPLANATIONS")
        for component, explanation in enhanced_result.score_explanations.items():
            print(f"\n{component}")
            print("-" * 80)
            print(explanation)
        
        # Skill analysis
        print_section("🎯 SKILL-BY-SKILL ANALYSIS")
        
        print("✅ MATCHED SKILLS:")
        for skill in enhanced_result.skill_analysis:
            if skill.is_matched:
                print(f"\n  • {skill.skill_name} ({skill.importance})")
                print(f"    {skill.reason}")
                print(f"    Market Demand: {skill.market_demand}")
        
        print("\n\n❌ MISSING SKILLS:")
        for skill in enhanced_result.skill_analysis:
            if not skill.is_matched:
                print(f"\n  • {skill.skill_name} ({skill.importance})")
                print(f"    {skill.reason}")
                print(f"    Learning Time: {skill.estimated_learning_time}")
                print(f"    Resources:")
                for resource in skill.learning_resources[:2]:
                    print(f"      - {resource}")
        
        # ATS Compatibility
        print_section("🤖 ATS COMPATIBILITY CHECK")
        ats = enhanced_result.ats_compatibility
        print(f"Overall ATS Score: {ats.overall_score:.1f}/100")
        print(f"ATS Friendly: {'✅ YES' if ats.is_ats_friendly else '⚠️  NEEDS IMPROVEMENT'}")
        print(f"Formatting Score: {ats.formatting_score:.1f}/100")
        print(f"Keyword Optimization: {ats.keyword_optimization:.1f}/100")
        
        if ats.issues:
            print("\n⚠️  Issues Found:")
            for issue in ats.issues:
                print(f"  • {issue}")
        
        if ats.recommendations:
            print("\n💡 Recommendations:")
            for rec in ats.recommendations:
                print(f"  • {rec}")
        
        # Career Insights
        print_section("💼 CAREER INSIGHTS")
        career = enhanced_result.career_insights
        print(f"Career Level: {career['career_level']}")
        print(f"Role Fit: {career['role_fit']}")
        
        if career['growth_potential']:
            print("\n📈 Growth Potential:")
            for insight in career['growth_potential']:
                print(f"  • {insight}")
        
        if career['alternative_roles']:
            print("\n🔄 Alternative Roles to Consider:")
            for role in career['alternative_roles']:
                print(f"  • {role}")
        
        # Learning Roadmap
        print_section("📚 PERSONALIZED LEARNING ROADMAP")
        if enhanced_result.learning_roadmap:
            current_phase = 0
            for item in enhanced_result.learning_roadmap:
                if item['phase'] != current_phase:
                    current_phase = item['phase']
                    print(f"\n🎯 PHASE {current_phase} ({item['priority']} Priority)")
                    print("-" * 80)
                
                print(f"\n  📖 {item['skill']}")
                print(f"     Time: {item['estimated_time']} | Demand: {item['market_demand']}")
                print(f"     Why: {item['reason']}")
                print(f"     Resources:")
                for resource in item['resources'][:2]:
                    print(f"       • {resource}")
        else:
            print("✅ No skill gaps! You meet all requirements.")
        
        # Recommendations
        print_section("💡 TOP RECOMMENDATIONS")
        for i, rec in enumerate(enhanced_result.recommendations, 1):
            print(f"{i}. {rec}\n")
        
        # Industry Benchmark
        print_section("📊 INDUSTRY BENCHMARK")
        benchmark = enhanced_result.industry_benchmark
        print(f"Your Score: {benchmark['your_score']:.1f}")
        print(f"Average Applicant: {benchmark['average_applicant']}")
        print(f"Top 25%: {benchmark['top_25_percent']}")
        print(f"Top 10%: {benchmark['top_10_percent']}")
        print(f"\n🎯 You're in the {benchmark['percentile']}th percentile")
        print(f"\n{benchmark['interpretation']}")
        
        print("\n" + "=" * 80)
        print("✅ ENHANCED ANALYSIS COMPLETE!")
        print("=" * 80 + "\n")
        
    finally:
        # Clean up temp file
        import os
        if os.path.exists(temp_resume_path):
            os.remove(temp_resume_path)

if __name__ == "__main__":
    main()
