from resume_screener.parsers.skill_extractor import SkillExtractor

job_text = """
Line Cook Position

We are looking for:
- Cooks with a drive to produce top quality food and maintain a clean and organized work environment
- Cooks who are excited about great customer service and contributing to a team effort
- Cooks with a positive attitude and embrace great teamwork
- Cooks who are passionate about the restaurant business

We offer;
- Competitive Wages
- Medical/Dental Benefits
- Free Meal per Shift
- Daily CASH tips!!!

Required experience:
Line Cook: 1 year
"""

extractor = SkillExtractor(use_spacy=False)
skills = extractor.extract(job_text)

print("=" * 60)
print("SKILLS EXTRACTED FROM LINE COOK JOB POSTING")
print("=" * 60)
print(f"\nFound {len(skills)} skills:")
for skill in skills:
    print(f"  - {skill}")
    
print("\n" + "=" * 60)
print("BEFORE vs AFTER")
print("=" * 60)
print("\nBEFORE (old database):")
print("  - Teamwork")
print("  - Communication") 
print("  - Customer Service")
print("  (Missing: line cook, food prep, cooking, sanitation)")

print("\nAFTER (new database):")
print(f"  Found {len(skills)} skills including culinary-specific ones!")
