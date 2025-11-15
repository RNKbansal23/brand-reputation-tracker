import os
from pymongo import MongoClient
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get MongoDB connection details from .env
MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = os.getenv("MONGO_DB_NAME")
COLLECTION_NAME = os.getenv("MONGO_COLLECTION_NAME")

# Establish a connection to the database
client = MongoClient(MONGO_URI)
db = client[DB_NAME]
collection = db[COLLECTION_NAME]

print("Successfully connected to MongoDB.")

def save_mention(mention: dict):
    """Saves a single mention to the database if it doesn't already exist."""
    # We use the article URL as a unique identifier to prevent duplicates
    if collection.find_one({"url": mention["url"]}) is None:
        collection.insert_one(mention)
        print(f"Saved new mention: {mention['title']}")
        return True
    else:
        print(f"Mention already exists: {mention['title']}")
        return False

def get_recent_mentions(limit: int = 50):
    """Retrieves the most recent mentions from the database."""
    # Sorts by 'published_at' in descending order (-1) and limits the result
    mentions_cursor = collection.find({}).sort("published_at", -1).limit(limit)
    
    # Convert cursor to a list and handle the MongoDB '_id' object
    mentions_list = []
    for mention in mentions_cursor:
        mention["_id"] = str(mention["_id"]) # Convert ObjectId to string for JSON compatibility
        mentions_list.append(mention)
        
    return mentions_list