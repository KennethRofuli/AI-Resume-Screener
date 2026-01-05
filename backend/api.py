"""
FastAPI REST API for Resume Screening Service
"""

from fastapi import FastAPI, UploadFile, File, Form, HTTPException, Depends, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field, model_validator
from typing import Optional, List
import tempfile
import os
from pathlib import Path
import logging
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

from resume_screener import ResumeAnalyzer
from resume_screener.bias_detection import BiasDetector
from resume_screener.explainability.enhanced_explainer import EnhancedExplainabilityEngine
from feedback_storage import get_feedback_storage
from config import config
from security import (
    verify_api_key,
    validate_file_upload,
    validate_text_input,
    sanitize_filename,
    validate_batch_size
)
import uuid

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize rate limiter
limiter = Limiter(key_func=get_remote_address)

# Initialize FastAPI app
app = FastAPI(
    title="AI Resume Screener API",
    description="Intelligent resume screening with NLP and bias detection",
    version="1.0.0",
    docs_url="/docs" if not config.REQUIRE_API_KEY else None,  # Disable docs in production
    redoc_url="/redoc" if not config.REQUIRE_API_KEY else None
)

# Add rate limiter to app
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# CORS middleware - Configure with specific origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=config.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type", "X-API-Key"],
    max_age=3600,  # Cache preflight requests for 1 hour
)

# Initialize components
analyzer = ResumeAnalyzer(use_sbert=True, use_spacy=False)
bias_detector = BiasDetector()
enhanced_explainer = EnhancedExplainabilityEngine()


# Request/Response Models
class AnalyzeRequest(BaseModel):
    """Request model for text-based analysis"""
    resume_text: str = Field(..., description="Resume text content", max_length=config.MAX_TEXT_LENGTH)
    job_description: str = Field(..., description="Job description text", max_length=config.MAX_TEXT_LENGTH)
    required_skills: Optional[List[str]] = Field(None, description="Optional list of required skills")
    
    @model_validator(mode='after')
    def validate_not_empty(self) -> 'AnalyzeRequest':
        if not self.resume_text or not self.resume_text.strip():
            raise ValueError('resume_text cannot be empty')
        if not self.job_description or not self.job_description.strip():
            raise ValueError('job_description cannot be empty')
        return self


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
@limiter.limit(f"{config.RATE_LIMIT_PER_MINUTE}/minute")
async def root(request: Request):
    """Root endpoint"""
    return {
        "message": "AI Resume Screener API",
        "version": "1.0.0",
        "endpoints": {
            "analyze": "/api/analyze",
            "analyze_file": "/api/analyze-file",
            "bias_check": "/api/bias-check",
            "health": "/health"
        },
        "security": config.get_settings_info()
    }


@app.get("/health")
@limiter.limit("60/minute")
async def health_check(request: Request):
    """Health check endpoint"""
    return {"status": "healthy", "service": "resume-screener"}


@app.post("/api/analyze", response_model=AnalyzeResponse)
@limiter.limit(f"{config.RATE_LIMIT_PER_MINUTE}/minute")
async def analyze_resume(
    request: Request,
    data: AnalyzeRequest,
    api_key: str = Depends(verify_api_key)
):
    """
    Analyze resume text against job description
    
    Args:
        data: AnalyzeRequest with resume and job description text
        api_key: API key from header (required if auth enabled)
        
    Returns:
        AnalyzeResponse with detailed analysis
    """
    try:
        # Validate inputs
        validate_text_input(data.resume_text, "resume_text")
        validate_text_input(data.job_description, "job_description")
        
        logger.info(f"Analyzing resume (text length: {len(data.resume_text)})")
        
        result = analyzer.analyze(
            resume_text=data.resume_text,
            job_description=data.job_description,
            required_skills=data.required_skills
        )
        
        return AnalyzeResponse(**result.to_dict())
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Analysis failed: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="Analysis failed. Please try again.")


