"""
Test the delivery driver job posting issue
"""
from resume_screener import ResumeAnalyzer

RESUME = """
KENNETH ROFULI
Computer Science student

SKILLS
JavaScript, React, React Native, Node.js, Express.js, MongoDB, SQLite, Git
"""

JOB = """
Delivery Driver Position

Requirements:
- Valid BC class 5 driver's license
- Ability to drive a panel van (Chevy Express or Ford Transit)
- Ability to lift up to 50lbs
- Must deliver 14-16 Packages an Hour
- Fast paced environment
- Good communication skills
"""

print("Testing Delivery Driver Job vs CS Resume")
print("=" * 60)

analyzer = ResumeAnalyzer(use_sbert=True, use_spacy=False)
result = analyzer.analyze(RESUME, JOB)

print(f"\n❌ Overall Score: {result['overall_score']}/100")
print(f"\nMatched Skills: {result['matched_skills']}")
print(f"Missing Skills: {result['missing_skills'][:10]}")

print("\n🔍 The Problem:")
print("- Job mentions 'Chevy Express' (a van)")
print("- Resume has 'Express.js' (Node.js framework)")
print("- System incorrectly matches these as the same skill")
print("\n- This is FALSE POSITIVE - wrong job type entirely!")
print(f"\n- Semantic Similarity: {result['score_breakdown']['semantic_similarity']}/100")
print("  (Should be LOW for driver job vs developer resume)")
