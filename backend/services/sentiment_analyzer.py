# We are using a built-in library now, no more external APIs.
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer

# This downloads the necessary data for NLTK the first time it runs.
try:
    nltk.data.find('sentiment/vader_lexicon.zip')
except LookupError:
    print("Downloading NLTK vader_lexicon...")
    nltk.download('vader_lexicon')

# Create an instance of the analyzer
sia = SentimentIntensityAnalyzer()

def analyze_sentiment(text: str) -> dict:
    """
    Analyzes sentiment using the built-in NLTK library.
    This is reliable and does not depend on external APIs.
    """
    if not text:
        return {"label": "Neutral", "score": 0.0}

    # The sia.polarity_scores returns a dictionary with neg, neu, pos, and compound scores.
    scores = sia.polarity_scores(text)
    
    # We use the 'compound' score to determine the overall sentiment.
    compound_score = scores['compound']
    
    label = "Neutral"
    if compound_score >= 0.05:
        label = "Positive"
    elif compound_score <= -0.05:
        label = "Negative"

    return {
        "label": label,
        "score": compound_score 
    }