@app.post("/api/analyze-file")
@limiter.limit(f"{config.RATE_LIMIT_PER_MINUTE}/minute")
async def analyze_resume_file(
    request: Request,
    resume_file: UploadFile = File(..., description="Resume file (PDF, DOCX, TXT)"),
    job_description: str = Form(..., description="Job description text"),
    api_key: str = Depends(verify_api_key)
):
    """
    Analyze resume file against job description
    
    Args:
        resume_file: Uploaded resume file
        job_description: Job description text
        api_key: API key from header (required if auth enabled)
        
    Returns:
        Analysis results
    """
    try:
        # Validate job description
        validate_text_input(job_description, "job_description")
        
        # Read and validate file
        content = await resume_file.read()
        await validate_file_upload(content, resume_file.filename)
        
        # Sanitize filename
        safe_filename = sanitize_filename(resume_file.filename or "resume.pdf")
        
        logger.info(f"Analyzing file: {safe_filename} ({len(content)} bytes)")
        
        # Save uploaded file temporarily with sanitized name
        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=Path(safe_filename).suffix,
            prefix="resume_"
        ) as tmp_file:
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
                try:
                    os.remove(tmp_path)
                except Exception as e:
                    logger.warning(f"Failed to remove temp file: {e}")
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"File analysis failed: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="Analysis failed. Please try again.")


@app.post("/api/bias-check", response_model=BiasCheckResponse)
@limiter.limit(f"{config.RATE_LIMIT_PER_MINUTE}/minute")
async def check_bias(
    request: Request,
    data: BiasCheckRequest,
    api_key: str = Depends(verify_api_key)
):
    """
    Check for potential bias in resume and/or job description
    
    Args:
        data: BiasCheckRequest with text to analyze
        api_key: API key from header (required if auth enabled)
        
    Returns:
        BiasCheckResponse with bias detection results
    """
    try:
        if not data.resume_text and not data.job_description:
            raise HTTPException(
                status_code=400,
                detail="Either resume_text or job_description must be provided"
            )
        
        # Validate text inputs if provided
        if data.resume_text:
            validate_text_input(data.resume_text, "resume_text")
        if data.job_description:
            validate_text_input(data.job_description, "job_description")
        
        results = bias_detector.detect(
            resume_text=data.resume_text or "",
            job_description=data.job_description
        )
        
        return BiasCheckResponse(
            overall_risk=results['overall_risk'],
            resume_risk=results['resume_bias']['risk_level'] if data.resume_text else None,
            job_risk=results['job_bias']['risk_level'] if results['job_bias'] else None,
            warnings=results['warnings'],
            recommendations=results['recommendations']
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Bias check failed: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="Bias check failed. Please try again.")


@app.post("/api/batch-analyze")
@limiter.limit(f"{config.RATE_LIMIT_PER_HOUR}/hour")
async def batch_analyze(
    request: Request,
    job_description: str = Form(..., description="Job description text"),
    resume_files: List[UploadFile] = File(..., description="Multiple resume files"),
    api_key: str = Depends(verify_api_key)
):
    """
    Analyze multiple resumes against one job description
    
    Args:
        job_description: Job description text
        resume_files: List of resume files
        api_key: API key from header (required if auth enabled)
        
    Returns:
        List of analysis results sorted by score
    """
    try:
        # Validate batch size
        await validate_batch_size(len(resume_files))
        
        # Validate job description
        validate_text_input(job_description, "job_description")
        
        logger.info(f"Batch analysis: {len(resume_files)} files")
        
        results = []
        
        for resume_file in resume_files:
            try:
                # Read and validate file
                content = await resume_file.read()
                await validate_file_upload(content, resume_file.filename)
                
                # Sanitize filename
                safe_filename = sanitize_filename(resume_file.filename or "resume.pdf")
                
                # Save temporarily
                with tempfile.NamedTemporaryFile(
                    delete=False,
                    suffix=Path(safe_filename).suffix,
                    prefix="batch_resume_"
                ) as tmp_file:
                    tmp_file.write(content)
                    tmp_path = tmp_file.name
                
                try:
                    # Analyze
                    result = analyzer.analyze(
                        resume_path=tmp_path,
                        job_description=job_description
                    )
                    
                    result_dict = result.to_dict()
                    result_dict['filename'] = safe_filename
                    results.append(result_dict)
                    
                finally:
                    if os.path.exists(tmp_path):
                        try:
                            os.remove(tmp_path)
                        except Exception as e:
                            logger.warning(f"Failed to remove temp file: {e}")
            
            except HTTPException as e:
                # Log validation errors but continue with other files
                logger.warning(f"File {resume_file.filename} failed validation: {e.detail}")
                results.append({
                    'filename': resume_file.filename,
                    'error': str(e.detail),
                    'overall_score': 0
                })
            except Exception as e:
                logger.error(f"Error processing {resume_file.filename}: {str(e)}")
                results.append({
                    'filename': resume_file.filename,
                    'error': 'Processing failed',
                    'overall_score': 0
                })
        
        # Sort by score (descending)
        results.sort(key=lambda x: x['overall_score'], reverse=True)
        
        return JSONResponse(content={
            "total_resumes": len(results),
            "successful": len([r for r in results if 'error' not in r]),
            "failed": len([r for r in results if 'error' in r]),
            "results": results
        })
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Batch analysis failed: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="Batch analysis failed. Please try again.")


