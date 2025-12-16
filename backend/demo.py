"""
Demo Script - Comprehensive demonstration of the Resume Screener
"""

from resume_screener import ResumeAnalyzer
from resume_screener.bias_detection import BiasDetector

# Sample resume data
SAMPLE_RESUME = """
Sarah Johnson
Senior Software Engineer
sarah.johnson@email.com | LinkedIn: linkedin.com/in/sarahjohnson

PROFESSIONAL SUMMARY
Results-driven software engineer with 6+ years of experience building scalable web applications 
and RESTful APIs. Expert in Python, Django, and cloud technologies. Proven track record of 
leading development teams and delivering high-quality software solutions.

EXPERIENCE

Senior Software Engineer | TechCorp Inc | San Francisco, CA | 2020 - Present
• Lead development of microservices architecture serving 10M+ users
• Built RESTful APIs using Django and FastAPI with PostgreSQL databases
• Implemented CI/CD pipelines using Jenkins and Docker
• Mentored team of 4 junior developers
• Reduced API response time by 40% through optimization

Software Engineer | StartupXYZ | Remote | 2018 - 2020
• Developed full-stack web applications using Python, Django, and React
• Integrated third-party APIs and payment gateways
• Collaborated with cross-functional teams in Agile environment
• Implemented automated testing with pytest and Selenium

EDUCATION
Master of Science in Computer Science | Stanford University | 2018
Bachelor of Science in Software Engineering | UC Berkeley | 2016

TECHNICAL SKILLS
Languages: Python, JavaScript, TypeScript, SQL, Bash
Frameworks: Django, Flask, FastAPI, React, Node.js
Databases: PostgreSQL, MySQL, MongoDB, Redis
Cloud & DevOps: AWS (EC2, S3, Lambda), Docker, Kubernetes, Jenkins, Git
Tools: JIRA, Confluence, VS Code, Postman

CERTIFICATIONS
• AWS Certified Solutions Architect - Associate
• Certified Scrum Master (CSM)

ACHIEVEMENTS
• Architected system handling 100K requests/day with 99.9% uptime
• Open source contributor to Django and FastAPI projects
• Speaker at PyCon 2022 on "Building Scalable APIs"
"""

SAMPLE_JOB_DESCRIPTION = """
Senior Python Developer

About the Role:
We are seeking an experienced Senior Python Developer to join our growing engineering team. 
You will be responsible for designing and developing scalable backend services and APIs.

Requirements:
• 5+ years of professional Python development experience
• Strong experience with Django or Flask frameworks
• Expertise in building RESTful APIs
• Experience with relational databases (PostgreSQL, MySQL)
• Knowledge of Docker and containerization
• Experience with AWS or other cloud platforms
• Strong understanding of software design patterns and best practices
• Experience with Agile/Scrum methodologies
• Bachelor's degree in Computer Science or related field

Nice to Have:
• Experience with Kubernetes
• Knowledge of microservices architecture
• React or frontend framework experience
• CI/CD pipeline experience
• Experience mentoring junior developers
• Open source contributions

What We Offer:
• Competitive salary and equity
• Comprehensive health benefits
• Remote work flexibility
• Professional development budget
• Collaborative team environment
"""

