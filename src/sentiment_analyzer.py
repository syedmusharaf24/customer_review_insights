#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pandas as pd
from textblob import TextBlob
import nltk
import os

def download_nltk_resources():
    """Download required NLTK resources if they don't exist"""
    try:
        nltk.data.find('vader_lexicon')
        nltk.data.find('punkt')
    except LookupError:
        nltk.download('vader_lexicon')
        nltk.download('punkt')

def analyze_sentiment_textblob(text):
    """
    Analyze sentiment using TextBlob.
    
    Parameters:
        text (str): Text to analyze
        
    Returns:
        tuple: (sentiment_score, sentiment_label)
    """
    if not isinstance(text, str) or text.strip() == '':
        return 0.0, 'neutral'
    
    # Analyze sentiment
    blob = TextBlob(text)
    sentiment_score = blob.sentiment.polarity
    
    # Determine sentiment label
    if sentiment_score > 0.1:
        sentiment_label = 'positive'
    elif sentiment_score < -0.1:
        sentiment_label = 'negative'
    else:
        sentiment_label = 'neutral'
    
    return sentiment_score, sentiment_label

def analyze_sentiment(df):
    """
    Analyze the sentiment of reviews in the DataFrame.
    
    Parameters:
        df (pandas.DataFrame): DataFrame with reviews
        
    Returns:
        pandas.DataFrame: DataFrame with sentiment analysis results
    """
    # Download required NLTK resources
    download_nltk_resources()
    
    # Make a copy to avoid modifying the original
    result_df = df.copy()
    
    print("Performing sentiment analysis...")
    
    # Apply sentiment analysis to each review
    result_df[['sentiment_score', 'sentiment']] = result_df.apply(
        lambda row: pd.Series(analyze_sentiment_textblob(row['review_text'])), 
        axis=1
    )
    
    # Count sentiment categories
    positive_count = len(result_df[result_df['sentiment'] == 'positive'])
    negative_count = len(result_df[result_df['sentiment'] == 'negative'])
    neutral_count = len(result_df[result_df['sentiment'] == 'neutral'])
    
    print(f"Sentiment analysis completed: {positive_count} positive, "
          f"{negative_count} negative, {neutral_count} neutral reviews.")
    
    return result_df