import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))
import unittest
from nlp_engine import NLPEngine
from data_handler import DataHandler

class TestNLPEngine(unittest.TestCase):
    def setUp(self):
        self.nlp = NLPEngine()
        self.data = DataHandler()
    
    def test_clean_text(self):
        text = "ये https://test.com बहुत अच्छा है! @user #tag"
        result = self.nlp.clean_text(text)
        self.assertNotIn("https", result)
        self.assertNotIn("@", result)
        self.assertNotIn("#", result)
    
    def test_predict_positive(self):
        result = self.nlp.predict_sentiment("बहुत अच्छी फिल्म है कमाल की")
        self.assertEqual(result['sentiment'], 1)
        self.assertGreater(result['confidence'], 0.5)
    
    def test_predict_negative(self):
        result = self.nlp.predict_sentiment("बकवास फिल्म बेकार")
        self.assertEqual(result['sentiment'], 0)
        self.assertGreater(result['confidence'], 0.5)
    
    def test_empty_text(self):
        result = self.nlp.predict_sentiment("")
        self.assertEqual(result['cleaned_text'], "")

if __name__ == '__main__':
    unittest.main()
