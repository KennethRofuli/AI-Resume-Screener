"""
Document Parser for Resume and Job Description Processing
Supports PDF, DOCX, and TXT formats
"""

import re
from pathlib import Path
from typing import Optional, Dict, Any
import logging

try:
    import PyPDF2
except ImportError:
    PyPDF2 = None

try:
    from docx import Document
except ImportError:
    Document = None

try:
    import pdfplumber
except ImportError:
    pdfplumber = None

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DocumentParser:
    """Parse various document formats to extract text"""
    
    @staticmethod
    def parse_pdf_pypdf2(file_path: str) -> str:
        """Parse PDF using PyPDF2"""
        if PyPDF2 is None:
            raise ImportError("PyPDF2 not installed. Install with: pip install PyPDF2")
        
        text = ""
        with open(file_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            for page in reader.pages:
                text += page.extract_text() + "\n"
        return text
    
    @staticmethod
    def parse_pdf_pdfplumber(file_path: str) -> str:
        """Parse PDF using pdfplumber (better for complex layouts)"""
        if pdfplumber is None:
            raise ImportError("pdfplumber not installed. Install with: pip install pdfplumber")
        
        text = ""
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
        return text
    
    @staticmethod
    def parse_docx(file_path: str) -> str:
        """Parse DOCX file"""
        if Document is None:
            raise ImportError("python-docx not installed. Install with: pip install python-docx")
        
        doc = Document(file_path)
        text = "\n".join([paragraph.text for paragraph in doc.paragraphs])
        return text
    
    @staticmethod
    def parse_txt(file_path: str) -> str:
        """Parse TXT file"""
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
            return file.read()
    
    @classmethod
    def parse(cls, file_path: str, use_pdfplumber: bool = True) -> str:
        """
        Auto-detect and parse document
        
        Args:
            file_path: Path to document
            use_pdfplumber: Use pdfplumber for PDFs (better quality)
            
        Returns:
            Extracted text
        """
        path = Path(file_path)
        
        if not path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        
        extension = path.suffix.lower()
        
        try:
            if extension == '.pdf':
                if use_pdfplumber and pdfplumber:
                    logger.info(f"Parsing PDF with pdfplumber: {file_path}")
                    text = cls.parse_pdf_pdfplumber(file_path)
                else:
                    logger.info(f"Parsing PDF with PyPDF2: {file_path}")
                    text = cls.parse_pdf_pypdf2(file_path)
            elif extension == '.docx':
                logger.info(f"Parsing DOCX: {file_path}")
                text = cls.parse_docx(file_path)
            elif extension == '.txt':
                logger.info(f"Parsing TXT: {file_path}")
                text = cls.parse_txt(file_path)
            else:
                raise ValueError(f"Unsupported file format: {extension}")
            
            # Clean and normalize text
            text = cls.clean_text(text)
            return text
            
        except Exception as e:
            logger.error(f"Error parsing {file_path}: {str(e)}")
            raise
    
    @staticmethod
    def clean_text(text: str) -> str:
        """Clean and normalize extracted text"""
        # Remove excessive whitespace
        text = re.sub(r'\s+', ' ', text)
        # Remove special characters but keep important punctuation
        text = re.sub(r'[^\w\s\.\,\-\:\;\(\)\@\#\+]', '', text)
        # Trim
        text = text.strip()
        return text


class ResumeParser:
    """Parse and extract structured information from resumes"""
    
    def __init__(self):
        self.document_parser = DocumentParser()
    
    def parse(self, file_path: str) -> Dict[str, Any]:
        """
        Parse resume and extract structured data
        
        Args:
            file_path: Path to resume file
            
        Returns:
            Dictionary with parsed resume data
        """
        # Extract raw text
        raw_text = self.document_parser.parse(file_path)
        
        # Extract structured information
        result = {
            'raw_text': raw_text,
            'email': self._extract_email(raw_text),
            'phone': self._extract_phone(raw_text),
            'education': self._extract_education(raw_text),
            'experience_years': self._estimate_experience(raw_text),
            'sections': self._identify_sections(raw_text)
        }
        
        return result
    
    @staticmethod
    def _extract_email(text: str) -> Optional[str]:
        """Extract email address"""
        pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        match = re.search(pattern, text)
        return match.group(0) if match else None
    
    @staticmethod
    def _extract_phone(text: str) -> Optional[str]:
        """Extract phone number"""
        patterns = [
            r'\b\d{3}[-.\s]?\d{3}[-.\s]?\d{4}\b',
            r'\b\(\d{3}\)\s*\d{3}[-.\s]?\d{4}\b',
            r'\b\+\d{1,3}[-.\s]?\d{3}[-.\s]?\d{3}[-.\s]?\d{4}\b'
        ]
        for pattern in patterns:
            match = re.search(pattern, text)
            if match:
                return match.group(0)
        return None
    
    @staticmethod
    def _extract_education(text: str) -> list:
        """Extract education information"""
        education_keywords = [
            r'\b(Bachelor|B\.S\.|B\.A\.|BS|BA)\b',
            r'\b(Master|M\.S\.|M\.A\.|MS|MA|MBA)\b',
            r'\b(Ph\.?D\.?|Doctorate)\b',
            r'\b(Associate|A\.S\.|A\.A\.)\b'
        ]
        
        education = []
        for pattern in education_keywords:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                # Extract context around match
                start = max(0, match.start() - 50)
                end = min(len(text), match.end() + 50)
                context = text[start:end].strip()
                education.append(context)
        
        return education
    
    @staticmethod
    def _estimate_experience(text: str) -> Optional[float]:
        """Estimate years of experience"""
        # Look for patterns like "5 years", "5+ years", "5-7 years"
        patterns = [
            r'(\d+)\+?\s*years?\s+(?:of\s+)?experience',
            r'experience\s+of\s+(\d+)\+?\s*years?',
            r'(\d+)\+?\s*years?\s+(?:in|with)'
        ]
        
        years = []
        for pattern in patterns:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                try:
                    years.append(int(match.group(1)))
                except (ValueError, IndexError):
                    continue
        
        return max(years) if years else None
    
    @staticmethod
    def _identify_sections(text: str) -> Dict[str, str]:
        """Identify major resume sections"""
        sections = {}
        
        # Common section headers
        section_patterns = {
            'experience': r'(?:work\s+)?experience|employment\s+history|professional\s+experience',
            'education': r'education|academic\s+background|qualifications',
            'skills': r'(?:technical\s+)?skills|competencies|expertise',
            'summary': r'summary|objective|profile|about\s+me',
            'projects': r'projects|portfolio',
            'certifications': r'certifications?|licenses?'
        }
        
        text_lower = text.lower()
        for section_name, pattern in section_patterns.items():
            match = re.search(pattern, text_lower)
            if match:
                sections[section_name] = match.group(0)
        
        return sections


class JobDescriptionParser:
    """Parse and extract structured information from job descriptions"""
    
    def __init__(self):
        self.document_parser = DocumentParser()
    
    def parse(self, text_or_path: str) -> Dict[str, Any]:
        """
        Parse job description
        
        Args:
            text_or_path: Job description text or file path
            
        Returns:
            Dictionary with parsed job data
        """
        # Check if input is a file path
        if Path(text_or_path).exists():
            raw_text = self.document_parser.parse(text_or_path)
        else:
            raw_text = text_or_path
        
        result = {
            'raw_text': raw_text,
            'job_title': self._extract_job_title(raw_text),
            'required_experience': self._extract_experience_requirement(raw_text),
            'sections': self._identify_sections(raw_text)
        }
        
        return result
    
    @staticmethod
    def _extract_job_title(text: str) -> Optional[str]:
        """Extract job title (simple heuristic)"""
        # Usually in first few lines
        lines = text.split('\n')[:5]
        for line in lines:
            line = line.strip()
            if 10 < len(line) < 100 and not line.startswith('http'):
                return line
        return None
    
    @staticmethod
    def _extract_experience_requirement(text: str) -> Optional[str]:
        """Extract experience requirements"""
        pattern = r'(\d+)\+?\s*years?\s+(?:of\s+)?experience'
        match = re.search(pattern, text, re.IGNORECASE)
        return match.group(0) if match else None
    
    @staticmethod
    def _identify_sections(text: str) -> Dict[str, str]:
        """Identify job description sections"""
        sections = {}
        
        section_patterns = {
            'requirements': r'requirements?|qualifications?|what\s+(?:we|you)\s+(?:need|bring)',
            'responsibilities': r'responsibilities?|duties|what\s+you(?:\'ll|\s+will)\s+do',
            'benefits': r'benefits?|what\s+we\s+offer|perks',
            'about': r'about\s+(?:us|the\s+company|the\s+role)'
        }
        
        text_lower = text.lower()
        for section_name, pattern in section_patterns.items():
            match = re.search(pattern, text_lower)
            if match:
                sections[section_name] = match.group(0)
        
        return sections


if __name__ == "__main__":
    # Test parsers
    print("Document Parser Test")
    
    # Test with sample text
    sample_resume = """
    John Doe
    john.doe@email.com | (555) 123-4567
    
    EXPERIENCE
    Senior Software Engineer - TechCorp (2020-Present)
    - 5 years of experience in Python development
    
    EDUCATION
    Master of Science in Computer Science
    University of Technology, 2018
    
    SKILLS
    Python, Django, Machine Learning, AWS
    """
    
    resume_parser = ResumeParser()
    result = {
        'email': resume_parser._extract_email(sample_resume),
        'phone': resume_parser._extract_phone(sample_resume),
        'experience': resume_parser._estimate_experience(sample_resume),
        'sections': resume_parser._identify_sections(sample_resume)
    }
    
    print("\nParsed Resume Info:")
    for key, value in result.items():
        print(f"{key}: {value}")
