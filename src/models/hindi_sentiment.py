class HindiSentimentPredictor:
    def __init__(self):
        self.positive_words = [
            'अच्छा', 'बहुत अच्छा', 'कमाल', 'शानदार', 'मजा', 'बेस्ट', 'सुपर',
            'अद्भुत', 'चमत्कार', 'महान', 'उत्तम', 'प्रयासरत'
        ]
        self.negative_words = [
            'बकवास', 'खराब', 'बुरा', 'बेकार', 'बोरिंग', 'घिनौना', 'निराशाजनक'
        ]
    
    def predict(self, text):
        text_lower = text.lower()
        pos_score = sum(1 for word in self.positive_words if word in text_lower)
        neg_score = sum(1 for word in self.negative_words if word in text_lower)
        
        if pos_score > neg_score:
            return {'sentiment': 1, 'confidence': 0.85 + pos_score*0.05}
        else:
            return {'sentiment': 0, 'confidence': 0.85 + neg_score*0.05}
