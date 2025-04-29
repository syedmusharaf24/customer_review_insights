#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import pandas as pd
import json
from flask import Flask, render_template, request, redirect, url_for, jsonify
from werkzeug.utils import secure_filename
sys.path.append(os.path.join(os.path.dirname(__file__), 'modules'))

from src.data_loader import load_excel_data
from src.language_detector import detect_languages
from src.translator import translate_non_english
from src.sentiment_analyzer import analyze_sentiment
from src.visualizer import generate_charts

# Initialize Flask app
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'data'
app.config['ALLOWED_EXTENSIONS'] = {'xlsx', 'xls', 'csv'}
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # Check if the post request has the file part
        if 'file' not in request.files:
            return redirect(request.url)
        
        file = request.files['file']
        
        # If user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            return redirect(request.url)
        
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            
            # Process the file and redirect to dashboard
            return redirect(url_for('process_data', filename=filename))
    
    return render_template('upload.html')

@app.route('/process/<filename>')
def process_data(filename):
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    
    # Load the data
    reviews_df = load_excel_data(filepath)
    
    # Detect languages
    reviews_df = detect_languages(reviews_df)
    
    # Translate non-English reviews
    reviews_df = translate_non_english(reviews_df)
    
    # Analyze sentiment
    results_df = analyze_sentiment(reviews_df)
    
    # Save processed data for the session
    processed_filepath = os.path.join(app.config['UPLOAD_FOLDER'], 'processed_' + filename)
    results_df.to_excel(processed_filepath, index=False)
    
    return redirect(url_for('dashboard', filename='processed_' + filename))

@app.route('/dashboard/<filename>')
def dashboard(filename):
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    df = pd.read_excel(filepath)
    
    # Generate charts and statistics
    charts_data = generate_charts(df)
    
    # Get statistics
    stats = {
        'total_reviews': len(df),
        'english_reviews': len(df[df['is_english'] == True]),
        'non_english_reviews': len(df[df['is_english'] == False]),
        'positive_reviews': len(df[df['sentiment'] == 'positive']),
        'negative_reviews': len(df[df['sentiment'] == 'negative']),
        'neutral_reviews': len(df[df['sentiment'] == 'neutral']),
    }
    
    return render_template('dashboard.html', 
                          charts_data=json.dumps(charts_data), 
                          stats=stats)

@app.route('/api/data/<filename>')
def get_data(filename):
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    df = pd.read_excel(filepath)
    return jsonify(df.to_dict(orient='records'))

if __name__ == '__main__':
    # Create folders if they don't exist
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)), debug=True)