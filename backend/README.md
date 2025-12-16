# Backend - AI Resume Screener

This folder contains all the Python backend code for the AI Resume Screener application.

## Structure

```
backend/
├── api.py                    # FastAPI REST API server
├── demo.py                   # Demo script to test the analyzer
├── test_installation.py      # Installation verification script
├── requirements.txt          # Python dependencies
├── .env.example             # Environment variables template
└── resume_screener/         # Main package
    ├── __init__.py
    ├── main.py              # Main ResumeAnalyzer orchestrator
    ├── models/              # NLP models (BERT, SBERT)
    ├── parsers/             # Document parsers & skill extraction
    ├── scoring/             # Scoring engine & classification
    ├── explainability/      # Explainability features
    └── bias_detection/      # Bias detection & fairness metrics
```

## Quick Start

### 1. Install Dependencies

```bash
cd backend
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

### 2. Run the API Server

```bash
python api.py
```

The API will be available at http://localhost:8000

### 3. View API Documentation

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Testing

Run the test script to verify installation:

```bash
python test_installation.py
```

Run the demo script:

```bash
python demo.py
```

## API Endpoints

- `POST /api/analyze-file` - Analyze resume from uploaded file
- `POST /api/analyze` - Analyze resume from text input
- `POST /api/bias-check` - Check for bias in job descriptions
- `POST /api/batch-analyze` - Analyze multiple resumes
- `GET /health` - Health check endpoint

## Environment Variables

Copy `.env.example` to `.env` and configure:

```
API_HOST=0.0.0.0
API_PORT=8000
CORS_ORIGINS=http://localhost:3000
LOG_LEVEL=INFO
```
