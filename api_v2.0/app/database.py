import motor.motor_asyncio

from .config import settings

client = motor.motor_asyncio.AsyncIOMotorClient(settings.mongo_url)
db = client[settings.mongo_database]