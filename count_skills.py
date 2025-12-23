import sys
sys.path.insert(0, 'backend')
from resume_screener.parsers.skill_extractor import SkillExtractor

s = SkillExtractor(use_spacy=False)
total = sum(len(skills) for skills in s.SKILL_DATABASE.values())
categories = len(s.SKILL_DATABASE)

print(f'Total Skills: {total}')
print(f'Categories: {categories}')
print('\nBreakdown by category:')
for cat, skills in s.SKILL_DATABASE.items():
    print(f'  {cat}: {len(skills)} skills')
