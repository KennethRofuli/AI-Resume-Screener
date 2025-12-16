"""
Skill Extraction and Analysis
Uses NLP and pattern matching to identify skills
"""

import re
import spacy
from typing import List, Set, Dict, Any
import logging
from pathlib import Path
import json

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class SkillExtractor:
    """Extract skills from text using multiple methods"""
    
    # Comprehensive skill database
    SKILL_DATABASE = {
        # Programming Languages
        'programming': [
            'Python', 'Java', 'JavaScript', 'TypeScript', 'C++', 'C#', 'Ruby', 
            'Go', 'Rust', 'Swift', 'Kotlin', 'PHP', 'Scala', 'R', 'MATLAB',
            'Perl', 'Shell', 'Bash', 'PowerShell', 'SQL', 'HTML', 'CSS'
        ],
        
        # Frameworks & Libraries
        'frameworks': [
            'Django', 'Flask', 'FastAPI', 'Spring', 'React', 'Angular', 'Vue.js',
            'Node.js', 'Express', 'TensorFlow', 'PyTorch', 'Keras', 'Scikit-learn',
            'Pandas', 'NumPy', 'jQuery', 'Bootstrap', 'Tailwind', 'Next.js',
            'Laravel', 'Ruby on Rails', '.NET', 'ASP.NET', 'Hibernate', 'Spring Boot'
        ],
        
        # Databases
        'databases': [
            'MySQL', 'PostgreSQL', 'MongoDB', 'Redis', 'Cassandra', 'Oracle',
            'SQL Server', 'SQLite', 'DynamoDB', 'Elasticsearch', 'Neo4j',
            'MariaDB', 'CouchDB', 'Firebase'
        ],
        
        # Cloud & DevOps
        'cloud': [
            'AWS', 'Azure', 'GCP', 'Docker', 'Kubernetes', 'Jenkins', 'GitLab CI',
            'GitHub Actions', 'Terraform', 'Ansible', 'CircleCI', 'Travis CI',
            'CloudFormation', 'Helm', 'ArgoCD', 'ECS', 'EKS', 'Lambda'
        ],
        
        # Tools & Technologies
        'tools': [
            'Git', 'GitHub', 'GitLab', 'Bitbucket', 'JIRA', 'Confluence',
            'VS Code', 'IntelliJ', 'Eclipse', 'Postman', 'Swagger',
            'Linux', 'Unix', 'Windows', 'MacOS', 'Apache', 'Nginx'
        ],
        
        # Data & AI
        'data_ai': [
            'Machine Learning', 'Deep Learning', 'NLP', 'Computer Vision',
            'Data Science', 'Data Analysis', 'Big Data', 'Hadoop', 'Spark',
            'Kafka', 'Airflow', 'ETL', 'Data Warehousing', 'BI', 'Tableau',
            'Power BI', 'BERT', 'GPT', 'Transformers', 'LLM'
        ],
        
        # Methodologies
        'methodologies': [
            'Agile', 'Scrum', 'Kanban', 'DevOps', 'CI/CD', 'TDD', 'BDD',
            'Microservices', 'REST API', 'GraphQL', 'SOAP', 'MVC',
            'Design Patterns', 'OOP', 'Functional Programming'
        ],
        
        # Soft Skills
        'soft_skills': [
            'Leadership', 'Communication', 'Teamwork', 'Problem Solving',
            'Critical Thinking', 'Project Management', 'Time Management',
            'Collaboration', 'Mentoring', 'Presentation', 'Documentation',
            'Analytical Skills', 'Attention to Detail', 'Creative Thinking',
            'Decision Making', 'Adaptability', 'Work Ethic'
        ],
        
        # Writing & Content
        'writing_content': [
            'Writing', 'Technical Writing', 'Content Writing', 'Copywriting',
            'Creative Writing', 'Editorial', 'Editing', 'Proofreading',
            'Content Strategy', 'Content Creation', 'Blogging', 'Journalism',
            'Grant Writing', 'Report Writing', 'Documentation Writing',
            'UX Writing', 'Academic Writing', 'Research Writing',
            'Script Writing', 'Social Media Writing'
        ],
        
        # Healthcare & Medical
        'healthcare': [
            'Patient Care', 'Nursing', 'CPR', 'First Aid', 'Medical Terminology',
            'HIPAA', 'EMR', 'EHR', 'Clinical Documentation', 'Phlebotomy',
            'Vital Signs', 'IV Therapy', 'Wound Care', 'Medical Coding',
            'ICD-10', 'Medical Billing', 'Healthcare Administration',
            'Pharmacology', 'Patient Assessment', 'Healthcare Compliance'
        ],
        
        # Culinary & Food Service
        'culinary': [
            'Food Preparation', 'Cooking', 'Baking', 'Knife Skills', 'Plating',
            'Food Safety', 'Sanitation', 'ServSafe', 'Menu Planning', 'Recipe Development',
            'Grill', 'Sauté', 'Butchering', 'Line Cook', 'Sous Chef', 'Pastry',
            'Food Cost Control', 'Inventory Management', 'Kitchen Management',
            'Customer Service', 'POS Systems', 'Catering', 'Meal Prep'
        ],
        
        # Finance & Accounting
        'finance': [
            'Accounting', 'Bookkeeping', 'Financial Analysis', 'Budgeting',
            'Financial Reporting', 'Auditing', 'Tax Preparation', 'Payroll',
            'QuickBooks', 'Excel', 'SAP', 'Oracle Financials', 'GAAP', 'IFRS',
            'Accounts Payable', 'Accounts Receivable', 'Reconciliation',
            'Financial Planning', 'Investment Analysis', 'Risk Management',
            'Compliance', 'CPA', 'Financial Modeling', 'Forecasting'
        ],
        
        # Design & Creative
        'design': [
            'Adobe Photoshop', 'Adobe Illustrator', 'Adobe InDesign', 'Figma',
            'Sketch', 'UI Design', 'UX Design', 'Web Design', 'Graphic Design',
            'Typography', 'Color Theory', 'Wireframing', 'Prototyping',
            'User Research', 'Branding', 'Logo Design', 'Print Design',
            'Motion Graphics', 'Video Editing', 'Adobe After Effects',
            'Adobe Premiere', 'Canva', '3D Modeling', 'Blender'
        ],
        
        # Marketing & Sales
        'marketing': [
            'Digital Marketing', 'SEO', 'SEM', 'Social Media Marketing',
            'Content Marketing', 'Email Marketing', 'Google Analytics',
            'Google Ads', 'Facebook Ads', 'Marketing Automation', 'CRM',
            'Salesforce', 'HubSpot', 'Copywriting', 'Brand Management',
            'Market Research', 'Campaign Management', 'Lead Generation',
            'Sales', 'Negotiation', 'Cold Calling', 'B2B Sales', 'B2C Sales',
            'Customer Relationship Management', 'Sales Strategy'
        ]
    }
    
    def __init__(self, use_spacy: bool = True):
        """
        Initialize skill extractor
        
        Args:
            use_spacy: Whether to use spaCy for NER (requires model installation)
        """
        self.nlp = None
        if use_spacy:
            try:
                self.nlp = spacy.load('en_core_web_sm')
                logger.info("spaCy model loaded successfully")
            except OSError:
                logger.warning("spaCy model not found. Run: python -m spacy download en_core_web_sm")
        
        # Build flat skill list for matching
        self.all_skills = []
        for category, skills in self.SKILL_DATABASE.items():
            self.all_skills.extend(skills)
        
        # Create lowercase mapping for case-insensitive matching
        self.skill_map = {skill.lower(): skill for skill in self.all_skills}
    
    def extract(self, text: str, method: str = 'hybrid') -> List[str]:
        """
        Extract skills from text
        
        Args:
            text: Input text
            method: Extraction method ('pattern', 'ner', 'hybrid')
            
        Returns:
            List of extracted skills
        """
        if method == 'pattern':
            return self._extract_by_pattern(text)
        elif method == 'ner' and self.nlp:
            return self._extract_by_ner(text)
        else:  # hybrid
            pattern_skills = self._extract_by_pattern(text)
            if self.nlp:
                ner_skills = self._extract_by_ner(text)
                # Combine and deduplicate
                all_skills = set(pattern_skills + ner_skills)
                return sorted(list(all_skills))
            return pattern_skills
    
    def _extract_by_pattern(self, text: str) -> List[str]:
        """Extract skills using pattern matching"""
        found_skills = set()
        text_lower = text.lower()
        
        # Define context filters to avoid false positives
        # Format: {skill: [list of words that if nearby, invalidate the match]}
        context_filters = {
            'express': ['chevy', 'ford', 'van', 'vehicle', 'truck', 'delivery', 'transit'],
            'java': ['coffee', 'chip', 'island'],  # Avoid "Java chip" or "Java island"
            'ruby': ['red', 'gem', 'stone', 'jewelry'],
            'python': ['snake', 'monty'],
            'writing': ['code', 'coding', 'program', 'software', 'clean', 'wrote'],  # Avoid "writing code"
            'creative writing': ['code', 'coding', 'program'],
            'content writing': ['code', 'coding'],
            'technical writing': ['code', 'coding'],  # Unless it's about documentation
        }
        
        # Match skills from database
        for skill_lower, skill_proper in self.skill_map.items():
            # Use word boundaries to avoid partial matches
            pattern = r'\b' + re.escape(skill_lower) + r'\b'
            matches = list(re.finditer(pattern, text_lower))
            
            if matches:
                # Check context for ambiguous skills
                if skill_lower in context_filters:
                    filter_words = context_filters[skill_lower]
                    has_valid_match = False
                    
                    for match in matches:
                        # Check surrounding context (15 chars before/after)
                        start = max(0, match.start() - 15)
                        end = min(len(text_lower), match.end() + 15)
                        context = text_lower[start:end]
                        
                        # If NO filter word is in this match's context, it's valid
                        if not any(word in context for word in filter_words):
                            has_valid_match = True
                            break
                    
                    if has_valid_match:
                        found_skills.add(skill_proper)
                else:
                    # No context filter needed
                    found_skills.add(skill_proper)
        
        # Also look for common variations
        # e.g., "python3" -> "Python", "node.js" -> "Node.js"
        variations = {
            r'\bpython\d?\b': 'Python',
            r'\bnode\.?js\b': 'Node.js',
            r'\bc\+\+\b': 'C++',
            r'\bc#\b': 'C#',
            r'\bvue\.?js\b': 'Vue.js',
            r'\breact\.?js\b': 'React',
            r'\bangular\.?js\b': 'Angular',
        }
        
        for pattern, skill in variations.items():
            if re.search(pattern, text_lower):
                found_skills.add(skill)
        
        return sorted(list(found_skills))
    
    def _extract_by_ner(self, text: str) -> List[str]:
        """Extract skills using Named Entity Recognition"""
        if not self.nlp:
            return []
        
        doc = self.nlp(text)
        found_skills = set()
        
        # Extract entities that might be skills
        for ent in doc.ents:
            if ent.label_ in ['ORG', 'PRODUCT', 'GPE']:
                # Check if it's in our skill database
                if ent.text in self.all_skills:
                    found_skills.add(ent.text)
        
        # Also extract noun chunks that might be skills
        for chunk in doc.noun_chunks:
            chunk_text = chunk.text
            if chunk_text in self.all_skills:
                found_skills.add(chunk_text)
        
        return sorted(list(found_skills))
    
    def categorize_skills(self, skills: List[str]) -> Dict[str, List[str]]:
        """
        Categorize skills into groups
        
        Args:
            skills: List of skills
            
        Returns:
            Dictionary mapping categories to skills
        """
        categorized = {category: [] for category in self.SKILL_DATABASE.keys()}
        categorized['other'] = []
        
        for skill in skills:
            found = False
            for category, skill_list in self.SKILL_DATABASE.items():
                if skill in skill_list:
                    categorized[category].append(skill)
                    found = True
                    break
            
            if not found:
                categorized['other'].append(skill)
        
        # Remove empty categories
        return {k: v for k, v in categorized.items() if v}
    
    def extract_from_section(self, text: str, section_name: str = 'skills') -> List[str]:
        """
        Extract skills from a specific section
        
        Args:
            text: Full document text
            section_name: Name of section to extract from
            
        Returns:
            List of skills found in section
        """
        # Find the skills section
        section_pattern = rf'(?i){section_name}[:\s]+(.*?)(?=\n\n|\n[A-Z]{{2,}}|$)'
        match = re.search(section_pattern, text, re.DOTALL)
        
        if match:
            section_text = match.group(1)
            return self.extract(section_text)
        else:
            # If no specific section found, extract from entire text
            return self.extract(text)
    
    def suggest_missing_skills(self, current_skills: List[str], 
                               job_description: str) -> List[str]:
        """
        Suggest skills to add based on job description
        
        Args:
            current_skills: Skills currently on resume
            job_description: Job posting text
            
        Returns:
            List of suggested skills to add
        """
        required_skills = self.extract(job_description)
        current_skills_lower = [s.lower() for s in current_skills]
        
        missing = []
        for skill in required_skills:
            if skill.lower() not in current_skills_lower:
                missing.append(skill)
        
        return missing


if __name__ == "__main__":
    # Test skill extraction
    print("Testing Skill Extractor...")
    
    extractor = SkillExtractor()
    
    sample_text = """
    Experienced software engineer with expertise in Python, Django, and React.
    Strong background in machine learning using TensorFlow and PyTorch.
    Proficient in AWS, Docker, and Kubernetes.
    Experience with PostgreSQL, MongoDB, and Redis databases.
    Agile/Scrum methodology and CI/CD pipelines using Jenkins and GitLab.
    """
    
    skills = extractor.extract(sample_text)
    print(f"\nExtracted Skills ({len(skills)}):")
    print(skills)
    
    categorized = extractor.categorize_skills(skills)
    print("\nCategorized Skills:")
    for category, skill_list in categorized.items():
        print(f"  {category}: {skill_list}")
    
    # Test skill suggestions
    job_desc = "Looking for Python developer with Flask, FastAPI, and GraphQL experience"
    suggestions = extractor.suggest_missing_skills(skills, job_desc)
    print(f"\nSuggested Skills to Add: {suggestions}")
