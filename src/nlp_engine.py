import yaml
import numpy as np
import re
import logging
import random
from typing import Dict, List, Any

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class NLPEngine:
    def __init__(self, config_path='../config.yaml'):
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                self.config = yaml.safe_load(f)
        except:
            self.config = {'nlp': {'max_length': 128}}
        
        self.positive_keywords = ['अच्छा', 'बहुत अच्छा', 'कमाल', 'शानदार', 'मजा', 'बेस्ट', 'सुपर']
        self.negative_keywords = ['बकवास', 'खराब', 'बोरिंग', 'बेकार', 'बचें', 'बुरा']
        logger.info("NLP Engine initialized - Rule-based Hindi Sentiment")
    
    def clean_text(self, text: str) -> str:
        if not text:
            return ""
        text = re.sub(r'http\S+|www\S+|https\S+', '', str(text))
        text = re.sub(r'@\w+|#\w+', '', text)
        text = re.sub(r'[^\w\s।?!]', ' ', text)
        return text.strip()
    
    def predict_sentiment(self, text: str) -> Dict[str, Any]:
        cleaned_text = self.clean_text(text)
        text_lower = cleaned_text.lower()
        
        pos_count = sum(1 for word in self.positive_keywords if word in text_lower)
        neg_count = sum(1 for word in self.negative_keywords if word in text_lower)
        
        if pos_count > neg_count:
            sentiment = 1
            confidence = min(0.95, 0.6 + pos_count * 0.1)
        elif neg_count > pos_count:
            sentiment = 0
            confidence = min(0.95, 0.6 + neg_count * 0.1)
        else:
            sentiment = 1
            confidence = 0.55
        
        probs = [1-confidence, confidence] if sentiment == 1 else [confidence, 1-confidence]
        
        return {
            'sentiment': sentiment,
            'confidence': float(confidence),
            'probs': probs,
            'original_text': text,
            'cleaned_text': cleaned_text,
            'tokens_count': len(cleaned_text.split())
        }

nlp_engine = NLPEngine()
