from resume_screener.parsers.skill_extractor import SkillExtractor

ex = SkillExtractor(use_spacy=False)
print(f'Total skills: {len(ex.all_skills)}')
print(f'\nCategories: {list(ex.SKILL_DATABASE.keys())}')
print(f'\nSample culinary skills: {ex.SKILL_DATABASE["culinary"][:5]}')
print(f'Sample healthcare skills: {ex.SKILL_DATABASE["healthcare"][:5]}')
print(f'Sample finance skills: {ex.SKILL_DATABASE["finance"][:5]}')
