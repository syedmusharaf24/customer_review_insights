#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pandas as pd
from langdetect import detect, LangDetectException

def detect_language(text):
    """
    Detect the language of a given text.
    
    Parameters:
        text (str): The text to analyze
        
    Returns:
        str: The detected language code
    """
    try:
        if not isinstance(text, str) or text.strip() == '':
            return 'en'  # Default to English for empty strings
        
        lang = detect(text)
        return lang
    except LangDetectException:
        return 'en'  # Default to English on error

def detect_languages(df):
    """
    Detect the language of each review in the DataFrame.
    
    Parameters:
        df (pandas.DataFrame): DataFrame containing reviews
        
    Returns:
        pandas.DataFrame: DataFrame with language detection results
    """
    # Make a copy to avoid modifying the original
    result_df = df.copy()
    
    # Detect language for each review
    result_df['language'] = result_df['original_review'].apply(detect_language)
    
    # Mark if the review is in English
    result_df['is_english'] = result_df['language'] == 'en'
    
    print(f"Language detection completed. Found {sum(result_df['is_english'])} English reviews and "
          f"{len(result_df) - sum(result_df['is_english'])} non-English reviews.")
    
    return result_df