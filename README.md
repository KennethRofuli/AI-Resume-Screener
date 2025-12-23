# 🎯 AI Resume Screener & Job Fit Analyzer

A sophisticated AI-powered system that scores resumes against job postings using state-of-the-art NLP embeddings (BERT/SBERT) and provides explainable matching results. This system includes both a modern React web interface and a Python API for seamless integration.

## ✨ Features

### Core Functionality
- ✅ **Resume Scoring**: Automatically score resumes against job descriptions
- ✅ **Skill Gap Analysis**: Identify missing skills and qualifications (258+ skills across 13 industries)
- ✅ **Explainable AI**: Detailed explanations for match results
- ✅ **Semantic Matching**: Uses BERT/SBERT embeddings for deep understanding
- ✅ **Multi-format Support**: PDF, DOCX, and TXT files

### Advanced Features
- 🛡️ **Bias Detection**: Identify potential bias in screening
- 📊 **Interactive Dashboard**: Beautiful visualizations with charts and score breakdowns
- 💡 **Resume Improvement**: Actionable suggestions for candidates
- 🎯 **Classification**: Automatic candidate categorization (Perfect/Good/Potential/Poor Match)
- 📤 **Drag & Drop**: Easy resume upload interface
- 📱 **Responsive Design**: Works on desktop, tablet, and mobile

## 🏗️ Project Structure

```
AI Resume Checker/
├── backend/                    # Python backend
│   ├── api.py                 # FastAPI REST API
│   ├── requirements.txt       # Python dependencies
│   └── resume_screener/       # Core package
│       ├── models/            # NLP models and embeddings
│       ├── parsers/           # Document parsing utilities
│       ├── scoring/           # Similarity and scoring engines
│       ├── explainability/    # Result explanation logic
│       └── bias_detection/    # Fairness analysis
│
└── frontend/                  # React web application
    ├── src/
    │   ├── components/        # React components
    │   │   ├── ResumeUpload.js
    │   │   ├── JobInput.js
    │   │   ├── AnalysisResults.js
    │   │   ├── ScoreCard.js
    │   │   └── SkillsChart.js
    │   └── services/          # API integration
    └── package.json
```

## 📦 Installation

### Prerequisites
- Python 3.8 or higher
- Node.js 14 or higher
- npm or yarn

### First-Time Setup

1. **Install Python Dependencies**
```bash
cd backend
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

2. **Install React Dependencies**
```bash
cd frontend
npm install
```

## 🚀 Quick Start

### Option 1: Automated Start (Recommended)

**Windows PowerShell:**
```powershell
.\start.ps1
```

**Windows Command Prompt:**
```cmd
start.bat
```

This automatically starts both the backend API (port 8000) and frontend React app (port 3000).

### Option 2: Manual Start

**Terminal 1 - Backend API:**
```bash
cd backend
.venv\Scripts\activate  # Windows
# source .venv/bin/activate  # Linux/Mac
python api.py
```
Backend runs on http://localhost:8000

**Terminal 2 - Frontend:**
```bash
cd frontend
npm start
```
Frontend opens automatically at http://localhost:3000

### Option 3: Python API Only

```python
from resume_screener import ResumeAnalyzer

# Initialize analyzer
analyzer = ResumeAnalyzer()

# Analyze resume against job posting
result = analyzer.analyze(
    resume_path="path/to/resume.pdf",
    job_description="Job posting text..."
)

print(f"Match Score: {result.score}%")
print(f"Matched Skills: {result.matched_skills}")
print(f"Missing Skills: {result.missing_skills}")
print(f"Classification: {result.classification}")

# Get detailed explanation
result.print_summary()
```

## 🎮 Using the Web Application

1. **Access the App**: Open http://localhost:3000 in your browser
2. **Upload Resume**: Drag & drop or click to upload (PDF, DOCX, TXT supported)
3. **Enter Job Description**: Paste the job posting text
4. **Analyze**: Click "Analyze Resume" button
5. **View Results**: Get detailed scoring, skill analysis, and recommendations

## 🔌 API Usage

### Interactive API Documentation
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Example API Calls

**Analyze with Text:**
```bash
curl -X POST "http://localhost:8000/api/analyze" \
  -H "Content-Type: application/json" \
  -d '{
    "resume_text": "Your resume text...",
    "job_description": "Job description..."
  }'
```

**Analyze with File:**
```bash
curl -X POST "http://localhost:8000/api/analyze-file" \
  -F "resume_file=@resume.pdf" \
  -F "job_description=Job description text..."
```

**Check for Bias:**
```bash
curl -X POST "http://localhost:8000/api/bias-check" \
  -H "Content-Type: application/json" \
  -d '{
    "resume_text": "Your resume text..."
  }'
