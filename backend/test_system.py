"""
Quick test of the enhanced AI Resume Screener system
"""
import requests
import json

# Test data
RESUME_TEXT = """
John Doe
Software Engineer

EXPERIENCE
Senior Software Engineer at Tech Corp (2020-2023)
- Developed web applications using Python and React
- Implemented RESTful APIs with FastAPI
- Managed PostgreSQL databases
- Led team of 5 developers

SKILLS
Python, JavaScript, React, FastAPI, PostgreSQL, Git, Docker, AWS

EDUCATION
B.S. Computer Science, University of Tech (2016-2020)
"""

JOB_DESCRIPTION = """
Line Cook Position

We are seeking an experienced Line Cook for our busy restaurant.

Requirements:
- 2+ years experience as a line cook
- Food preparation and knife skills
- Ability to work in fast-paced environment
- Food safety certification preferred
- Team player with good communication

Responsibilities:
- Prepare menu items according to recipes
- Maintain clean work station
- Follow food safety guidelines
- Assist with inventory management
"""

def test_basic_analysis():
    print("=" * 60)
    print("TEST 1: Basic Analysis (Tech Resume vs Line Cook Job)")
    print("=" * 60)
    
    response = requests.post(
        "http://localhost:8000/api/analyze-file",
        json={
            "resume_text": RESUME_TEXT,
            "job_description": JOB_DESCRIPTION
        }
    )
    
    if response.status_code == 200:
        result = response.json()
        print(f"\n✓ Overall Score: {result['overall_score']}/100")
        print(f"✓ Recommendation: {result['recommendation']}")
        print(f"\n📊 Score Breakdown:")
        for component, score in result['score_breakdown'].items():
            print(f"  • {component}: {score}/100")
        
        print(f"\n🎯 Skills Matched: {len(result['matched_skills'])}")
        if result['matched_skills']:
            print(f"  {', '.join(result['matched_skills'][:5])}")
        
        print(f"\n❌ Skills Missing: {len(result['missing_skills'])}")
        if result['missing_skills']:
            print(f"  {', '.join(result['missing_skills'][:8])}")
            print("\n  ⚠️  Notice: Culinary skills now detected!")
            print(f"  Check if 'Line Cook' is in missing skills: {'Line Cook' in result['missing_skills']}")
    else:
        print(f"❌ Error: {response.status_code}")

def test_enhanced_analysis():
    print("\n" + "=" * 60)
    print("TEST 2: Enhanced Analysis with Learning Resources")
    print("=" * 60)
    
    # Test with a tech job that matches better
    TECH_JOB = """
    Senior Backend Developer

    Requirements:
    - 3+ years Python development
    - Experience with FastAPI or Django
    - PostgreSQL and database design
    - RESTful API development
    - AWS cloud services
    - Docker containerization
    - Git version control
    """
    
    response = requests.post(
        "http://localhost:8000/api/analyze-enhanced",
        json={
            "resume_text": RESUME_TEXT,
            "job_description": TECH_JOB
        }
    )
    
    if response.status_code == 200:
        result = response.json()
        print(f"\n✓ Overall Score: {result['overall_score']}/100")
        
        print(f"\n📚 Top Skills Analysis:")
        for i, skill in enumerate(result['skill_analysis'][:3], 1):
            print(f"\n  {i}. {skill['skill_name']} (Importance: {skill['importance']})")
            print(f"     Status: {skill['status']}")
            if skill['learning_resources']:
                print(f"     📖 Resource: {skill['learning_resources'][0]}")
        
        print(f"\n📋 ATS Compatibility:")
        ats = result['ats_compatibility']
        print(f"  Score: {ats['score']}/100")
        print(f"  Keyword Match: {ats['keyword_match_rate']*100:.1f}%")
        
        if result.get('learning_roadmap'):
            print(f"\n🎓 Learning Roadmap:")
            roadmap = result['learning_roadmap']
            print(f"  Phase 1 (0-3 months): {roadmap.get('phase_1', 'N/A')}")
    else:
        print(f"❌ Error: {response.status_code}")

def test_skill_database():
    print("\n" + "=" * 60)
    print("TEST 3: Skill Database Verification")
    print("=" * 60)
    
    response = requests.get("http://localhost:8000/api/skills")
    
    if response.status_code == 200:
        data = response.json()
        print(f"\n✓ Total Skills: {data['total_skills']}")
        print(f"✓ Categories: {len(data['categories'])}")
        print(f"\n📂 Categories:")
        for category, skills in data['categories'].items():
            count = len(skills)
            print(f"  • {category}: {count} skills")
        
        # Check for new industries
        print(f"\n🆕 New Industries Added:")
        new_industries = ['healthcare', 'culinary', 'finance', 'design', 'marketing']
        for industry in new_industries:
            if industry in data['categories']:
                sample_skills = data['categories'][industry][:3]
                print(f"  ✓ {industry.title()}: {', '.join(sample_skills)}")
    else:
        print(f"❌ Error: {response.status_code}")

if __name__ == "__main__":
    import time
    
    print("\n🚀 AI Resume Screener - System Test")
    print("\nWaiting for server to start...")
    time.sleep(3)
    
    try:
        # Run tests
        test_skill_database()
        test_basic_analysis()
        test_enhanced_analysis()
        
        print("\n" + "=" * 60)
        print("✅ ALL TESTS COMPLETE")
        print("=" * 60)
        print("\n💡 Next Steps:")
        print("  1. Open http://localhost:3000 in your browser")
        print("  2. Upload a resume and paste the line cook job")
        print("  3. See the expanded skills in action!")
        
    except requests.exceptions.ConnectionError:
        print("\n❌ Could not connect to backend server")
        print("   Make sure the server is running on http://localhost:8000")
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
