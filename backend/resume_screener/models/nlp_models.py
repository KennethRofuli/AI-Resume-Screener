"""
NLP Model Service for Resume Screening
Handles BERT/SBERT embeddings and semantic similarity
"""

import torch
from sentence_transformers import SentenceTransformer, util
from transformers import AutoTokenizer, AutoModel
import numpy as np
from typing import List, Union, Tuple
import logging
from pathlib import Path

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class EmbeddingModel:
    """Handles text embeddings using Sentence-BERT"""
    
    def __init__(self, model_name: str = 'sentence-transformers/all-MiniLM-L6-v2'):
        """
        Initialize the embedding model
        
        Args:
            model_name: HuggingFace model identifier
        """
        logger.info(f"Loading embedding model: {model_name}")
        self.model = SentenceTransformer(model_name)
        self.device = 'cuda' if torch.cuda.is_available() else 'cpu'
        self.model.to(self.device)
        logger.info(f"Model loaded on device: {self.device}")
    
    def encode(self, texts: Union[str, List[str]], 
               batch_size: int = 32,
               show_progress: bool = False) -> np.ndarray:
        """
        Generate embeddings for text(s)
        
        Args:
            texts: Single text or list of texts
            batch_size: Batch size for encoding
            show_progress: Show progress bar
            
        Returns:
            numpy array of embeddings
        """
        if isinstance(texts, str):
            texts = [texts]
        
        embeddings = self.model.encode(
            texts,
            batch_size=batch_size,
            show_progress_bar=show_progress,
            convert_to_numpy=True
        )
        return embeddings
    
    def compute_similarity(self, text1: str, text2: str) -> float:
        """
        Compute cosine similarity between two texts
        
        Args:
            text1: First text
            text2: Second text
            
        Returns:
            Similarity score (0-1)
        """
        embeddings = self.encode([text1, text2])
        similarity = util.cos_sim(embeddings[0], embeddings[1])
        return float(similarity.item())
    
    def compute_similarity_matrix(self, texts1: List[str], 
                                   texts2: List[str]) -> np.ndarray:
        """
        Compute similarity matrix between two lists of texts
        
        Args:
            texts1: First list of texts
            texts2: Second list of texts
            
        Returns:
            Similarity matrix (len(texts1) x len(texts2))
        """
        embeddings1 = self.encode(texts1)
        embeddings2 = self.encode(texts2)
        
        similarity_matrix = util.cos_sim(embeddings1, embeddings2)
        return similarity_matrix.cpu().numpy()


class BERTModel:
    """Handles BERT-based contextual embeddings"""
    
    def __init__(self, model_name: str = 'bert-base-uncased'):
        """
        Initialize BERT model
        
        Args:
            model_name: HuggingFace model identifier
        """
        logger.info(f"Loading BERT model: {model_name}")
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModel.from_pretrained(model_name)
        self.device = 'cuda' if torch.cuda.is_available() else 'cpu'
        self.model.to(self.device)
        self.model.eval()
        logger.info(f"BERT model loaded on device: {self.device}")
    
    def get_embeddings(self, text: str, 
                       pooling: str = 'mean') -> np.ndarray:
        """
        Get BERT embeddings for text
        
        Args:
            text: Input text
            pooling: Pooling strategy ('mean', 'cls', or 'max')
            
        Returns:
            Embedding vector
        """
        # Tokenize
        inputs = self.tokenizer(
            text,
            return_tensors='pt',
            truncation=True,
            max_length=512,
            padding=True
        ).to(self.device)
        
        # Get embeddings
        with torch.no_grad():
            outputs = self.model(**inputs)
            hidden_states = outputs.last_hidden_state
        
        # Apply pooling
        if pooling == 'mean':
            embedding = hidden_states.mean(dim=1)
        elif pooling == 'cls':
            embedding = hidden_states[:, 0, :]
        elif pooling == 'max':
            embedding = hidden_states.max(dim=1)[0]
        else:
            raise ValueError(f"Unknown pooling strategy: {pooling}")
        
        return embedding.cpu().numpy()


