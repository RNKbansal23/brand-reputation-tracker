import os
from pymongo import MongoClient
from dotenv import load_dotenv
# We no longer need certifi, but we'll leave the import in case we need to revert.
import certifi 

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = os.getenv("MONGO_DB_NAME")
COLLECTION_NAME = os.getenv("MONGO_COLLECTION_NAME")

# THIS IS THE FINAL FIX: We are telling pymongo to not verify the SSL certificate.
# This bypasses the handshake failure in Render's environment.
client = MongoClient(MONGO_URI, tlsAllowInvalidCertificates=True)

db = client[DB_NAME]
collection = db[COLLECTION_NAME]

print("MongoDB client initialized with SSL verification disabled.")

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