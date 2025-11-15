import os
import requests
from dotenv import load_dotenv
import time

# Load environment variables
load_dotenv()

# The specific model we want to use for sentiment analysis
MODEL = "cardiffnlp/twitter-roberta-base-sentiment"
API_URL = f"https://api-inference.huggingface.co/models/{MODEL}"

# Get the token from the .env file
HF_TOKEN = os.getenv("HUGGINGFACE_TOKEN")

def analyze_sentiment(text: str) -> dict:
    """
    Analyzes the sentiment of a given text using the Hugging Face Inference API.
    """
    if not HF_TOKEN:
        print("Error: HUGGINGFACE_TOKEN not found.")
        return {"label": "Error", "score": 0.0}

    # Truncate text to avoid sending too much data
    truncated_text = text[:512]

    headers = {"Authorization": f"Bearer {HF_TOKEN}"}
    payload = {"inputs": truncated_text}

    try:
        response = requests.post(API_URL, headers=headers, json=payload)

        # The first time you use a model, the API has to load it, which can take ~20s.
        # This block handles that initial loading time.
        if response.status_code == 503:
            print("Model is loading, retrying in 20 seconds...")
            time.sleep(20) # Wait for the model to load
            response = requests.post(API_URL, headers=headers, json=payload)

        response.raise_for_status() # Raise an exception for other bad status codes
        
        data = response.json()
        
        # The API returns a list of lists of results. We need the one with the highest score.
        highest_score_result = max(data[0], key=lambda x: x['score'])
        
        # Map the label to a more readable format
        label_map = {
            "LABEL_0": "Negative",
            "LABEL_1": "Neutral",
            "LABEL_2": "Positive"
        }

        return {
            "label": label_map.get(highest_score_result['label'], 'Unknown'),
            "score": highest_score_result['score']
        }

    except requests.exceptions.RequestException as e:
        print(f"Error calling Hugging Face API: {e}")
        return {"label": "Error", "score": 0.0}
    except (KeyError, IndexError) as e:
        print(f"Error parsing Hugging Face API response: {e}, Response: {response.text}")
        return {"label": "Error", "score": 0.0}