import os
import requests
from dotenv import load_dotenv
import time

load_dotenv()

# NEW, more reliable model
MODEL = "distilbert-base-uncased-finetuned-sst-2-english"
API_URL = f"https://api-inference.huggingface.co/models/{MODEL}"
HF_TOKEN = os.getenv("HUGGINGFACE_TOKEN")

def analyze_sentiment(text: str) -> dict:
    if not HF_TOKEN:
        print("Error: HUGGINGFACE_TOKEN not found.")
        return {"label": "Error", "score": 0.0}

    truncated_text = text[:512]
    headers = {"Authorization": f"Bearer {HF_TOKEN}"}
    payload = {"inputs": truncated_text}

    try:
        response = requests.post(API_URL, headers=headers, json=payload)

        if response.status_code == 503: # Handle model loading
            print("Model is loading, retrying in 20 seconds...")
            time.sleep(20)
            response = requests.post(API_URL, headers=headers, json=payload)

        response.raise_for_status()
        data = response.json()
        
        # This new model has a simpler output format
        highest_score_result = max(data[0], key=lambda x: x['score'])
        
        # Let's map the labels to our desired format
        label_map = {
            "POSITIVE": "Positive",
            "NEGATIVE": "Negative",
        }

        return {
            "label": label_map.get(highest_score_result['label'], 'Neutral'),
            "score": highest_score_result['score']
        }

    except requests.exceptions.RequestException as e:
        print(f"Error calling Hugging Face API: {e}")
        return {"label": "Error", "score": 0.0}
    except (KeyError, IndexError) as e:
        print(f"Error parsing Hugging Face API response: {e}, Response: {response.text}")
        return {"label": "Error", "score": 0.0}