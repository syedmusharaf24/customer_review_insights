#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import json

def generate_sentiment_pie_chart(df):
    """
    Generate a pie chart of sentiment distribution.
    
    Parameters:
        df (pandas.DataFrame): DataFrame with sentiment analysis results
        
    Returns:
        dict: Plotly chart data
    """
    sentiment_counts = df['sentiment'].value_counts().reset_index()
    sentiment_counts.columns = ['sentiment', 'count']
    
    # Define colors for sentiments
    colors = {'positive': '#4CAF50', 'negative': '#F44336', 'neutral': '#9E9E9E'}
    
    fig = px.pie(
        sentiment_counts, 
        values='count', 
        names='sentiment',
        title='Sentiment Distribution',
        color='sentiment',
        color_discrete_map=colors
    )
    
    fig.update_traces(textposition='inside', textinfo='percent+label')
    fig.update_layout(uniformtext_minsize=12, uniformtext_mode='hide')
    
    return json.loads(fig.to_json())

def generate_language_pie_chart(df):
    """
    Generate a pie chart of language distribution.
    
    Parameters:
        df (pandas.DataFrame): DataFrame with language detection results
        
    Returns:
        dict: Plotly chart data
    """
    language_counts = df['is_english'].value_counts().reset_index()
    language_counts.columns = ['is_english', 'count']
    language_counts['language'] = language_counts['is_english'].map({True: 'English', False: 'Non-English'})
    
    fig = px.pie(
        language_counts, 
        values='count', 
        names='language',
        title='Language Distribution',
        color='language',
        color_discrete_map={'English': '#2196F3', 'Non-English': '#FF9800'}
    )
    
    fig.update_traces(textposition='inside', textinfo='percent+label')
    fig.update_layout(uniformtext_minsize=12, uniformtext_mode='hide')
    
    return json.loads(fig.to_json())

def generate_sentiment_histogram(df):
    """
    Generate a histogram of sentiment scores.
    
    Parameters:
        df (pandas.DataFrame): DataFrame with sentiment analysis results
        
    Returns:
        dict: Plotly chart data
    """
    fig = px.histogram(
        df, 
        x='sentiment_score',
        nbins=20,
        title='Distribution of Sentiment Scores',
        color_discrete_sequence=['#673AB7']
    )
    
    fig.update_layout(
        xaxis_title='Sentiment Score',
        yaxis_title='Number of Reviews',
        bargap=0.1
    )
    
    return json.loads(fig.to_json())

def generate_sentiment_by_language(df):
    """
    Generate a grouped bar chart of sentiment by language.
    
    Parameters:
        df (pandas.DataFrame): DataFrame with sentiment and language results
        
    Returns:
        dict: Plotly chart data
    """
    # Create language category
    df['language_category'] = df['is_english'].map({True: 'English', False: 'Non-English'})
    
    # Aggregate data
    grouped_data = df.groupby(['language_category', 'sentiment']).size().reset_index(name='count')
    
    # Create the figure
    fig = px.bar(
        grouped_data,
        x='language_category',
        y='count',
        color='sentiment',
        title='Sentiment Distribution by Language',
        barmode='group',
        color_discrete_map={'positive': '#4CAF50', 'negative': '#F44336', 'neutral': '#9E9E9E'}
    )
    
    fig.update_layout(
        xaxis_title='Language',
        yaxis_title='Number of Reviews'
    )
    
    return json.loads(fig.to_json())

def generate_charts(df):
    """
    Generate all charts for the dashboard.
    
    Parameters:
        df (pandas.DataFrame): DataFrame with analysis results
        
    Returns:
        dict: Dictionary with all chart data
    """
    charts = {
        'sentiment_pie': generate_sentiment_pie_chart(df),
        'language_pie': generate_language_pie_chart(df),
        'sentiment_histogram': generate_sentiment_histogram(df),
        'sentiment_by_language': generate_sentiment_by_language(df)
    }
    
    return charts   