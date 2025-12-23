"""
FastAPI REST API for Resume Screening Service
"""

from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional, List
import tempfile
import os
from pathlib import Path

from resume_screener import ResumeAnalyzer
from resume_screener.bias_detection import BiasDetector
from resume_screener.explainability.enhanced_explainer import EnhancedExplainabilityEngine
from feedback_storage import get_feedback_storage
import uuid

# Initialize FastAPI app
app = FastAPI(
    title="AI Resume Screener API",
    description="Intelligent resume screening with NLP and bias detection",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize components
analyzer = ResumeAnalyzer(use_sbert=True, use_spacy=False)
bias_detector = BiasDetector()
enhanced_explainer = EnhancedExplainabilityEngine()


# Request/Response Models
class AnalyzeRequest(BaseModel):
    """Request model for text-based analysis"""
    resume_text: str = Field(..., description="Resume text content")
    job_description: str = Field(..., description="Job description text")
    required_skills: Optional[List[str]] = Field(None, description="Optional list of required skills")


class AnalyzeResponse(BaseModel):
    """Response model for analysis results"""
    overall_score: float
    classification: str
    recommendation: str
    confidence: float
    matched_skills: List[str]
    missing_skills: List[str]
    score_breakdown: dict
    strengths: List[str]
    weaknesses: List[str]
    explanation_summary: str
    key_factors: List[str]
    improvement_suggestions: List[str]


class BiasCheckRequest(BaseModel):
    """Request model for bias detection"""
    resume_text: Optional[str] = None
    job_description: Optional[str] = None


class BiasCheckResponse(BaseModel):
    """Response model for bias detection"""
    overall_risk: str
    resume_risk: Optional[str]
    job_risk: Optional[str]
    warnings: List[str]
    recommendations: List[str]


class FeedbackRequest(BaseModel):
    """Request model for user feedback"""
    session_id: str = Field(..., description="Unique session identifier")
    overall_score: float = Field(..., description="System's calculated score")
    user_rating: Optional[int] = Field(None, ge=1, le=5, description="User rating (1-5)")
    was_helpful: Optional[bool] = Field(None, description="Was the analysis helpful?")
    comments: Optional[str] = Field(None, description="User comments")
    resume_text: Optional[str] = Field(None, description="Resume content (for training)")
    job_description: Optional[str] = Field(None, description="Job description")
    matched_skills: Optional[List[str]] = Field(None, description="Matched skills")
    missing_skills: Optional[List[str]] = Field(None, description="Missing skills")
    score_breakdown: Optional[dict] = Field(None, description="Score breakdown")


# API Endpoints
@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "AI Resume Screener API",
        "version": "1.0.0",
        "endpoints": {
            "analyze": "/api/analyze",
            "analyze_file": "/api/analyze-file",
            "bias_check": "/api/bias-check",
            "health": "/health"
        }
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "resume-screener"}


@app.post("/api/analyze", response_model=AnalyzeResponse)
async def analyze_resume(request: AnalyzeRequest):
    """
    Analyze resume text against job description
    
    Args:
        request: AnalyzeRequest with resume and job description text
        
    Returns:
        AnalyzeResponse with detailed analysis
    """
    try:
        result = analyzer.analyze(
            resume_text=request.resume_text,
            job_description=request.job_description,
            required_skills=request.required_skills
        )
        
        return AnalyzeResponse(**result.to_dict())
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")


@app.post("/api/analyze-file")
async def analyze_resume_file(
    resume_file: UploadFile = File(..., description="Resume file (PDF, DOCX, TXT)"),
    job_description: str = Form(..., description="Job description text")
):
    """
    Analyze resume file against job description
    
    Args:
        resume_file: Uploaded resume file
        job_description: Job description text
        
    Returns:
        Analysis results
    """
    try:
        # Save uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix=Path(resume_file.filename).suffix) as tmp_file:
            content = await resume_file.read()
            tmp_file.write(content)
            tmp_path = tmp_file.name
        
        try:
            # Analyze
            result = analyzer.analyze(
                resume_path=tmp_path,
                job_description=job_description
            )
            
            return JSONResponse(content=result.to_dict())
            
        finally:
            # Clean up temporary file
            if os.path.exists(tmp_path):
                os.remove(tmp_path)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")