def main():
    """Run comprehensive demo"""
    
    print("=" * 100)
    print(" " * 30 + "🎯 AI RESUME SCREENER DEMO")
    print("=" * 100)
    print()
    
    # Initialize analyzer
    print("📦 Initializing Resume Analyzer...")
    analyzer = ResumeAnalyzer(use_sbert=True, use_spacy=False)
    print("✅ Analyzer ready!\n")
    
    # Analyze resume
    print("🔍 Analyzing resume against job description...")
    print("-" * 100)
    
    result = analyzer.analyze(
        resume_text=SAMPLE_RESUME,
        job_description=SAMPLE_JOB_DESCRIPTION
    )
    
    # Display results
    print("\n" + "=" * 100)
    print(" " * 35 + "📊 ANALYSIS RESULTS")
    print("=" * 100)
    
    print(f"\n🎯 Overall Match Score: {result.score:.1f}/100")
    print(f"🏷️  Classification: {result.classification}")
    print(f"📈 Confidence Level: {result.score_breakdown.confidence*100:.1f}%")
    print(f"💡 Recommendation: {result.recommendation}")
    
    # Score breakdown
    print("\n" + "-" * 100)
    print("📊 SCORE BREAKDOWN")
    print("-" * 100)
    breakdown_data = result.to_dict()['score_breakdown']
    print(f"  • Semantic Similarity: {breakdown_data['semantic_similarity']:.1f}%")
    print(f"  • Skill Match:         {breakdown_data['skill_match']:.1f}%")
    print(f"  • Experience Level:    {breakdown_data['experience']:.1f}%")
    print(f"  • Education:           {breakdown_data['education']:.1f}%")
    print(f"  • Keyword Match:       {breakdown_data['keyword_match']:.1f}%")
    
    # Matched skills
    print("\n" + "-" * 100)
    print("✅ MATCHED SKILLS")
    print("-" * 100)
    if result.matched_skills:
        for i, skill in enumerate(result.matched_skills, 1):
            print(f"  {i}. {skill}")
    else:
        print("  None")
    
    # Missing skills
    print("\n" + "-" * 100)
    print("❌ MISSING SKILLS")
    print("-" * 100)
    if result.missing_skills:
        for i, skill in enumerate(result.missing_skills, 1):
            print(f"  {i}. {skill}")
    else:
        print("  None")
    
    # Strengths
    print("\n" + "-" * 100)
    print("💪 KEY STRENGTHS")
    print("-" * 100)
    for i, strength in enumerate(result.score_breakdown.strengths, 1):
        print(f"  {i}. {strength}")
    
    # Weaknesses
    if result.score_breakdown.weaknesses:
        print("\n" + "-" * 100)
        print("⚠️  AREAS FOR IMPROVEMENT")
        print("-" * 100)
        for i, weakness in enumerate(result.score_breakdown.weaknesses, 1):
            print(f"  {i}. {weakness}")
    
    # Explanation
    print("\n" + "=" * 100)
    print(" " * 35 + "📝 DETAILED EXPLANATION")
    print("=" * 100)
    print(f"\n{result.explanation.summary}\n")
    
    for component, analysis in result.explanation.detailed_analysis.items():
        print(f"\n{component}:")
        print(f"  {analysis}")
    
    # Recommendations
    print("\n" + "=" * 100)
    print(" " * 35 + "💡 RECOMMENDATIONS")
    print("=" * 100)
    for rec in result.explanation.recommendations:
        print(f"  {rec}")
    
    # Improvement suggestions
    if result.explanation.improvement_suggestions:
        print("\n" + "=" * 100)
        print(" " * 30 + "🚀 IMPROVEMENT SUGGESTIONS")
        print("=" * 100)
        for suggestion in result.explanation.improvement_suggestions:
            print(f"  {suggestion}")
    
    # Bias detection
    print("\n" + "=" * 100)
    print(" " * 35 + "🛡️  BIAS DETECTION")
    print("=" * 100)
    
    bias_detector = BiasDetector()
    bias_results = bias_detector.detect(SAMPLE_RESUME, SAMPLE_JOB_DESCRIPTION)
    
    print(f"\n📊 Overall Risk Level: {bias_results['overall_risk'].upper()}")
    print(f"Resume Risk: {bias_results['resume_bias']['risk_level'].upper()}")
    print(f"Job Description Risk: {bias_results['job_bias']['risk_level'].upper()}")
    
    if bias_results['warnings']:
        print("\n⚠️  Warnings:")
        for warning in bias_results['warnings']:
            print(f"  {warning}")
    else:
        print("\n✅ No significant bias indicators detected")
    
    if bias_results['recommendations']:
        print("\n🔧 Bias Mitigation Recommendations:")
        for rec in bias_results['recommendations']:
            print(f"  {rec}")
    
    # Summary
    print("\n" + "=" * 100)
    print(" " * 35 + "✨ FINAL SUMMARY")
    print("=" * 100)
    print(f"""
This resume scored {result.score:.1f}/100 - a {result.classification}.
    
The candidate demonstrates {len(result.matched_skills)} of the required skills and has relevant 
experience that aligns well with the job requirements. 

{result.recommendation}

Key Takeaways:
  • Strong technical foundation in Python and Django
  • Relevant experience with cloud technologies and microservices
  • Leadership and mentoring experience
  • Active in the developer community
  
Next Steps:
  • Schedule technical phone screen
  • Prepare questions on missing skills (if any)
  • Review portfolio and open source contributions
""")
    
    print("=" * 100)
    print(" " * 30 + "🎉 Demo Complete!")
    print("=" * 100)


if __name__ == "__main__":
    main()