class SemanticMatcher:
    """High-level semantic matching interface"""
    
    def __init__(self, use_sbert: bool = True, use_bert: bool = False):
        """
        Initialize semantic matcher
        
        Args:
            use_sbert: Use Sentence-BERT (recommended)
            use_bert: Use standard BERT (optional, for comparison)
        """
        self.sbert_model = EmbeddingModel() if use_sbert else None
        self.bert_model = BERTModel() if use_bert else None
    
    def match_resume_to_job(self, resume_text: str, 
                            job_description: str) -> dict:
        """
        Match resume to job description
        
        Args:
            resume_text: Full resume text
            job_description: Job posting text
            
        Returns:
            Dictionary with similarity scores and details
        """
        results = {}
        
        if self.sbert_model:
            sbert_score = self.sbert_model.compute_similarity(
                resume_text, 
                job_description
            )
            results['sbert_similarity'] = round(sbert_score, 4)
        
        if self.bert_model:
            resume_emb = self.bert_model.get_embeddings(resume_text)
            job_emb = self.bert_model.get_embeddings(job_description)
            
            # Cosine similarity
            bert_score = float(np.dot(resume_emb[0], job_emb[0]) / 
                             (np.linalg.norm(resume_emb[0]) * 
                              np.linalg.norm(job_emb[0])))
            results['bert_similarity'] = round(bert_score, 4)
        
        # Calculate overall score
        scores = [v for v in results.values()]
        results['overall_similarity'] = round(np.mean(scores), 4) if scores else 0.0
        
        return results
    
    def match_skills(self, resume_skills: List[str], 
                     required_skills: List[str]) -> dict:
        """
        Match resume skills against required skills
        
        Args:
            resume_skills: List of skills from resume
            required_skills: List of required skills from job
            
        Returns:
            Dictionary with matching details
        """
        if not self.sbert_model:
            raise ValueError("SBERT model required for skill matching")
        
        if not resume_skills or not required_skills:
            return {
                'matched_skills': [],
                'missing_skills': required_skills,
                'match_rate': 0.0
            }
        
        # Compute similarity matrix
        similarity_matrix = self.sbert_model.compute_similarity_matrix(
            resume_skills, 
            required_skills
        )
        
        # Find matches (threshold: 0.7)
        threshold = 0.7
        matched_skills = []
        matched_details = []
        missing_skills = []
        
        for j, req_skill in enumerate(required_skills):
            max_sim = similarity_matrix[:, j].max()
            if max_sim >= threshold:
                best_match_idx = similarity_matrix[:, j].argmax()
                matched_skills.append(req_skill)
                matched_details.append({
                    'required': req_skill,
                    'matched': resume_skills[best_match_idx],
                    'similarity': round(float(max_sim), 4)
                })
            else:
                missing_skills.append(req_skill)
        
        match_rate = len(matched_skills) / len(required_skills)
        
        return {
            'matched_skills': matched_skills,
            'matched_details': matched_details,
            'missing_skills': missing_skills,
            'match_rate': round(match_rate, 4),
            'total_required': len(required_skills),
            'total_matched': len(matched_skills)
        }


if __name__ == "__main__":
    # Test the models
    print("Testing Semantic Matcher...")
    
    matcher = SemanticMatcher(use_sbert=True)
    
    # Test resume to job matching
    resume = "Software engineer with 5 years Python experience, Django, Flask, REST APIs"
    job = "Looking for Python developer with Django and API development experience"
    
    result = matcher.match_resume_to_job(resume, job)
    print(f"\nResume-Job Match: {result}")
    
    # Test skill matching
    resume_skills = ["Python", "Django", "JavaScript", "Git"]
    required_skills = ["Python", "Flask", "Docker", "AWS"]
    
    skill_result = matcher.match_skills(resume_skills, required_skills)
    print(f"\nSkill Match: {skill_result}")
