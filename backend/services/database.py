import os
from pymongo import MongoClient
from dotenv import load_dotenv
import certifi # <-- ADD THIS IMPORT

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = os.getenv("MONGO_DB_NAME")
COLLECTION_NAME = os.getenv("MONGO_COLLECTION_NAME")

# vvv MODIFY THIS LINE to include the tlsCAFile parameter vvv
client = MongoClient(MONGO_URI, tlsCAFile=certifi.where())

db = client[DB_NAME]
collection = db[COLLECTION_NAME]

print("Successfully connected to MongoDB using certifi.")

def save_mention(mention: dict):
    if collection.find_one({"url": mention["url"]}) is None:
        collection.insert_one(mention)
        print(f"Saved new mention: {mention['title']}")
        return True
    else:
        print(f"Mention already exists: {mention['title']}")
        return False

def get_recent_mentions(limit: int = 50):
    mentions_cursor = collection.find({}).sort("published_at", -1).limit(limit)
    mentions_list = []
    for mention in mentions_cursor:
        mention["_id"] = str(mention["_id"])
        mentions_list.append(mention)
    return mentions_list