from pymongo import MongoClient
import os

MONGO_URI = os.getenv("MONGO_URI")

client = MongoClient(MONGO_URI)

db = client["fightlife"]
players_collection = db["players"]
world_collection = db["world"]
