# 🚀 Quick Start Guide

## Installation

1. **Create a virtual environment**
```bash
python -m venv venv
```

2. **Activate the environment**
```bash
# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Download spaCy model (optional, for enhanced skill extraction)**
```bash
python -m spacy download en_core_web_sm
```

## Running the Demo

```bash
python demo.py
```

This will run a comprehensive demonstration showing:
- Resume parsing and analysis
- Skill matching
- Score calculation with explanations
- Bias detection
- Recommendations

## Starting the API Server

```bash
python api.py
```

Then visit:
- **Interactive API Docs**: http://localhost:8000/docs
- **Alternative Docs**: http://localhost:8000/redoc

## Basic Usage Example

```python
from resume_screener import ResumeAnalyzer

# Initialize
analyzer = ResumeAnalyzer()

# Analyze a resume
result = analyzer.analyze(
    resume_path="path/to/resume.pdf",
    job_description="Your job description text here..."
)

# View results
print(f"Score: {result.score}/100")
print(f"Classification: {result.classification}")
print(f"Matched Skills: {result.matched_skills}")
print(f"Missing Skills: {result.missing_skills}")

# Get detailed explanation
result.print_summary()
```

## API Usage Examples

### Analyze Resume (Text)

```bash
curl -X POST "http://localhost:8000/api/analyze" \
  -H "Content-Type: application/json" \
  -d '{
    "resume_text": "Your resume text...",
    "job_description": "Job description..."
  }'
```

### Analyze Resume (File)

```bash
curl -X POST "http://localhost:8000/api/analyze-file" \
  -F "resume_file=@resume.pdf" \
  -F "job_description=Job description text..."
```

### Check for Bias

```bash
curl -X POST "http://localhost:8000/api/bias-check" \
  -H "Content-Type: application/json" \
  -d '{
    "resume_text": "Resume text...",
    "job_description": "Job description..."
  }'
```

## Project Structure

```
resume_screener/
├── models/              # NLP models (BERT/SBERT)
│   ├── nlp_models.py   # Embedding and semantic matching
│   └── __init__.py
├── parsers/            # Document parsing
│   ├── document_parser.py  # PDF/DOCX/TXT parsing
│   ├── skill_extractor.py  # Skill extraction
│   └── __init__.py
├── scoring/            # Scoring engine
│   ├── scoring_engine.py   # Composite scoring
│   └── __init__.py
├── explainability/     # Result explanation
│   ├── explainer.py    # Explanation generation
│   └── __init__.py
├── bias_detection/     # Bias detection
│   ├── bias_detector.py    # Bias analysis
│   └── __init__.py
├── main.py            # Main analyzer
└── __init__.py
```

## Features Overview

### 1. Semantic Matching
- Uses Sentence-BERT for deep semantic understanding
- Calculates similarity between resume and job description
- Handles synonyms and context

### 2. Skill Extraction & Matching
- Pattern-based skill detection
- NER (Named Entity Recognition) with spaCy
- Fuzzy matching for similar skills
- Categorized skill database (programming, frameworks, tools, etc.)

### 3. Scoring Engine
- Multi-factor composite scoring
- Weighted components:
  - Semantic similarity (30%)
  - Skill match (35%)
  - Experience (20%)
  - Education (10%)
  - Keywords (5%)

### 4. Explainability
- Detailed breakdown of scores
- Strengths and weaknesses
- Actionable recommendations
- Improvement suggestions

### 5. Bias Detection
- Identifies gender, age, ethnicity indicators
- Risk assessment
- Anonymization features
- Fairness metrics

## Customization

### Custom Scoring Weights

```python
from resume_screener.scoring import ScoringWeights

custom_weights = ScoringWeights(
    semantic_similarity=0.25,
    skill_match=0.40,
    experience_match=0.20,
    education_match=0.10,
    keyword_match=0.05
)

analyzer = ResumeAnalyzer()
analyzer.scoring_engine.weights = custom_weights
```

### Adding Custom Skills

```python
from resume_screener.parsers.skill_extractor import SkillExtractor

extractor = SkillExtractor()
extractor.SKILL_DATABASE['custom_category'] = [
    'CustomSkill1', 'CustomSkill2', 'CustomSkill3'
]
```

## Troubleshooting

### Issue: Import errors
**Solution**: Make sure you're in the project directory and virtual environment is activated

### Issue: spaCy model not found
**Solution**: Run `python -m spacy download en_core_web_sm`

### Issue: PDF parsing errors
**Solution**: Install alternative parser: `pip install pdfplumber`

### Issue: CUDA out of memory
**Solution**: Models will automatically fall back to CPU. Reduce batch size or use smaller models.

## Next Steps

1. ✅ Run the demo to see the system in action
2. ✅ Try the API with your own resumes
3. ✅ Customize for your specific use case
4. ✅ Integrate with your HR system
5. ✅ Deploy to production

## Support

For issues, questions, or contributions, please refer to the main README.md file.
