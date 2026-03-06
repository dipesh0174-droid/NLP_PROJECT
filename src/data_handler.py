import os
import yaml
import json
from datetime import datetime
from typing import Dict, Any
import pandas as pd

class DataHandler:
    def __init__(self, config_path='../config.yaml'):
        self.config_path = config_path
        try:
            with open(self.config_path, 'r') as f:
                self.config = yaml.safe_load(f)
        except:
            self.config = {'paths': {'logs': 'logs', 'cache': 'data/cache'}}
        
        os.makedirs('logs', exist_ok=True)
        os.makedirs('data/cache', exist_ok=True)
        self.predictions_log = 'logs/predictions.jsonl'
    
    def log_prediction(self, result: Dict[str, Any]):
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'sentiment': result['sentiment'],
            'confidence': result['confidence'],
            'text_length': len(result['original_text'])
        }
        
        with open(self.predictions_log, 'a') as f:
            f.write(json.dumps(log_entry) + '\n')
    
    def get_stats(self) -> Dict[str, Any]:
        if not os.path.exists(self.predictions_log):
            return {'total': 0, 'positive': 0, 'negative': 0, 'positive_pct': 0}
        
        df = pd.read_json(self.predictions_log, lines=True)
        total = len(df)
        positive = len(df[df['sentiment'] == 1])
        
        return {
            'total': total,
            'positive': positive,
            'negative': total - positive,
            'positive_pct': round((positive/total)*100, 1) if total > 0 else 0
        }

data_handler = DataHandler()
