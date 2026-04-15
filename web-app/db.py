"""Database connection module for the web app."""
import os
from pymongo import MongoClient

client = MongoClient(os.getenv("MONGO_URI", "mongodb://localhost:27017/"))
db = client["sillysealions"]

users_collection = db["users"]
speeches_collection = db["speeches"]
