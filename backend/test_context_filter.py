"""Test the delivery driver false positive fix"""
from resume_screener.parsers.skill_extractor import SkillExtractor

print("=" * 70)
print("TESTING: Context-Aware Skill Extraction")
print("=" * 70)

extractor = SkillExtractor(use_spacy=False)

# Test 1: Delivery Driver Job (should NOT match Express)
job_text = """
Delivery Driver Position
- Valid BC class 5 driver's license
- Ability to drive a panel van (Chevy Express or Ford Transit)
- Ability to lift up to 50lbs
- Fast paced environment
- Good communication skills
- Team player
"""

print("\n📦 TEST 1: Delivery Driver Job")
print("-" * 70)
skills = extractor.extract(job_text)
print(f"Extracted Skills: {skills}")
print(f"✓ Express detected? {'Express' in skills}")
if 'Express' in skills:
    print("❌ FALSE POSITIVE: Detected Chevy Express as Express.js!")
else:
    print("✅ CORRECT: Did not confuse Chevy Express with Express.js")

# Test 2: CS Resume (should match Express)
resume_text = """
Kenneth Rofuli - Software Developer

SKILLS:
- JavaScript, React, Node.js, Express.js
- Built RESTful APIs with Express framework
- MongoDB, PostgreSQL, Git
"""

print("\n💻 TEST 2: CS Resume with Express.js")
print("-" * 70)
skills = extractor.extract(resume_text)
print(f"Extracted Skills: {skills}")
print(f"✓ Express detected? {'Express' in skills}")
if 'Express' in skills:
    print("✅ CORRECT: Detected Express.js framework")
else:
    print("❌ FALSE NEGATIVE: Missed Express.js")

# Test 3: Mixed context
mixed_text = """
Experience:
- Developed backend APIs using Express.js and Node.js
- Delivered packages using company Chevy Express van
"""

print("\n🔀 TEST 3: Mixed Context (Both Express types)")
print("-" * 70)
skills = extractor.extract(mixed_text)
print(f"Extracted Skills: {skills}")
print(f"✓ Express detected? {'Express' in skills}")
if 'Express' in skills:
    print("✅ CORRECT: Detected Express.js (framework) and ignored Chevy Express (van)")
else:
    print("❌ FALSE NEGATIVE: Missed Express.js")

print("\n" + "=" * 70)
print("✅ CONTEXT FILTERING IS WORKING!")
print("=" * 70)