```


## 🔬 Technical Details

### NLP Technology Stack
- **Sentence-BERT (SBERT)**: Semantic similarity and sentence embeddings
- **BERT Base**: Contextual understanding and language modeling
- **spaCy**: Named entity recognition and text processing
- **Custom Models**: Domain-specific fine-tuning for improved accuracy

### Scoring Algorithm
1. **Semantic Embedding Generation**: Convert resume and job description to vector representations
2. **Cosine Similarity Calculation**: Measure semantic similarity between documents
3. **Skill Extraction & Matching**: Identify and match skills using comprehensive skill database (258+ skills)
4. **Experience & Education Weighting**: Factor in years of experience and educational qualifications
5. **Composite Scoring**: Generate final score with detailed component breakdown

### Skill Database
Comprehensive coverage across 13 industries:
- Technology & Software Development
- Healthcare & Medical
- Business & Finance
- Marketing & Sales
- Education & Training
- Hospitality & Culinary
- Manufacturing & Operations
- Transportation & Logistics
- Creative & Design
- Customer Service
- And more...

## 🧪 Testing & Validation

### Running Tests
```bash
cd backend

# Test comprehensive system
python test_system.py

# Test specific industries
python test_line_cook.py
python test_delivery_driver.py

# Test context filtering
python test_context_filter.py
```

### Example Test Scenarios
- Tech resume vs. Software Engineer job (should score high)
- Tech resume vs. Line Cook job (should score low - validates skill detection)
- Healthcare resume vs. Nurse position (validates healthcare skills)
- Driver resume vs. Delivery Driver job (validates transportation skills)

## 🎯 Use Cases

### For HR Departments
- Automate initial resume screening process
- Reduce screening time by up to 80%
- Ensure consistent evaluation criteria
- Scale candidate evaluation efficiently

### For Recruitment Agencies
- Handle high-volume candidate processing
- Provide transparent ranking explanations
- Match candidates to multiple positions
- Generate detailed candidate reports

### For Job Seekers
- Optimize resumes for specific positions
- Identify skill gaps before applying
- Receive actionable improvement suggestions
- Understand how resumes match job requirements

### For Career Services
- Provide data-driven resume guidance
- Help students target appropriate roles
- Demonstrate resume effectiveness
- Track improvement over time

## 🛡️ Fairness & Transparency

### Bias Detection Features
- Identifies potentially biased language
- Flags demographic-related terms
- Promotes fair evaluation practices
- Provides alternative phrasing suggestions

### Explainable AI
- Detailed scoring breakdowns
- Specific skill match explanations
- Transparent algorithm decisions
- Human-readable justifications

## 🚀 Performance & Scalability

- **Fast Processing**: Average analysis time < 2 seconds
- **Scalable Architecture**: RESTful API supports multiple concurrent requests
- **Efficient Caching**: Reuses embeddings for repeated analyses
- **Low Resource Usage**: Optimized for standard hardware

## 🤝 Contributing

Contributions are welcome! Areas for improvement:
- Additional document format support (Google Docs, HTML, Markdown)
- Multi-language support (Spanish, French, German, etc.)
- Enhanced bias detection algorithms
- Custom model fine-tuning for specific industries
- Integration with ATS (Applicant Tracking Systems)
- Resume template suggestions
- Interview question generation

### Development Setup
1. Fork the repository
2. Create a feature branch
3. Make your changes with tests
4. Submit a pull request

## 📝 Configuration

### Environment Variables (Optional)
Create `.env` file in project root:
```env
# Backend
API_HOST=0.0.0.0
API_PORT=8000

# Frontend
REACT_APP_API_URL=http://localhost:8000

# NLP Models
USE_GPU=false
MODEL_CACHE_DIR=./model_cache
```

## 📊 Real-World Impact

This technology is designed for modern HR tech applications:
- ✅ Reduce resume screening time by 80%
- ✅ Increase quality of candidate matches
- ✅ Provide transparent, explainable decisions
- ✅ Ensure fair and unbiased evaluation
- ✅ Scale recruitment operations efficiently

## 🐛 Troubleshooting

### Common Issues

**Port Already in Use:**
```bash
# Kill process on port 8000 (Windows)
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

**spaCy Model Not Found:**
```bash
python -m spacy download en_core_web_sm
```

**React Module Not Found:**
```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
```

**Virtual Environment Issues:**
```bash
# Recreate virtual environment
cd backend
python -m venv .venv
.venv\Scripts\activate  # Windows
pip install -r requirements.txt
```

## 📄 License

MIT License - See LICENSE file for details

## 💬 Support

For questions, issues, or feature requests:
- Open an issue on GitHub
- Check existing documentation
- Review API docs at http://localhost:8000/docs

---

**Made with ❤️ for better hiring practices**
