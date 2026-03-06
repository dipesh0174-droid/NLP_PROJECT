import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import logging
import requests

load_dotenv()
app = Flask(__name__)
app.secret_key = 'professional_nlp_2026_secret'
app.config['MAX_CONTENT_LENGTH'] = 1 * 1024 * 1024
CORS(app)

# NLP Engine
try:
    from src.nlp_engine import NLPEngine
    from src.data_handler import DataHandler
    nlp_engine = NLPEngine()
    data_handler = DataHandler()
except ImportError:
    nlp_engine = None
    data_handler = None

# FIXED LANGUAGES - NO DUPLICATES
LANGUAGES = {
    'auto': 'Auto Detect',
    'en': 'English', 
    'hi': 'हिंदी', 
    'gu': 'ગુજરાતી', 
    'ta': 'தமிழ்', 
    'te': 'తెలుగు',
    'kn': 'ಕನ್ನಡ', 
    'ml': 'മലയാളം', 
    'mr': 'मराठी', 
    'bn': 'বাংলা', 
    'pa': 'ਪੰਜਾਬੀ',
    'or': 'ଓଡ଼ିଆ'
}

def safe_translate(text, src_lang, dest_lang):
    """Safe Google Translate - ERROR PROOF"""
    try:
        if src_lang not in LANGUAGES or dest_lang not in LANGUAGES:
            return text  # Return original if invalid language
        
        url = "https://translate.googleapis.com/translate_a/single"
        params = {
            'client': 'gtx',
            'sl': src_lang if src_lang != 'auto' else 'auto',
            'tl': dest_lang,
            'dt': 't',
            'q': text
        }
        response = requests.get(url, params=params, timeout=10)
        if response.status_code == 200:
            result = response.json()
            return result[0][0][0] if result and result[0] else text
    except Exception as e:
        print(f"Translation error: {e}")  # Silent fail
        return text
    return text

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['GET', 'POST'])
def analyze():
    if request.method == 'POST':
        if nlp_engine:
            text = request.json.get('text', '')
            result = nlp_engine.predict_sentiment(text)
            if data_handler:
                data_handler.log_prediction(result)
            return jsonify(result)
        return jsonify({'sentiment': 'neutral', 'confidence': 0.5})
    return render_template('analyze.html')

@app.route('/results')
def results():
    stats = {}
    if data_handler:
        stats = data_handler.get_stats()
    return render_template('results.html', stats=stats)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/translate', methods=['GET', 'POST'])
def translate():
    result = {}
    if request.method == 'POST':
        text = request.form.get('text', '').strip()
        from_lang = request.form.get('from_lang', 'auto')
        to_lang = request.form.get('to_lang', 'hi')
        
        # SAFETY CHECKS
        if not text:
            result = {'error': 'Text enter करें!'}
        else:
            translated = safe_translate(text, from_lang, to_lang)
            result = {
                'original': text,
                'translated': translated,
                'from_lang': LANGUAGES.get(from_lang, from_lang),
                'to_lang': LANGUAGES.get(to_lang, to_lang),
                'success': True
            }
    
    return render_template('translate.html', result=result, languages=LANGUAGES)

@app.errorhandler(404)
def not_found(error):
    return render_template('base.html'), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
