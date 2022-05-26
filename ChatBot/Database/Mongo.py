from ChatBot import MONGO_URL, USERBOT_USERNAME
from motor.motor_asyncio import AsyncIOMotorClient


class Database:
    def __init__(self, uri, database_name):
        self._client = motor.motor_asyncio.AsyncIOMotorClient(uri)
        self.db = self._client[database_name]
        self.col = self.db.users

db = Database(MONGO_URL)
