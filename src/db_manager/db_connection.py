import os

from pymongo import MongoClient
from dotenv import load_dotenv

# Load dotenv
load_dotenv()

# Connect to MongoDB (generate client)
client = MongoClient(os.getenv("DB_CONNECTION_STRING"))


# Return client to who needs to operate on db
def get_db_client():
    return client
