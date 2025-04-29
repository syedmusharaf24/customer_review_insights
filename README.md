# Customer Review Insights

A comprehensive solution for analyzing customer reviews using sentiment analysis, language detection, and translation to provide valuable insights.

## 🌟 Features

- **Multi-language Support**: Automatically detects the language of each review
- **Translation**: Translates non-English reviews to English for better sentiment analysis
- **Sentiment Analysis**: Analyzes the sentiment of each review (positive, negative, neutral)
- **Interactive Dashboard**: Visualizes the results with charts and statistics
- **Excel/CSV Import**: Easily import customer reviews from Excel or CSV files

## 💻 Technical Overview

This project aims to enhance sentiment analysis accuracy by first translating non-English reviews to English before performing sentiment analysis. The process includes:

1. **Data Import**: Load customer reviews from Excel/CSV files
2. **Language Detection**: Identify the language of each review
3. **Translation**: Translate non-English reviews to English
4. **Sentiment Analysis**: Apply sentiment analysis techniques
5. **Visualization**: Display results in an interactive dashboard

## 📋 Requirements

- Python 3.8+
- Flask
- pandas
- NLTK
- langdetect
- deep-translator
- TextBlob
- Plotly
- See `requirements.txt` for complete list

## 🚀 Installation

1. Clone the repository
   ```bash
   git clone https://github.com/yourusername/customer-review-insights.git
   cd customer-review-insights
   ```

2. Create a virtual environment
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies
   ```bash
   pip install -r requirements.txt
   ```

4. Run the application
   ```bash
   python app.py
   ```

5. Open a web browser and navigate to http://127.0.0.1:5000/

## 📊 Dashboard

The dashboard provides:

- Overall statistics (total reviews, languages, sentiment distribution)
- Sentiment distribution pie chart
- Language distribution pie chart
- Sentiment score histogram
- Sentiment by language comparison

## 📋 Data Format

The application accepts Excel (.xlsx, .xls) or CSV files with a column containing review text. The system will try to automatically detect the review column, but it's best if your data includes columns with names like:

- review
- reviews
- feedback
- comment
- comments
- text

## 📈 Why Translation Matters

When performing sentiment analysis directly on non-English content, accuracy can be significantly lower due to:

1. Limited language-specific resources in many sentiment analysis tools
2. Variations in language expressions and idioms
3. Different grammatical structures affecting analysis algorithms

By translating to English first, we leverage the robust English language sentiment analysis capabilities, resulting in more accurate sentiment classification regardless of the original language.

## 📝 Sample Data

A sample dataset is included (`data/sample_reviews.xlsx`) with reviews in multiple languages. You can also generate your own sample data by running:

```bash
python data/sample_reviews.xlsx
```

## 📚 Project Structure

```
customer_review_insights/
│
├── app.py                 # Main application entry point
├── requirements.txt       # Project dependencies
│
├── data/
│   └── sample_reviews.xlsx  # Sample review data
│
├── src/
│   ├── __init__.py
│   ├── data_loader.py     # Functions to load review data
│   ├── language_detector.py # Language detection functionality
│   ├── translator.py      # Translation functionality
│   ├── sentiment_analyzer.py # Sentiment analysis implementation
│   └── visualizer.py      # Data visualization components
│
├── static/
│   ├── css/
│   │   └── styles.css     # Custom styling
│   └── js/
│       └── dashboard.js   # JavaScript for interactive elements
│
└── templates/
    ├── index.html         # Main application page
    ├── upload.html        # File upload interface
    └── dashboard.html     # Results dashboard
```

## 🔄 Workflow

1. User uploads an Excel/CSV file containing customer reviews
2. System loads and processes the data
3. Language detection is performed on each review
4. Non-English reviews are translated to English
5. Sentiment analysis is performed on all reviews (original English + translated)
6. Results are visualized in the dashboard

## 📝 License

This project is licensed under the MIT License.