@app.post("/api/bias-check", response_model=BiasCheckResponse)
async def check_bias(request: BiasCheckRequest):
    """
    Check for potential bias in resume and/or job description
    
    Args:
        request: BiasCheckRequest with text to analyze
        
    Returns:
        BiasCheckResponse with bias detection results
    """
    try:
        if not request.resume_text and not request.job_description:
            raise HTTPException(
                status_code=400,
                detail="Either resume_text or job_description must be provided"
            )
        
        results = bias_detector.detect(
            resume_text=request.resume_text or "",
            job_description=request.job_description
        )
        
        return BiasCheckResponse(
            overall_risk=results['overall_risk'],
            resume_risk=results['resume_bias']['risk_level'] if request.resume_text else None,
            job_risk=results['job_bias']['risk_level'] if results['job_bias'] else None,
            warnings=results['warnings'],
            recommendations=results['recommendations']
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Bias check failed: {str(e)}")


@app.post("/api/batch-analyze")
async def batch_analyze(
    job_description: str = Form(..., description="Job description text"),
    resume_files: List[UploadFile] = File(..., description="Multiple resume files")
):
    """
    Analyze multiple resumes against one job description
    
    Args:
        job_description: Job description text
        resume_files: List of resume files
        
    Returns:
        List of analysis results sorted by score
    """
    try:
        results = []
        
        for resume_file in resume_files:
            # Save temporarily
            with tempfile.NamedTemporaryFile(delete=False, suffix=Path(resume_file.filename).suffix) as tmp_file:
                content = await resume_file.read()
                tmp_file.write(content)
                tmp_path = tmp_file.name
            
            try:
                # Analyze
                result = analyzer.analyze(
                    resume_path=tmp_path,
                    job_description=job_description
                )
                
                result_dict = result.to_dict()
                result_dict['filename'] = resume_file.filename
                results.append(result_dict)
                
            finally:
                if os.path.exists(tmp_path):
                    os.remove(tmp_path)
        
        # Sort by score (descending)
        results.sort(key=lambda x: x['overall_score'], reverse=True)
        
        return JSONResponse(content={
            "total_resumes": len(results),
            "results": results
        })
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Batch analysis failed: {str(e)}")


@app.post("/api/analyze-enhanced")
async def analyze_enhanced(
    resume_file: UploadFile = File(..., description="Resume file (PDF, DOCX, TXT)"),
    job_description: str = Form(..., description="Job description text")
):
    """
    Enhanced analysis with detailed explanations, ATS compatibility, and learning resources
    
    Args:
        resume_file: Uploaded resume file
        job_description: Job description text
        
    Returns:
        Enhanced analysis with:
        - Detailed score explanations
        - Skill-by-skill analysis with learning resources
        - ATS compatibility check
        - Career insights and benchmarking
        - Personalized learning roadmap
    """
    try:
        # Save uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix=Path(resume_file.filename).suffix) as tmp_file:
            content = await resume_file.read()
            tmp_file.write(content)
            tmp_path = tmp_file.name
        
        try:
            # Get basic analysis
            result = analyzer.analyze(
                resume_path=tmp_path,
                job_description=job_description
            )
            
            # Get parsed data for enhanced analysis
            from resume_screener.parsers.document_parser import ResumeParser, JobDescriptionParser
            resume_parser = ResumeParser()
            job_parser = JobDescriptionParser()
            
            resume_data = resume_parser.parse(tmp_path)
            job_data = job_parser.parse(job_description)
            
            # Generate enhanced explanation
            enhanced_result = enhanced_explainer.explain(
                score_breakdown=analyzer.score_breakdown,
                resume_data=resume_data,
                job_data=job_data,
                resume_text=resume_data.get('text', '')
            )
            
            # Build comprehensive response
            response = {
                # Basic scores
                'overall_score': result.score,
                'confidence': result.confidence,
                'classification': result.classification,
                
                # Enhanced explanations
                'summary': enhanced_result.summary,
                'score_explanations': enhanced_result.score_explanations,
                
                # Skill analysis
                'skill_analysis': [
                    {
                        'skill_name': s.skill_name,
                        'is_matched': s.is_matched,
                        'importance': s.importance,
                        'reason': s.reason,
                        'market_demand': s.market_demand,
                        'learning_resources': s.learning_resources,
                        'estimated_learning_time': s.estimated_learning_time
                    }
                    for s in enhanced_result.skill_analysis
                ],
                
                # ATS compatibility
                'ats_compatibility': {
                    'overall_score': enhanced_result.ats_compatibility.overall_score,
                    'is_ats_friendly': enhanced_result.ats_compatibility.is_ats_friendly,
                    'issues': enhanced_result.ats_compatibility.issues,
                    'recommendations': enhanced_result.ats_compatibility.recommendations,
                    'formatting_score': enhanced_result.ats_compatibility.formatting_score,
                    'keyword_optimization': enhanced_result.ats_compatibility.keyword_optimization
                },
                
                # Career insights
                'career_insights': enhanced_result.career_insights,
                
                # Recommendations
                'recommendations': enhanced_result.recommendations,
                
                # Learning roadmap
                'learning_roadmap': enhanced_result.learning_roadmap,
                
                # Industry benchmark
                'industry_benchmark': enhanced_result.industry_benchmark,
                
                # Original data
                'matched_skills': result.matched_skills,
                'missing_skills': result.missing_skills,
                'strengths': result.strengths,
                'weaknesses': result.weaknesses
            }
            
            return JSONResponse(content=response)
            
        finally:
            # Clean up temporary file
            if os.path.exists(tmp_path):
                os.remove(tmp_path)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Enhanced analysis failed: {str(e)}")


@app.get("/api/skills")
async def get_skill_database():
    """Get the skill database"""
    from resume_screener.parsers.skill_extractor import SkillExtractor
    
    extractor = SkillExtractor()
    return {
        "total_skills": len(extractor.all_skills),
        "categories": {
            category: skills 
            for category, skills in extractor.SKILL_DATABASE.items()
        }
    }


@app.post("/api/feedback")
async def submit_feedback(feedback: FeedbackRequest):
    """
    Submit user feedback on analysis results
    
    Args:
        feedback: FeedbackRequest with user's feedback
        
    Returns:
        Success status and message
    """
    try:
        storage = get_feedback_storage()
        
        success = storage.save_feedback(
            session_id=feedback.session_id,
            overall_score=feedback.overall_score,
            user_rating=feedback.user_rating,
            was_helpful=feedback.was_helpful,
            comments=feedback.comments,
            resume_text=feedback.resume_text,
            job_description=feedback.job_description,
            matched_skills=feedback.matched_skills,
            missing_skills=feedback.missing_skills,
            score_breakdown=feedback.score_breakdown
        )
        
        if success:
            return {
                "status": "success",
                "message": "Thank you for your feedback! It helps us improve."
            }
        else:
            raise HTTPException(status_code=500, detail="Failed to save feedback")
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Feedback submission failed: {str(e)}")


@app.get("/api/feedback/stats")
async def get_feedback_stats():
    """Get feedback statistics"""
    try:
        storage = get_feedback_storage()
        stats = storage.get_statistics()
        return stats
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get stats: {str(e)}")


@app.post("/api/feedback/export")
async def export_training_data():
    """Export feedback data for model training"""
    try:
        storage = get_feedback_storage()
        count = storage.export_training_data()
        return {
            "status": "success",
            "message": f"Exported {count} training examples",
            "file": "training_data.json"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Export failed: {str(e)}")


if __name__ == "__main__":
    import uvicorn
    
    print("🚀 Starting AI Resume Screener API...")
    print("📖 API Documentation: http://localhost:8000/docs")
    print("🔍 Alternative Docs: http://localhost:8000/redoc")
    
    uvicorn.run(
        "api:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
