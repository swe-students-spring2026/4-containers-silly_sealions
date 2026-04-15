"""Database connection module for the web app."""
import os
from pymongo import MongoClient

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/speech_rater")

client = MongoClient(MONGO_URI)

db = client.get_default_database()

users_collection = db["users"]
speeches_collection = db["speeches"]
