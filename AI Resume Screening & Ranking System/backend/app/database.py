import os
from typing import Optional

from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.database import Database


MONGO_URL = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
DATABASE_NAME = os.getenv("MONGODB_DB_NAME", "resume_screening_db")

_client: Optional[MongoClient] = None


def get_client() -> MongoClient:
    global _client
    if _client is None:
        _client = MongoClient(MONGO_URL)
    return _client


def get_database() -> Database:
    return get_client()[DATABASE_NAME]


def get_rankings_collection() -> Collection:
    return get_database()["rankings"]