@app.post("/api/analyze-enhanced")
@limiter.limit(f"{config.RATE_LIMIT_PER_MINUTE}/minute")
async def analyze_enhanced(
    request: Request,
    resume_file: UploadFile = File(..., description="Resume file (PDF, DOCX, TXT)"),
    job_description: str = Form(..., description="Job description text"),
    api_key: str = Depends(verify_api_key)
):
    """
    Enhanced analysis with detailed explanations, ATS compatibility, and learning resources
    
    Args:
        resume_file: Uploaded resume file
        job_description: Job description text
        api_key: API key from header (required if auth enabled)
        
    Returns:
        Enhanced analysis with:
        - Detailed score explanations
        - Skill-by-skill analysis with learning resources
        - ATS compatibility check
        - Career insights and benchmarking
        - Personalized learning roadmap
    """
    try:
        # Validate job description
        validate_text_input(job_description, "job_description")
        
        # Read and validate file
        content = await resume_file.read()
        await validate_file_upload(content, resume_file.filename)
        
        # Sanitize filename
        safe_filename = sanitize_filename(resume_file.filename or "resume.pdf")
        
        # Save uploaded file temporarily
        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=Path(safe_filename).suffix,
            prefix="enhanced_"
        ) as tmp_file:
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
                try:
                    os.remove(tmp_path)
                except Exception as e:
                    logger.warning(f"Failed to remove temp file: {e}")
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Enhanced analysis failed: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="Enhanced analysis failed. Please try again.")


@app.get("/api/skills")
@limiter.limit(f"{config.RATE_LIMIT_PER_MINUTE}/minute")
async def get_skill_database(
    request: Request,
    api_key: str = Depends(verify_api_key)
):
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
@limiter.limit("20/minute")
async def submit_feedback(
    request: Request,
    data: FeedbackRequest,
    api_key: str = Depends(verify_api_key)
):
    """
    Submit user feedback on analysis results
    
    Args:
        data: FeedbackRequest with user's feedback
        api_key: API key from header (required if auth enabled)
        
    Returns:
        Success status and message
    """
    try:
        # Validate comments length if provided
        if data.comments and len(data.comments) > 5000:
            raise HTTPException(
                status_code=400,
                detail="Comments too long. Maximum 5000 characters"
            )
        
        storage = get_feedback_storage()
        
        success = storage.save_feedback(
            session_id=data.session_id,
            overall_score=data.overall_score,
            user_rating=data.user_rating,
            was_helpful=data.was_helpful,
            comments=data.comments,
            resume_text=data.resume_text,
            job_description=data.job_description,
            matched_skills=data.matched_skills,
            missing_skills=data.missing_skills,
            score_breakdown=data.score_breakdown
        )
        
        if success:
            return {
                "status": "success",
                "message": "Thank you for your feedback! It helps us improve."
            }
        else:
            raise HTTPException(status_code=500, detail="Failed to save feedback")
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Feedback submission failed: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="Feedback submission failed. Please try again.")


@app.get("/api/feedback/stats")
@limiter.limit(f"{config.RATE_LIMIT_PER_MINUTE}/minute")
async def get_feedback_stats(
    request: Request,
    api_key: str = Depends(verify_api_key)
):
    """Get feedback statistics"""
    try:
        storage = get_feedback_storage()
        stats = storage.get_statistics()
        return stats
    except Exception as e:
        logger.error(f"Failed to get stats: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="Failed to get statistics")


@app.post("/api/feedback/export")
@limiter.limit("5/hour")
async def export_training_data(
    request: Request,
    api_key: str = Depends(verify_api_key)
):
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
        logger.error(f"Export failed: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="Export failed")


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

