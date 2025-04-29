"""
Source package for multilingual sentiment analysis application.

This package contains modules for data loading, language detection,
translation, sentiment analysis, and visualization.
"""

__version__ = '0.1.0'
__author__ = 'Your Name'

# Import key functions to make them available directly from the package
from .data_loader import load_excel_data
from .language_detector import detect_languages
from .translator import translate_non_english
from .sentiment_analyzer import analyze_sentiment
from .visualizer import generate_charts

# Define what gets imported with "from src import *"
__all__ = [
    'load_excel_data',
    'detect_languages',
    'translate_non_english',
    'analyze_sentiment',
    'generate_charts',
]