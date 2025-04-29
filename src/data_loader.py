#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pandas as pd

def load_excel_data(filepath):
    """
    Load customer review data from Excel file.
    
    Parameters:
        filepath (str): Path to the Excel file
        
    Returns:
        pandas.DataFrame: DataFrame containing the reviews
    """
    try:
        # Try to determine the review column name
        df = pd.read_excel(filepath)
        
        # Check if there's a column that might contain reviews
        potential_review_columns = ['review', 'reviews', 'feedback', 'comment', 'comments', 'text']
        review_column = None
        
        for col in potential_review_columns:
            if col in df.columns:
                review_column = col
                break
        
        # If no standard column name found, use the first text column
        if review_column is None:
            for col in df.columns:
                if df[col].dtype == 'object':  # Check if column contains text
                    review_column = col
                    break
        
        # If we still don't have a column, use the first column
        if review_column is None:
            review_column = df.columns[0]
        
        # Create a standardized DataFrame
        reviews_df = pd.DataFrame({
            'review_id': range(1, len(df) + 1),
            'original_review': df[review_column].astype(str),
            'review_text': df[review_column].astype(str),  # Will be modified after translation
            'is_english': False,  # Will be updated by language detector
            'language': '',       # Will be filled by language detector
            'sentiment_score': 0.0,  # Will be filled by sentiment analyzer
            'sentiment': ''       # Will be filled by sentiment analyzer
        })
        
        print(f"Successfully loaded {len(reviews_df)} reviews from {filepath}")
        return reviews_df
    
    except Exception as e:
        print(f"Error loading data: {str(e)}")
        # Return empty DataFrame with correct structure
        return pd.DataFrame(columns=['review_id', 'original_review', 'review_text', 
                                    'is_english', 'language', 'sentiment_score', 'sentiment'])