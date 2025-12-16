"""
Simple test script to verify installation
"""

def test_imports():
    """Test that all modules can be imported"""
    print("Testing imports...")
    
    try:
        print("  ✓ Importing numpy...")
        import numpy
        
        print("  ✓ Importing pandas...")
        import pandas
        
        print("  ✓ Importing sklearn...")
        import sklearn
        
        print("  ✓ Importing torch...")
        import torch
        print(f"    PyTorch version: {torch.__version__}")
        print(f"    CUDA available: {torch.cuda.is_available()}")
        
        print("  ✓ Importing transformers...")
        import transformers
        
        print("  ✓ Importing sentence_transformers...")
        import sentence_transformers
        
        print("  ✓ Importing fastapi...")
        import fastapi
        
        print("\n✅ All core dependencies imported successfully!")
        return True
        
    except ImportError as e:
        print(f"\n❌ Import error: {e}")
        print("\nPlease run: pip install -r requirements.txt")
        return False


def test_resume_screener():
    """Test the resume screener package"""
    print("\n" + "="*60)
    print("Testing Resume Screener Package...")
    print("="*60)
    
    try:
        from resume_screener import ResumeAnalyzer
        print("  ✓ ResumeAnalyzer imported")
        
        from resume_screener.models import SemanticMatcher
        print("  ✓ SemanticMatcher imported")
        
        from resume_screener.parsers import SkillExtractor
        print("  ✓ SkillExtractor imported")
        
        from resume_screener.scoring import ScoringEngine
        print("  ✓ ScoringEngine imported")
        
        from resume_screener.explainability import ExplainabilityEngine
        print("  ✓ ExplainabilityEngine imported")
        
        from resume_screener.bias_detection import BiasDetector
        print("  ✓ BiasDetector imported")
        
        print("\n✅ All resume screener components loaded successfully!")
        
        # Quick functional test
        print("\n" + "="*60)
        print("Running Quick Functional Test...")
        print("="*60)
        
        print("\n📦 Initializing analyzer (this may take a moment)...")
        analyzer = ResumeAnalyzer(use_sbert=True, use_spacy=False)
        print("  ✓ Analyzer initialized")
        
        # Test with minimal data
        test_resume = "Software engineer with Python and Django experience"
        test_job = "Looking for Python developer with Django skills"
        
        print("\n🔍 Running test analysis...")
        result = analyzer.analyze(
            resume_text=test_resume,
            job_description=test_job
        )
        print("  ✓ Analysis completed")
        
        print(f"\n📊 Test Results:")
        print(f"  • Score: {result.score:.1f}/100")
        print(f"  • Classification: {result.classification}")
        print(f"  • Matched skills: {len(result.matched_skills)}")
        
        print("\n✅ Functional test passed!")
        return True
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Run all tests"""
    print("="*60)
    print("AI Resume Screener - Installation Test")
    print("="*60)
    print()
    
    # Test imports
    if not test_imports():
        return
    
    # Test package
    if not test_resume_screener():
        return
    
    print("\n" + "="*60)
    print("🎉 All tests passed! System is ready to use.")
    print("="*60)
    print("\nNext steps:")
    print("  1. Run demo: python demo.py")
    print("  2. Start API: python api.py")
    print("  3. Read QUICKSTART.md for more examples")
    print()


if __name__ == "__main__":
    main()
