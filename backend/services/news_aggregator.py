import os
import requests
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get the API key from environment variables
API_KEY = os.getenv("NEWS_API_KEY")
BASE_URL = "https://gnews.io/api/v4/search"

def fetch_mentions(brand_name: str):
    """
    Fetches news articles mentioning a specific brand from the GNews API.
    """
    if not API_KEY:
        print("Error: NEWS_API_KEY not found. Please set it in the .env file.")
        return []

    # Parameters for the API request
    params = {
        "q": brand_name,
        "token": API_KEY,
        "lang": "en",
        "max": 10  # Fetch the 10 most recent articles
    }

    try:
        # Make the GET request to the GNews API
        response = requests.get(BASE_URL, params=params)
        
        # Raise an exception for bad status codes (4xx or 5xx)
        response.raise_for_status()
        
        data = response.json()
        articles = data.get("articles", [])
        
        # Format the articles into a cleaner structure
        formatted_mentions = []
        for article in articles:
            formatted_mentions.append({
                "source": "News",
                "source_name": article["source"]["name"],
                "title": article["title"],
                "text": article["description"], # Using description as the main text
                "url": article["url"],
                "published_at": article["publishedAt"]
            })
            
        return formatted_mentions

    except requests.exceptions.RequestException as e:
        print(f"An error occurred while fetching data: {e}")
        return []