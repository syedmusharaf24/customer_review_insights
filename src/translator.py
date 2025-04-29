#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pandas as pd
from deep_translator import GoogleTranslator
import time

def translate_text(text, source_lang='auto', target_lang='en'):
    """
    Translate text to target language using Google Translator.
    
    Parameters:
        text (str): Text to translate
        source_lang (str): Source language code (default: auto-detect)
        target_lang (str): Target language code (default: English)
        
    Returns:
        str: Translated text
    """
    try:
        if not isinstance(text, str) or text.strip() == '':
            return text
        
        # Limit text length to avoid API errors (Google Translator has a character limit)
        if len(text) > 5000:
            text = text[:5000]
            
        translator = GoogleTranslator(source=source_lang, target=target_lang)
        translated = translator.translate(text)
        
        # Add a small delay to avoid hitting rate limits
        time.sleep(0.2)
        
        return translated
    except Exception as e:
        print(f"Translation error: {str(e)}")
        return text  # Return original text on error

def translate_non_english(df):
    """
    Translate non-English reviews to English.
    
    Parameters:
        df (pandas.DataFrame): DataFrame with language detection results
        
    Returns:
        pandas.DataFrame: DataFrame with translated reviews
    """
    # Make a copy to avoid modifying the original
    result_df = df.copy()
    
    # Count non-English reviews
    non_english_count = len(result_df[~result_df['is_english']])
    print(f"Translating {non_english_count} non-English reviews...")
    
    # Translate only non-English reviews
    for idx, row in result_df[~result_df['is_english']].iterrows():
        source_lang = row['language']
        original_text = row['original_review']
        
        # Translate to English
        translated_text = translate_text(original_text, source_lang)
        
        # Update the review_text column with the translated text
        result_df.at[idx, 'review_text'] = translated_text
    
    # For English reviews, ensure review_text equals original_review
    result_df.loc[result_df['is_english'], 'review_text'] = result_df.loc[result_df['is_english'], 'original_review']
    
    print("Translation completed.")
    return result_df